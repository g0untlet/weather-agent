import streamlit as st
import os, requests
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

# --- Initialisierung (wie gehabt) ---
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

@tool
def get_real_weather(city: str):
    """Gibt die aktuelle Temperatur für München zurück."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.13&longitude=11.57&current_weather=true"
    res = requests.get(url).json()
    temp = res['current_weather']['temperature']
    return f"In {city} sind es aktuell {temp}°C."

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Butler Agent", page_icon="🤖")
st.title("Dein Wetter-Butler 🌤️")

# Agent im Session State halten (verhindert Neu-Initialisierung bei jedem Klick)
if "agent" not in st.session_state:
    llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0, api_key=api_key)
    st.session_state.memory = MemorySaver()
    st.session_state.agent = create_agent(
        model=llm,
        tools=[get_real_weather],
        checkpointer=st.session_state.memory,
        system_prompt="Du bist ein Butler. Antworte höflich und präzise."
    )
    st.session_state.messages = []

# Chat-Historie anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat-Input
if prompt := st.chat_input("Wie kann ich helfen?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agenten-Logik
    config = {"configurable": {"thread_id": "streamlit_session"}}
    response = st.session_state.agent.invoke({"messages": [("user", prompt)]}, config=config)
    
    # Letzte Antwort finden
    final_text = response["messages"][-1].content
    
    with st.chat_message("assistant"):
        st.markdown(final_text)
    st.session_state.messages.append({"role": "assistant", "content": final_text})

