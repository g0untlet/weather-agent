import streamlit as st
from agent_core import get_weather_agent

st.set_page_config(page_title="Butler Agent", page_icon="🤖")
st.title("Dein Wetter-Butler 🌤️")

# Agent einmalig initialisieren
if "agent" not in st.session_state:
    st.session_state.agent = get_weather_agent()
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

    # Agenten-Logik aufrufen
    config = {"configurable": {"thread_id": "streamlit_session"}}
    response = st.session_state.agent.invoke({"messages": [("user", prompt)]}, config=config)
    
    final_text = response["messages"][-1].content
    
    with st.chat_message("assistant"):
        st.markdown(final_text)
    st.session_state.messages.append({"role": "assistant", "content": final_text})

