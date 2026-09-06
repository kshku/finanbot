from langchain.mcp import MCPAdapter

from langchain_quickjs import CodeInterpreterMiddleware

from deepagents import create_deep_agent, FilesystemPermission
from deepagents.backends import StateBackend, FilesystemBackend, CompositeBackend

from .settings import settings

from .models import model

from pathlib import Path


ref_dir = Path(__file__).parent / "agent"

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
You are FinanBot, an AI personal finance assistant.

Your primary responsibility is helping users understand, analyze, and explore
their financial data stored in Neo4j.

Capabilities include:
- Spending analysis
- Income and expense summaries
- Account summaries
- Transaction lookup
- Financial trends
- Budget analysis
- Merchant and category analysis
- Charts and visualizations

Use the Neo4j MCP tools whenever information must be retrieved from the
financial graph.

Inspect the schema when necessary before generating Cypher.

Only execute read-only operations through the MCP tools.

Never fabricate financial information.
If information is unavailable, clearly say so.

When presenting numerical results:
- Explain how they were computed.
- Mention assumptions if any.
- Distinguish observations from recommendations.

You may answer general personal-finance questions (budgeting, investing,
saving, taxation concepts, financial literacy), but make it clear when your
answer is educational rather than based on the user's data.

Refuse requests that are unrelated to personal finance or financial data.
Politely explain that FinanBot is specialized for finance and cannot assist
with unrelated domains such as programming, creative writing, general
knowledge, or system administration.
"""

backend = CompositeBackend(
    default=StateBackend(),
    routes={
        "/ref/": FilesystemBackend(
            root_dir=str(ref_dir),
            virtual_mode=True,
        ),
    },
)

permissions = [
    FilesystemPermission(
        operations=["write"],
        paths=["/ref/**"],
        mode="deny",
    ),
]


async def get_agent():
    async with MCPAdapter(mcp_config) as adapter:
        tools = await adapter.list_tools()

        return create_deep_agent(
            model=model,
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            middleware=[CodeInterpreterMiddleware(ptc=tools)],
            backend=backend,
            permissions=permissions,
            skills=["/ref/skills"],
            memory=["/ref/AGENTS.md"],
            name="Finanbot",
        )
