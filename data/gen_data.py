from datetime import date, timedelta
from pathlib import Path
import csv
import random
import uuid

from faker import Faker

root = Path(__file__).resolve().parent.parent

fake = Faker("en_IN")
random.seed(42)

OUTPUT_DIR = root / Path("data/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = [
    "Food",
    "Groceries",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Rent",
    "Healthcare",
    "Travel",
    "Education",
]

MERCHANTS = {
    "Swiggy": "Food",
    "Zomato": "Food",
    "Local Restaurant": "Food",

    "BigBasket": "Groceries",
    "Reliance Fresh": "Groceries",
    "Local Grocery": "Groceries",

    "Uber": "Transport",
    "Ola": "Transport",
    "BMTC": "Transport",

    "Amazon": "Shopping",
    "Flipkart": "Shopping",
    "Myntra": "Shopping",

    "Netflix": "Entertainment",
    "Spotify": "Entertainment",
    "BookMyShow": "Entertainment",

    "Airtel": "Bills",
    "Electricity Board": "Bills",

    "Apollo Pharmacy": "Healthcare",
    "Local Clinic": "Healthcare",
}


def generate_accounts():
    return [
        {
            "account_id": "ACC001",
            "name": "Savings Account",
            "type": "savings",
            "bank": "HDFC Bank",
        },
        {
            "account_id": "ACC002",
            "name": "Credit Card",
            "type": "credit_card",
            "bank": "HDFC Bank",
        },
    ]


def generate_transactions(accounts):
    transactions = []

    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 31)

    current = start_date
    balance = 50000

    while current <= end_date:
        # Monthly salary
        if current.day == 1:
            amount = 70000
            balance += amount

            transactions.append({
                "transaction_id": str(uuid.uuid4()),
                "account_id": "ACC001",
                "date": current,
                "description": "Monthly Salary",
                "merchant": "Employer",
                "category": "Income",
                "type": "income",
                "amount": amount,
                "balance_after": balance,
            })

        # Monthly rent
        if current.day == 5:
            amount = 15000
            balance -= amount

            transactions.append({
                "transaction_id": str(uuid.uuid4()),
                "account_id": "ACC001",
                "date": current,
                "description": "Monthly Rent",
                "merchant": "Landlord",
                "category": "Rent",
                "type": "expense",
                "amount": amount,
                "balance_after": balance,
            })

        # Random daily expenses
        if random.random() < 0.65:
            merchant = random.choice(list(MERCHANTS))
            category = MERCHANTS[merchant]

            if category == "Food":
                amount = random.randint(150, 800)
            elif category == "Groceries":
                amount = random.randint(500, 3000)
            elif category == "Transport":
                amount = random.randint(100, 700)
            elif category == "Shopping":
                amount = random.randint(500, 5000)
            elif category == "Entertainment":
                amount = random.randint(100, 1000)
            elif category == "Bills":
                amount = random.randint(500, 3000)
            else:
                amount = random.randint(200, 2000)

            balance -= amount

            transactions.append({
                "transaction_id": str(uuid.uuid4()),
                "account_id": random.choice(["ACC001", "ACC002"]),
                "date": current,
                "description": f"Payment at {merchant}",
                "merchant": merchant,
                "category": category,
                "type": "expense",
                "amount": amount,
                "balance_after": balance,
            })

        current += timedelta(days=1)

    return transactions


def write_csv(filename, rows):
    if not rows:
        return

    path = OUTPUT_DIR / filename

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main():
    accounts = generate_accounts()
    transactions = generate_transactions(accounts)

    write_csv("accounts.csv", accounts)
    write_csv("transactions.csv", transactions)

    print(f"Generated {len(transactions)} transactions.")


if __name__ == "__main__":
    main()
