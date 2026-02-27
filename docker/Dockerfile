# Nutzen eines schlanken Python-Images für minimale Image-Größe
FROM python:3.11-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# System-Abhängigkeiten installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nur die notwendigen Backend-Skripte kopieren
COPY api_server.py .
COPY agent_core.py .
COPY weather_agent.py .
COPY weather_tools.py .

# Port für FastAPI freigeben
EXPOSE 8000

# Startbefehl: Bindet auf 0.0.0.0, damit der Container im Netzwerk erreichbar ist
CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
