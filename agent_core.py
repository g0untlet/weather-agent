import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

# Importiere das aufgebohrte Tool aus deiner weather_tools.py
from weather_tools import get_detailed_weather

# Lade Umgebungsvariablen (.env)
load_dotenv()

def get_weather_agent():
    """
    Initialisiert den Butler-Agenten mit LangGraph-Memory und Tool-Zugriff.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY wurde nicht in der .env Datei gefunden!")

    # Initialisierung des LLM (Claude 3 Haiku für Effizienz auf dem Chromebook)
    llm = ChatAnthropic(
        model="claude-3-haiku-20240307", 
        temperature=0, 
        api_key=api_key
    )

    # Das Gedächtnis des Agenten (In-Memory Checkpointer für LangGraph)
    memory = MemorySaver()
    
    # Definition des System-Prompts für das Verhalten des Butlers
    system_prompt = (
        "Du bist ein exzellenter, bayerischer Butler namens Johann. "
        "Du lebst in München und berätst deinen Herrn höflich und präzise. "
        "Nutze die detaillierten Wetterdaten (Wind, Temperatur, Zustand), "
        "um konkrete Empfehlungen für Kleidung oder Aktivitäten zu geben."
    )

    # Erstellung des Agenten-Graphen
    # create_agent verbindet das Modell, die Tools und die Memory-Schicht
    agent = create_agent(
        model=llm,
        tools=[get_detailed_weather],
        checkpointer=memory,
        system_prompt=system_prompt
    )
    
    return agent

# Falls man die Datei testweise direkt ausführt
if __name__ == "__main__":
    agent = get_weather_agent()
    print("Agent erfolgreich initialisiert.")

