import requests
from langchain_core.tools import tool

@tool
def get_detailed_weather(city: str):
    """Gibt detaillierte Wetterdaten für München zurück (Temp, Wind, Feuchtigkeit, Zustand)."""
    # Erweiterte Parameter: relative_humidity_2m und wind_speed_10m
    url = (
        "https://api.open-meteo.com/v1/forecast?latitude=48.13&longitude=11.57"
        "&current_weather=true&hourly=relative_humidity_2m"
    )
    
    try:
        res = requests.get(url, timeout=10).json()
        current = res.get('current_weather', {})
        
        # Wetter-Code in Text übersetzen (vereinfacht)
        wmo_code = current.get('weathercode', 0)
        condition = "Klar/Heiter" if wmo_code <= 2 else "Bewölkt/Regen"
        
        temp = current.get('temperature')
        wind = current.get('windspeed')
        
        # Wir geben einen strukturierten String zurück
        return (
            f"Wetterbericht für {city}:\n"
            f"- Temperatur: {temp}°C\n"
            f"- Zustand: {condition} (Code: {wmo_code})\n"
            f"- Windgeschwindigkeit: {wind} km/h\n"
            f"Hinweis: Nutze diese Daten für eine detaillierte Empfehlung."
        )
    except Exception as e:
        return f"Fehler beim Abrufen der Wetterdaten: {e}"
