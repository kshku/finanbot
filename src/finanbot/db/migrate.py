from pathlib import Path

from .connection import Neo4jDB


MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def migrate(db: Neo4jDB):
    migrations = sorted(MIGRATIONS_DIR.glob("*.cypher"))

    with db.session() as session:
        for migration in migrations:
            query = migration.read_text()

            statements = [statement.strip() for statement in query.split(";") if statement.strip()]

            for statement in statements:
                session.run(statement)
