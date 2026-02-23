import requests
from langchain_core.tools import tool
from datetime import datetime

def get_coordinates(city: str):
    """Sucht Koordinaten und die korrekte Zeitzone für eine Stadt."""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=de&format=json"
    response = requests.get(geo_url).json()
    
    if not response.get('results'):
        return None
    
    result = response['results'][0]
    return {
        "lat": result['latitude'],
        "lon": result['longitude'],
        "timezone": result.get('timezone', 'Auto'), # Wichtig für die lokale Zeit
        "full_name": f"{result['name']} ({result.get('country', '')})"
    }

@tool
def get_detailed_weather(city: str):
    """Gibt Wetter und lokale Uhrzeit für eine beliebige Stadt zurück."""
    coords = get_coordinates(city)
    if not coords:
        return f"Ich konnte den Ort '{city}' leider nicht finden."

    # Wir fügen &timezone=... hinzu, um lokale Zeitdaten zu erhalten
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}"
        f"&current_weather=true&timezone={coords['timezone']}"
    )
    
    try:
        res = requests.get(url, timeout=10).json()
        current = res.get('current_weather', {})
        
        # Lokale Zeit der Stadt extrahieren
        raw_time = current.get('time') # Format: 2026-02-23T14:30
        local_time = datetime.fromisoformat(raw_time).strftime("%H:%M Uhr")
        
        temp = current.get('temperature')
        is_day = current.get('is_day') # 1 für Tag, 0 für Nacht
        day_info = "Tag" if is_day == 1 else "Nacht"
        
        return (
            f"Wetterbericht für {coords['full_name']}:\n"
            f"- Lokale Uhrzeit: {local_time} ({day_info})\n"
            f"- Temperatur: {temp}°C\n"
            f"- Windgeschwindigkeit: {current.get('windspeed')} km/h"
        )
    except Exception as e:
        return f"Fehler beim Abrufen der Daten für {city}: {e}"
    
