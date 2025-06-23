import asyncio
import os
from dotenv import load_dotenv
from agents.load_webpages_agent import LoadWebPageAgent 

# Load environment variables from .env file
load_dotenv()
server_script_path = os.environ.get("MCP_SERVER_PATH")

async def async_main():
    """Run the Load Web Page Agent in interactive multi-turn mode."""
    
    if not server_script_path:
        print("ERROR: MCP_SERVER_PATH environment variable is not defined.")
        return

    agent = LoadWebPageAgent(server_script_path)

    try:
        await agent.start()
        print("Load Web Page Agent is running. Type 'exit' to quit.")

        while True:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ("exit", "quit"):
                break

            response = await agent.ask(user_input)
            print(f"\nAssistant:\n{response}\n---")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Shutting down the agent and MCP server...")
        await agent.shutdown()
        print("Cleanup completed.")


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"Fatal error: {e}")
