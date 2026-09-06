from .gen_data import (
    MERCHANTS,
    CATEGORIES,
    generate_accounts,
    generate_transactions,
    generate_people,
)
from .connection import Neo4jDB

def run_query(db: Neo4jDB, query: str, **kwargs):
    with db.session() as session:
        session.run(query, **kwargs)

def _seed_people(db: Neo4jDB, people: list[dict]):
    query = """
    UNWIND $people as person

    MERGE (p:Person {id: person.person_id})
    SET
        p.name = person.name
    """

    run_query(db, query, people=people)

def _seed_categories(db: Neo4jDB, categories: list[str]):
    query = """
    UNWIND $categories as category

    MERGE (c:Category {name: category})
    """

    run_query(db, query, categories=categories)

def _seed_merchants(db: Neo4jDB, merchants: dict):
    merchants = [
        {"name": name, "category": category}
        for name, category in merchants.items()
    ]

    query = """
    UNWIND $merchants as merchant

    MERGE (m:Merchant {name: merchant.name})
    WITH m, merchant
    MATCH (c:Category {name: merchant.category})
    MERGE (m)-[:IN_CATEGORY]->(c)
    """

    run_query(db, query, merchants=merchants)

def _seed_accounts(db: Neo4jDB, accounts: list[dict]):
    query = """
    UNWIND $accounts as account

    MERGE (a:Account {id: account.account_id})
    SET
        a.name = account.name,
        a.type = account.type,
        a.bank = account.bank

    WITH a, account
    MATCH (p:Person {id: account.person_id})
    MERGE (p)-[:HAS_ACCOUNT]->(a)
    """

    run_query(db, query, accounts=accounts)

def _seed_transactions(db: Neo4jDB, transactions: list[dict]):
    query = """
    UNWIND $transactions as transaction

    MATCH (a:Account {id: transaction.account_id})
    MATCH (m:Merchant {name: transaction.merchant})
    MATCH (c:Category {name: transaction.category})

    MERGE (t:Transaction {id: transaction.transaction_id})
    SET
        t.date = date(transaction.date),
        t.description = transaction.description,
        t.type = transaction.type,
        t.amount = toFloat(transaction.amount),
        t.balance = toFloat(transaction.balance_after)

    MERGE (a)-[:HAS_TRANSACTION]->(t)
    MERGE (t)-[:SPENT_ON]->(m)
    MERGE (t)-[:IN_CATEGORY]->(c)
    """

    run_query(db, query, transactions=transactions)

def seed(db: Neo4jDB):
    people = generate_people()
    accounts = generate_accounts(people)
    transactions = generate_transactions(accounts)

    _seed_people(db, people)
    _seed_categories(db, CATEGORIES)
    _seed_merchants(db, MERCHANTS)
    _seed_accounts(db, accounts)
    _seed_transactions(db, transactions)

def seed_if_needed(db: Neo4jDB):
    query = """
    MATCH (n) RETURN count(n) as count
    """
    with db.session() as session:
        result = session.run(query)
        count = result.single()["count"]

    if count == 0:
        seed(db)
