import asyncio

from .agent import get_agent

from .db.connection import Neo4jDB
from .db.migrate import migrate
from .db.seed import seed_if_needed


db = Neo4jDB()

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

async def run_agent():
    print("Getting the agent")
    agent = await get_agent()

    print("Starting chat loop")
    while True:
        message = input(">>> ")

        if message == "exit":
            break

        result = await agent.ainvoke({
            "messages": [
                {"role": "user", "content": message}
            ]
        })

        print(result["messages"][-1].content)
        print()

def main():
    print("Setting up DB")
    if not setup_db():
        return

    try:
        asyncio.run(run_agent())
    except Exception as e:
        print("Got some exception!", str(e))
    finally:
        cleanup_db()


if __name__ == '__main__':
    main()
