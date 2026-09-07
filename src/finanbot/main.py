import asyncio

from .agent import get_agent

from .db.connection import Neo4jDB
from .db.migrate import migrate
from .db.seed import seed_if_needed


db = Neo4jDB()
config = {
    "configurable": {
        "thread_id": "finanbot-cli"
    }
}

def setup_db() -> bool:
    try:
        db.wait_until_available()
    except RuntimeError as e:
        print(str(e))
        return False

    migrate(db)
    seed_if_needed(db)

    return True

def cleanup_db():
    db.close()

async def chat():
    agent = await get_agent()

    while True:
        message = input(">>> ")

        if message == "exit":
            break

        print()

        async for event in agent.astream_events(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            },
            version="v2",
            config=config,
        ):
            event_type = event["event"]

            match event_type:
                case "on_chat_model_start":
                    print("🤖 LLM")

                case "on_chat_model_stream":
                    chunk = event["data"]["chunk"]

                    # Normal assistant response
                    if chunk.content:
                        print(chunk.content, end="", flush=True)

                    # Reasoning / thinking exposed by the provider
                    reasoning = getattr(chunk, "reasoning_content", None)

                    if reasoning:
                        print(
                            f"\n💭 {reasoning}",
                            end="",
                            flush=True,
                        )

                case "on_chat_model_end":
                    print("\n")

                case "on_tool_start":
                    print(f"\n🛠 Tool: {event['name']}")
                    print("Input:")
                    print(event["data"]["input"])

                case "on_tool_end":
                    print(f"✅ Tool Finished: {event['name']}")
                    print("Output:")
                    print(event["data"]["output"])
                    print()

                case "on_chain_error":
                    print("❌ Error")
                    print(event["data"])

        print()

def main():
    print("Setting up DB")
    if not setup_db():
        return

    try:
        asyncio.run(chat())
    except Exception as e:
        print("Got some exception!", str(e))
    finally:
        cleanup_db()


if __name__ == '__main__':
    main()
