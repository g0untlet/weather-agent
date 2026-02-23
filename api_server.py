from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from agent_core import get_weather_agent

app = FastAPI(title="Johann Weather API")
agent = get_weather_agent()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """Verarbeitet die Anfrage und gibt die vollständige Antwort zurück."""
    config = {"configurable": {"thread_id": "api_session"}}
    
    # Wir rufen den Agenten auf und warten auf das finale Ergebnis
    response = agent.invoke(
        {"messages": [("user", request.message)]}, 
        config=config
    )
    
    # Die letzte Nachricht im Graph ist die Antwort von Johann
    final_reply = response["messages"][-1].content
    
    return {"reply": final_reply}

@app.get("/health")
async def health_check():
    """Gibt den Status des Backends zurück für Monitoring-Tools."""
    return {"status": "online", "agent": "Johann"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)

