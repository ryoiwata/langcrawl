#!/bin/bash
# obsynapse Environment Setup Script
# This script creates a conda environment with all dependencies needed for the obsynapse project

# Deactivate any currently active conda environment
conda deactivate

# Create conda environment with Python 3.12 (compatible with DBT)
# Using local path ./langcrawl instead of global environment
conda create -p ./envs/langcrawl python=3.12 --yes

# Activate the newly created environment
conda activate ./envs/langcrawl

# python-dotenv: Environment variable management
# Used for loading API keys and configuration from .env files
conda install conda-forge::python-dotenv --yes

# langchain: Framework for building LLM applications
# Used for text splitting (MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter)
# and integration with vector stores for the hierarchical chunking pipeline
conda install conda-forge::langchain --yes

# langgraph: Library for building stateful, multi-actor applications with LLMs
# Used for orchestrating the flashcard generation workflow (Generator-Critic loop)
# and managing state transitions in the Agentic Forge pipeline
conda install conda-forge::langgraph --yes

# langchain-openai: OpenAI integration for LangChain
# Provides ChatOpenAI and OpenAIEmbeddings classes for LLM and embedding models
conda install conda-forge::langchain-openai --yes

# langchain-community: Community-maintained LangChain integrations
# Provides document loaders (PyPDFLoader) and other community integrations
conda install conda-forge::langchain-community --yes

# langchain-mcp-adapters: Adapter for integrating Model Context Protocol (MCP) tools with LangChain
# Used for loading MCP server tools (e.g., Firecrawl scraping tools) into LangChain-compatible format
# Enables agents to use MCP tools via the load_mcp_tools function
conda install conda-forge::langchain-mcp-adapters --yes