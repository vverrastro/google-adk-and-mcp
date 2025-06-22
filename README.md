# 💬 Google ADK + MCP  (Filesystem Agent AI)

This project demonstrates the integration of **Google Advanced Developer Kit (ADK)** with the **Model Context Protocol (MCP)** to explore and interact with a local filesystem through a conversational LLM agent.

It includes two modes: a **terminal-based CLI** (`agent.py`) and a **modern Streamlit web UI** (`agent-ui.py`).

---

## 📁 Project Structure
```
google-adk-and-mcp/
│ agent.py # Terminal interface for multi-turn chat
| agent-ui.py # Streamlit web interface
| .env # Contains ABSOLUTE_PATH to set root directory and the GOOGLE_API_KEY to use Gemini model 
| requirements.txt
```
---

## 🧠 Architecture

Both versions use:
- **Google ADK (`google.genai`, `google.adk`)**
- **MCPToolset** with `@modelcontextprotocol/server-filesystem`
- **LlmAgent** using Gemini 2.0 Flash

### ✳️ `agent.py` – CLI Version
A terminal-based interactive agent:
- Input/output via standard input
- Displays detailed function calls and responses
- Ideal for quickly testing LLM logic and file access

### 🌐 `agent-ui.py` – Streamlit UI Version
A modern, ChatGPT-like web interface:
- Persistent session chat (`st.session_state`)
- Messages displayed above the input
- Centered input box
- Nicely formatted LLM and function responses

---

## ⚙️ Requirements

#### Python
- Python 3.10 or higher is recommended

#### `.env` file
Create a `.env` file in the project root with the following content:

```env
ABSOLUTE_PATH=/absolute/path/to/your/folder
Make sure the path points to a real, accessible folder (e.g., ~/Documents).

GOOGLE_API_KEY=<YOUR_API_KEY>
```

## 📦 Setup Instructions
1. Clone the repository

```
git clone https://github.com/your-username/google-adk-and-mcp.git
cd google-adk-and-mcp
```

2. Create and activate a virtual environment
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```

---

## 🚀 How to Run
#### CLI Version
```
python agent.py
```
#### Streamlit UI Version
```
streamlit run agent-ui.py
```
Then open your browser at the URL provided (usually http://localhost:8501).

---

## 🧹 Cleanup
To stop the MCP server and free resources, the agent automatically closes the toolset connection when the session ends.

---

## 📌 Notes
Make sure Node.js is installed (npx is required to run the MCP server).

The first execution might download dependencies for the MCP server.

The agent uses gemini-2.0-flash via the Google Generative AI API.