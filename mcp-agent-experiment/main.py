import asyncio
from textwrap import dedent
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_filesystem_agent(session: ClientSession) -> Agent:
    """
    Create and configure a filesystem agent with MCP tools.

    Args:
        session (ClientSession): The MCP client session.

    Returns:
        Agent: The configured agent.
    """
    # Initialize the MCP toolkit
    mcp_tools = MCPTools(session=session)
    await mcp_tools.initialize()

    # Create an agent with the MCP toolkit
    return Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            api_key='Your Key'),
        tools=[mcp_tools],
        instructions=dedent("""\
            You are an SQL agent.
            - your job is to write sql queries and retrieve the data form the db and give a natural language response 
            \
        """),
        markdown=True,
        show_tool_calls=True,
    )


async def run_agent(message: str) -> None:
    """
    Run the filesystem agent with the given message.

    Args:
        message (str): The message to send to the agent.
    """
    # Initialize the MCP server
    server_params = StdioServerParameters(
        command="uvx",
        args=[
            
            "mcp-sql-server",
            "--db-host",
            "localhost",
            "--db-user",
            "root",
            "--db-password",
            "passwordxxxxx",
            "--db-database",
            "xxxxxx",
           
            
        ],
    )

    # Create a client session to connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            agent = await create_filesystem_agent(session)

            # Run the agent
            await agent.aprint_response(message, stream=True)


# Example usage
if __name__ == "__main__":
    # Basic example - exploring project license
    asyncio.run(run_agent("get a list of all employees"))