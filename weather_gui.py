import streamlit as st
import requests

# 1. Seitenkonfiguration
st.set_page_config(
    page_title="Butler Johann", 
    page_icon="🌤️", 
    layout="centered"
)

# 2. Hilfsfunktionen
def check_backend_health():
    """Prüft die Erreichbarkeit des FastAPI-Backends."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=1)
        return response.status_code == 200
    except:
        return False

def get_johann_reply(user_input):
    """Sendet die Anfrage synchron an das Backend."""
    url = "http://localhost:8000/chat"
    try:
        response = requests.post(
            url, 
            json={"message": user_input}, 
            timeout=45
        )
        response.raise_for_status()
        return response.json().get("reply", "Ich bitte um Entschuldigung, ich habe keine Antwort erhalten.")
    except Exception as e:
        return f"❌ Technischer Fehler: {str(e)}"

# 3. Sidebar mit Status-Anzeige (Health Check)
with st.sidebar:
    st.header("System-Status")
    is_online = check_backend_health()
    if is_online:
        st.success("Johann ist bereit", icon="🤖")
    else:
        st.error("Johann ist offline", icon="🔌")
        st.info("Bitte starte den `api_server.py` im Terminal.")
    
    if st.button("Verbindung neu prüfen"):
        st.rerun()
    
    st.divider()
    if st.button("Chat-Verlauf löschen"):
        st.session_state.messages = []
        st.rerun()

# 4. Hauptoberfläche
status_emoji = "🟢" if is_online else "🔴"
st.title(f"🌤️ Butler Johann {status_emoji}")
st.caption("Präzise Analysen statt schneller Versprechen.")

# Session State für Chat-Historie
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat-Verlauf anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat-Eingabe
if prompt := st.chat_input("Wie kann ich behilflich sein, mein Herr?"):
    # User Nachricht hinzufügen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Butler Antwort generieren
    if is_online:
        with st.chat_message("assistant"):
            with st.spinner("Johann konsultiert die Wetterkarten..."):
                reply = get_johann_reply(prompt)
                st.toast("Daten empfangen!", icon="✅")
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
    else:
        st.warning("Ich kann derzeit keine Verbindung zum Archiv aufbauen (Backend offline).")

