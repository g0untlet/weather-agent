import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver

# Dein Tool importieren
from weather_tools import get_detailed_weather

load_dotenv()

# 1. LLM mit Tool-Bindung
llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key=os.getenv("ANTHROPIC_API_KEY"))
llm_with_tools = llm.bind_tools([get_detailed_weather])

# 2. Definition der Logik-Knoten (Nodes)
def call_model(state: MessagesState):
    messages = state['messages']
    # System Prompt hinzufügen (optional, aber sauberer)
    system_message = {"role": "system", "content": "Du bist ein Butler. Antworte kurz."}
    response = llm_with_tools.invoke([system_message] + messages)
    return {"messages": [response]}

# 3. Den Graph bauen
workflow = StateGraph(MessagesState)

# Knoten hinzufügen
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode([get_detailed_weather]))

# Kanten (Edges) definieren
workflow.add_edge(START, "agent")

# Bedingte Kante: Soll das Tool aufgerufen werden oder sind wir fertig?
def should_continue(state: MessagesState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# 4. Kompilieren mit Memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# --- Ausführung ---
config = {"configurable": {"thread_id": "butler_session_1"}}

def ask_butler(query):
    print(f"\nUser: {query}")
    inputs = {"messages": [("user", query)]}
    output = app.invoke(inputs, config=config)
    print(f"Butler: {output['messages'][-1].content}")

ask_butler("Wie ist das Wetter in Hamburg?")

