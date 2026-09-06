from .models import model

from .db.connection import Neo4jDB
from .db.migrate import migrate
from .db.seed import seed_if_needed

db = Neo4jDB()

def setup_db() -> bool:
    try:
        db.wait_until_available()
    except RuntimeError:
        return False

    migrate(db)
    seed_if_needed(db)

    return True

def cleanup_db():
    db.close()

def main():
    setup_db()

    try:
        # agent setup
        result = model.invoke(
            "Hello! Who are you? Briefly introudce yourself"
        )
        print(result.content)
    except Exception as e:
        print("Got some exception!", e)
    finally:
        cleanup_db()


if __name__ == '__main__':
    main()
