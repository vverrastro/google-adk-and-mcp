import asyncio
import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService  # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

# Load environment variables from .env file
load_dotenv()
absolute_path = os.environ.get("ABSOLUTE_PATH")

# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
    print("Attempting to connect to MCP Filesystem server...")

    # Create an instance of MCPToolset that connects to a local MCP server via stdio
    toolset = MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command='npx', # Use Node.js package runner to start the MCP server
                args=[
                    "-y", # Auto-confirm installation of dependencies
                    "@modelcontextprotocol/server-filesystem", # MCP Filesystem server package
                    absolute_path # Root directory the agent will be allowed to access
                ],
            ),
            timeout=20.0  # Timeout in seconds to wait for the server to respond
        )
    )

    tools = await toolset.get_tools()
    print("MCP Toolset created successfully.")
    return tools, toolset

# --- Step 2: Agent Definition ---
async def get_agent_async():
    tools, toolset = await get_tools_async()
    print(f"Fetched {len(tools)} tools from MCP server.")
    root_agent = LlmAgent(
        model='gemini-2.0-flash',
        name='filesystem_assistant',
        instruction='Assist the user in navigating and managing their local files. Maintain context across messages.',
        tools=tools,
    )
    return root_agent, toolset

# Extracts human-readable text or function-related info from a streamed event
def extract_text_from_event(event):
    texts = []
    if hasattr(event, 'content') and event.content and event.content.parts:
        for part in event.content.parts:
            if part.text:
                texts.append(part.text)
            elif part.function_call:
                fc = part.function_call
                texts.append(f"[Function Call] name: {fc.name}, args: {fc.args}")
            elif getattr(part, 'function_response', None):
                fr = part.function_response
                if fr.response:
                    # Stampa testuale più dettagliata della risposta
                    texts.append(f"[Function Response] id: {fr.id}, name: {fr.name}")
                    if hasattr(fr.response, 'content'):
                        for c in fr.response.content:
                            if hasattr(c, 'text'):
                                texts.append(f"  - {c.text}")
                            else:
                                texts.append(f"  - (no text in this content part)")
                else:
                    texts.append("[Function Response] No response content")
     # Join all collected text lines into a single string, separated by newlines
    return "\n".join(texts) if texts else "<no text>"


async def async_main():
    session_service = InMemorySessionService()
    artifacts_service = InMemoryArtifactService()
    session = await session_service.create_session(
        state={"current_directory": absolute_path}, app_name='mcp_filesystem_app', user_id='user_fs'
    )

    root_agent, toolset = await get_agent_async()
    runner = Runner(
        app_name='mcp_filesystem_app',
        agent=root_agent,
        artifact_service=artifacts_service,
        session_service=session_service,
    )

    print("Running agent in multi-turn mode. Type 'exit' to quit.")
    try:
        while True:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ("exit", "quit"):
                break

            content = types.Content(role='user', parts=[types.Part(text=user_input)])

            events_async = runner.run_async(
                session_id=session.id,
                user_id=session.user_id,
                new_message=content
            )

            async for event in events_async:
                text = extract_text_from_event(event)
                print(f"\nAssistant:\n{text}\n---")

    finally:
        print("Closing MCP server connection...")
        await toolset.close()
        print("Cleanup complete.")


if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")