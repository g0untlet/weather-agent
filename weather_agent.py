import os
import requests
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

# --- 1. AUTHENTIFIZIERUNG (WICHTIG!) ---
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
api_key = os.getenv("ANTHROPIC_API_KEY")

# --- 2. TOOL DEFINITION ---
@tool
def get_real_weather(city: str):
    """Gibt die aktuelle Temperatur für München zurück."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.13&longitude=11.57&current_weather=true"
    res = requests.get(url).json()
    temp = res['current_weather']['temperature']
    return f"In {city} sind es aktuell {temp}°C."

# --- 3. AGENT SETUP MIT KEY UND MEMORY ---
# Hier wird der Key explizit an das Modell übergeben
llm = ChatAnthropic(
    model="claude-3-haiku-20240307", 
    temperature=0,
    api_key=api_key 
)

memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=[get_real_weather],
    checkpointer=memory,
    system_prompt="Du bist ein Butler. Antworte kurz."
)

# --- 4. EXECUTION MIT VERBESSERTEM LOGGING ---
config = {"configurable": {"thread_id": "session_muenchen_001"}}

def ask_butler(query):
    print(f"\nUser: {query}")
    response = agent.invoke({"messages": [("user", query)]}, config=config)
    
    # Wir suchen die letzte Nachricht, die wirklich Text enthält
    for msg in reversed(response["messages"]):
        if msg.content:
            print(f"Butler: {msg.content}")
            break

ask_butler("Wie ist das Wetter in München?")
ask_butler("Und brauche ich dort eine Jacke?")

