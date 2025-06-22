import os
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters

class FilesystemAgent:
    """Encapsulates MCP Filesystem Agent lifecycle and interactions."""

    def __init__(self, absolute_path: str):
        self.absolute_path = absolute_path
        self.toolset = None
        self.agent = None
        self.runner = None
        self.session = None

    async def start(self):
        """Initialize MCP Toolset, LLM Agent, session and runner."""
        self.toolset = MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@modelcontextprotocol/server-filesystem", self.absolute_path],
                ),
                timeout=20.0,
            )
        )

        tools = await self.toolset.get_tools()

        self.agent = LlmAgent(
            model="gemini-2.0-flash",
            name="filesystem_assistant",
            instruction="Assist the user in navigating and managing their local files. Maintain context across messages.",
            tools=tools,
        )

        session_service = InMemorySessionService()
        artifact_service = InMemoryArtifactService()

        self.session = await session_service.create_session(
            state={"current_directory": self.absolute_path},
            app_name="mcp_filesystem_app",
            user_id="user_fs",
        )

        self.runner = Runner(
            app_name="mcp_filesystem_app",
            agent=self.agent,
            artifact_service=artifact_service,
            session_service=session_service,
        )

    async def ask(self, user_input: str) -> str:
        """Send user input to the agent and return the response."""
        content = types.Content(role="user", parts=[types.Part(text=user_input)])
        response_texts = []

        async for event in self.runner.run_async(
            session_id=self.session.id,
            user_id=self.session.user_id,
            new_message=content,
        ):
            response_texts.append(self._extract_text_from_event(event))

        return "\n".join(filter(None, response_texts))

    async def shutdown(self):
        """Clean shutdown of the MCP Toolset."""
        if self.toolset:
            try:
                await self.toolset.close()
            except Exception as e:
                print(f"Warning during shutdown: {e}")
            self.toolset = None
            self.agent = None
            self.runner = None
            self.session = None

    def _extract_text_from_event(self, event) -> str:
        """Helper to extract readable text from MCP streamed events."""
        texts = []
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    texts.append(part.text)
                elif part.function_call:
                    fc = part.function_call
                    texts.append(f"[Function Call] name: {fc.name}, args: {fc.args}")
                elif getattr(part, "function_response", None):
                    fr = part.function_response
                    if fr.response:
                        texts.append(f"[Function Response] id: {fr.id}, name: {fr.name}")
                        if hasattr(fr.response, "content"):
                            for c in fr.response.content:
                                if hasattr(c, "text"):
                                    texts.append(f"  - {c.text}")
                                else:
                                    texts.append("  - (no text)")
                    else:
                        texts.append("[Function Response] No response content")
        return "\n".join(texts) if texts else "<no text>"
