# finanbot

A chat-based CLI that answers questions about your personal finances by querying
a Neo4j financial graph.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker (for the Neo4j database)

## Setup

```bash
cp .env.example .env
# edit .env: model provider/name, provider API key, Neo4j connection
uv sync --extra <provider>
```

`<provider>` is one of `openai`, `gemini`, `anthropic`, `openrouter`, or
`ollama` — pick the one matching your model.

## Run

```bash
docker compose up --build
```

This starts Neo4j and the bot together. A REPL session begins; type `exit` to
quit. The DB is migrated and seeded with sample data automatically on first run.

Alternatively, point `FINANBOT_NEO4J_URI` at an existing Neo4j instance and run:

```bash
uv run python -m finanbot
```

## Configuration

All settings are read from `.env`, prefixed with `FINANBOT_` (see
`.env.example`):

- `FINANBOT_MODEL_PROVIDER` / `FINANBOT_MODEL_NAME` — the chat model to use
- `FINANBOT_NEO4J_URI`, `FINANBOT_NEO4J_USERNAME`, `FINANBOT_NEO4J_PASSWORD`,
  `FINANBOT_NEO4J_DATABASE` — Neo4j connection
- `FINANBOT_NEO4J_READ_ONLY` — enforce read-only queries against the graph

## License

MIT