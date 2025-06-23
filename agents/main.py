import asyncio
import os
from dotenv import load_dotenv
from filesystem_agent import FilesystemAgent  # Make sure the import path is correct

# Load environment variables from .env file
load_dotenv()
absolute_path = os.environ.get("ABSOLUTE_PATH")


async def async_main():
    """Run the Filesystem Agent in interactive multi-turn mode."""
    
    if not absolute_path:
        print("ERROR: ABSOLUTE_PATH environment variable is not defined.")
        return

    agent = FilesystemAgent(absolute_path)

    try:
        await agent.start()
        print("Filesystem Agent is running. Type 'exit' to quit.")

        while True:
            user_input = input("\nYou: ")
            if user_input.strip().lower() in ("exit", "quit"):
                break

            response = await agent.ask(user_input)
            print(f"\nAssistant:\n{response}\n---")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Shutting down agent and MCP server...")
        await agent.shutdown()
        print("Cleanup completed.")


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"Fatal error: {e}")
