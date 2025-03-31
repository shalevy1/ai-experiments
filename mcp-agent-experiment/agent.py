import asyncio
import os
from dotenv import load_dotenv
from textwrap import dedent
from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agno.utils.log import logger
from typing import Optional

# Load environment variables from .env file
load_dotenv()

# Default model ID if not specified in environment variables
DEFAULT_MODEL_ID = "llama-3.3-70b-versatile"


async def db_connection_agent(session: ClientSession, model_id: Optional[str] = None) -> Agent:
    """
    Creates and configures an agent that interacts with an SQL database via MCP.

    Args:
        session (ClientSession): The MCP client session.
        model_id (Optional[str]): The ID of the language model to use. Defaults to DEFAULT_MODEL_ID.

    Returns:
        Agent: The configured agent.

    Raises:
        ValueError: If the GROQ_API_KEY environment variable is not set.
    """
    # Check if GROQ_API_KEY is set
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    # Determine the model ID to use
    model_id_to_use = model_id or os.getenv("MODEL_ID", DEFAULT_MODEL_ID)

    # Initialize the MCP toolkit
    mcp_tools = MCPTools(session=session)
    await mcp_tools.initialize()

    # Create and return the configured agent
    return Agent(
        model=Groq(id=model_id_to_use, api_key=groq_api_key),
        tools=[mcp_tools],
        instructions=dedent(
            """\
            You are an SQL agent.
            - Your job is to write SQL queries and retrieve data from the database.
            - Provide a natural language response based on the query results.
            """
        ),
        markdown=True,
        show_tool_calls=True,
    )


async def run_agent(message: str, model_id: Optional[str] = None) -> RunResponse:
    """
    Runs the agent with the given message and returns the response.

    Args:
        message (str): The message to send to the agent.
        model_id (Optional[str]): The ID of the language model to use. Defaults to DEFAULT_MODEL_ID.

    Returns:
        RunResponse: The agent's response.

    Raises:
        ValueError: If any of the required database environment variables are not set.
        RuntimeError: If there is an error connecting to the MCP server.
    """
    # Check for required database environment variables
    required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    # Configure MCP server parameters
    server_params = StdioServerParameters(
        command="uvx",
        args=[
            "mcp-sql-server",
            "--db-host",
            os.getenv("DB_HOST"),
            "--db-user",
            os.getenv("DB_USER"),
            "--db-password",
            os.getenv("DB_PASSWORD"),
            "--db-database",
            os.getenv("DB_NAME"),
        ],
    )

    # Connect to the MCP server and run the agent
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                agent = await db_connection_agent(session, model_id)
                response = await agent.arun(message)
                return response
    except Exception as e:
        raise RuntimeError(f"Error connecting to MCP server or running agent: {e}") from e


async def main():
    """
    Example usage of the agent.
    """
    try:
        # Run the agent with a sample query
        response = await run_agent("get a list of all employees")
        logger.info(f"Agent Response: {response.content}")
    except ValueError as ve:
        logger.error(f"Configuration error: {ve}")
    except RuntimeError as re:
        logger.error(f"Runtime error: {re}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
