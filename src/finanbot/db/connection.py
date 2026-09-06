from time import sleep

from neo4j import GraphDatabase, Driver, Session

from finanbot.settings import settings


class Neo4jDB:
    def __init__(self, uri: str=settings.neo4j_uri, user: str=settings.neo4j_username, password: str=settings.neo4j_password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

    def is_connected(self) -> bool:
        if not self.driver:
            print("Create Neo4jDB instance first")
            return False

        try:
            self.driver.verify_connectivity()
            return True
        except Exception:
            return False

    def wait_until_available(self, timeout: int = 60, wait: int = 2):
        for _ in range(timeout):
            if self.is_connected():
                return
            sleep(wait)
        raise RuntimeError("Neo4j did not become available within the timeout")

    def session(self) -> Session:
        if not self.driver:
            raise RuntimeError("Neo4j driver is not initialized")

        return self.driver.session()

