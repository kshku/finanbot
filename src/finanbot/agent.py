from langchain.mcp import MCPAdapter

from langchain_quickjs import CodeInterpreterMiddleware

from deepagents import create_deep_agent
from deepagents import StateBackend


from .settings import settings

from .models import model


mcp_config = {
    "mcpServers": {
        "neo4j": {
            "command": "python",
            "args": ["-m", "neo4j_mcp_server"],
            "env": {
                "NEO4J_URI": settings.neo4j_uri,
                "NEO4J_USERNAME": settings.neo4j_username,
                "NEO4J_PASSWORD": settings.neo4j_password,
                "NEO4J_DATABASE": settings.neo4j_database,
                "NEO4J_READ_ONLY": str(settings.neo4j_read_only).lower(),
                "NEO4J_TELEMETRY": str(settings.neo4j_telemetry).lower(),
            },
        },
    }
}

SYSTEM_PROMPT = """
You are FinanBot, a personal finance assistant who helps to analzye the
financial data to give detailed answers, analysis reports, graphical 
representations for easy explanation.

You have access to the user's financial data through Neo4j.

Use the Neo4j MCP tools whenever the user's question requires
information from the financial graph.

Inspect the schema when necessary and generate appropriate
read-only Cypher queries.

Never invent financial information.
Base financial answers on data retrieved from Neo4j.
"""

backend = StateBackend()


async def get_agent():
    async with MCPAdapter(mcp_config) as adapter:
        tools = await adapter.list_tools()

        return create_deep_agent(
            model=model,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            middleware=[CodeInterpreterMiddleware(ptc=tools)],
            backend=backend,
            #skills=["/skills"],
            #memory=["/AGENTS.md"],
            name="Finanbot",
        )
