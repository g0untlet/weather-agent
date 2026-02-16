# 🌤️ Munich Weather Butler

A modular AI Agent built with **LangGraph**, **LangChain**, and **Streamlit**. The agent acts as a polite butler ("Johann") providing detailed weather advice for Munich using real-time data from the Open-Meteo API.

---

## 📁 Project Structure & Responsibilities

| File | Responsibility |
| :--- | :--- |
| **`weather_gui.py`** | **Frontend**: Streamlit-based web interface. |
| **`agent_core.py`** | **Orchestration**: Logic, LLM, and Memory setup. |
| **`weather_tools.py`** | **Capabilities**: Weather API integration. |
| **`requirements.txt`** | **Dependencies**: Required Python packages. |
| **`.env`** | **Secrets**: API Keys ANTHROPIC_API_KEY (Excluded from Git). |

---

## 🚀 How to Run

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Launch
```bash
streamlit run weather_gui.py
