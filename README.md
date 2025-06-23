# 💬 Google ADK + MCP (Filesystem & Custom Webpage Agents AI)
This project demonstrates the integration of **Google Advanced Developer Kit (ADK)** with the **Model Context Protocol (MCP)** to build conversational AI agents capable of:

✅ Navigating and interacting with the local filesystem
✅ Loading webpages via a custom MCP server exposing ADK tools

- It includes:
- A terminal-based CLI (main.py, servers/main.py)
- A Streamlit Web UI (main-ui.py)

---

## 📁 Project Structure
```
google-adk-and-mcp/
├─ .env                   
├─ requirements.txt
│
├─ agents/
│   ├─ filesystem_agent.py
│   ├─ load_webpage_agent.py
│   ├─ main.py
│   ├─ main-ui.py
│
├─ servers/
│   ├─ main.py
│   ├─ mcp_server.py

```
---

## 🧠 Architecture

Both versions use:
- **Google ADK (`google.genai`, `google.adk`)**
- **MCPToolset** with `@modelcontextprotocol/server-filesystem`
- **LlmAgent** using Gemini 2.0 Flash

---

## ✨ Available Agents

#### 📂 Filesystem Agent  
Interact with your local filesystem conversationally.

- Lists directories  
- Navigates folders  
- Maintains stateful chat  

Two access modes:  
- `main.py`: Terminal chat  
- `main-ui.py`: Streamlit Chat UI  

---

#### 🌐 Load Web Page Agent (Custom MCP Server)  
Leverages a custom Python MCP server (`adk_mcp_server.py`) to expose ADK tools like `load_web_page`.

- MCP server runs locally, communicating via stdin/stdout  
- Agent connects and wraps ADK functions for conversational use  

Access via:  
- `servers/main.py`: Terminal chat interface


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

MCP_SERVER_PATH=/absolute/path/to/mcp_server.py  # Custom MCP Server script
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
python agents/main.py
python -m servers.main 
```
#### Streamlit UI Version
```
streamlit run agents/main-ui.py
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