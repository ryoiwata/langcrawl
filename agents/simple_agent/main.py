"""
Simple LangGraph Agent with Firecrawl MCP Integration.

This script implements an interactive command-line agent that uses LangGraph's
ReAct pattern to provide web scraping, crawling, and data extraction capabilities
via the Firecrawl MCP (Model Context Protocol) server.

The agent connects to a Firecrawl MCP server process, loads available tools,
and provides a conversational interface for users to interact with web scraping
functionality powered by GPT-4o-mini.

Requirements:
    - OPENAI_API_KEY: OpenAI API key for the language model
    - FIRECRAWL_API_KEY: Firecrawl API key for web scraping tools
    - Node.js/npx: Required to run the firecrawl-mcp server

Usage:
    python main.py

    Type your queries at the prompt and 'quit' to exit.
"""

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio
import os

# Load environment variables from .env file (OPENAI_API_KEY, FIRECRAWL_API_KEY)
load_dotenv()

# Initialize the OpenAI language model with deterministic output (temperature=0)
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Configure MCP server parameters for the Firecrawl tool server.
# StdioServerParameters defines how to spawn and communicate with the MCP server
# via standard input/output streams.
server_params = StdioServerParameters(
    command="npx",  # Use npx to run the firecrawl-mcp package
    env={
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY"),  # Pass API key to server
    },
    args=["firecrawl-mcp"]  # The MCP server package to execute
)


async def main() -> None:
    """
    Run the interactive LangGraph agent with Firecrawl MCP tools.

    This function establishes a connection to the Firecrawl MCP server,
    initializes a ReAct agent with the loaded tools, and runs an interactive
    loop that accepts user input and streams agent responses.

    The function performs the following steps:
        1. Spawns the MCP server as a subprocess and establishes stdio communication
        2. Creates an MCP client session and initializes the protocol handshake
        3. Loads available tools from the MCP server into LangChain-compatible format
        4. Creates a ReAct agent that can reason and act using the loaded tools
        5. Runs an interactive loop for user queries until 'quit' is entered

    Returns:
        None

    Raises:
        Exception: Propagates any errors from the agent invocation, which are
            caught and printed in the interactive loop.
    """
    # Establish stdio connection to the MCP server process.
    # stdio_client spawns the server subprocess and returns read/write streams.
    async with stdio_client(server_params) as (read, write):
        # Create an MCP client session using the stdio streams.
        # ClientSession manages the MCP protocol communication.
        async with ClientSession(read, write) as session:
            # Initialize the MCP session - performs protocol handshake with server
            await session.initialize()

            # Load tools from the MCP server and convert them to LangChain tool format.
            # This makes Firecrawl's scraping/crawling capabilities available to the agent.
            tools = await load_mcp_tools(session)

            # Create a ReAct (Reasoning + Acting) agent using LangGraph's prebuilt factory.
            # The agent will use the LLM to reason about tasks and invoke tools as needed.
            agent = create_react_agent(model, tools)

            # Initialize conversation history with a system prompt that defines agent behavior
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can scrape websites, crawl pages, and extract data using Firecrawl tools. Think step by step and use the appropriate tools to help the user."
                }
            ]

            # Display available tools loaded from the MCP server
            print("Available Tools -", *[tool.name for tool in tools])
            print("-" * 60)

            # Main interactive loop - process user queries until 'quit' is entered
            while True:
                user_input = input("\nYou: ")
                if user_input == "quit":
                    print("Goodbye")
                    break

                # Append user message to conversation history (truncate to avoid token limits)
                messages.append({"role": "user", "content": user_input[:175000]})

                try:
                    # Invoke the ReAct agent asynchronously with the full conversation history.
                    # The agent will reason about the query and potentially call MCP tools.
                    agent_response = await agent.ainvoke({"messages": messages})

                    # Extract and display the final response from the agent's message list
                    ai_message = agent_response["messages"][-1].content
                    print("\nAgent:", ai_message)
                except Exception as e:
                    print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())