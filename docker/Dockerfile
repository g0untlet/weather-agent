FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# System-Abhängigkeiten (falls nötig für manche Python-Pakete)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Zuerst nur requirements kopieren (besseres Caching)
COPY requirements.txt .

# Upgrade pip und installiere Abhängigkeiten
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Nur die notwendigen Backend-Skripte kopieren
COPY api_server.py .
COPY agent_core.py .
COPY weather_agent.py .
COPY weather_tools.py .

# Port für FastAPI freigeben
EXPOSE 8000

# Startbefehl: Bindet auf 0.0.0.0, damit der Container im Netzwerk erreichbar ist
CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
