from datetime import date, timedelta
import random
import uuid


random.seed(42)


CATEGORIES = [
    "Income",
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


# Merchant -> Category
MERCHANTS = {
    "Employer": "Income",
    "Landlord": "Rent",

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


def generate_people() -> list[dict]:
    return [
        {
            "person_id": "USER001",
            "name": "Alex",
        }
    ]


def generate_accounts(people: list[dict]) -> list[dict]:
    person_ids = [person["person_id"] for person in people]

    return [
        {
            "account_id": "ACC001",
            "person_id": random.choice(person_ids),
            "name": "Savings Account",
            "type": "savings",
            "bank": "HDFC Bank",
        },
        {
            "account_id": "ACC002",
            "person_id": random.choice(person_ids),
            "name": "Credit Card",
            "type": "credit_card",
            "bank": "HDFC Bank",
        },
    ]


def generate_transactions(accounts: list[dict]) -> list[dict]:
    transactions = []

    start_date = date(2020, 1, 1)
    end_date = date(2025, 12, 31)

    current = start_date
    balance = 50_000

    account_ids = [account["account_id"] for account in accounts]
    savings_account = next(account for account in accounts if account["type"] == "savings")

    while current <= end_date:

        # Monthly salary
        if current.day == 1:
            amount = 70_000
            balance += amount

            transactions.append({
                "transaction_id": str(uuid.uuid4()),
                "account_id": savings_account["account_id"],
                "date": current.isoformat(),
                "description": "Monthly Salary",
                "merchant": "Employer",
                "category": "Income",
                "type": "income",
                "amount": amount,
                "balance_after": balance,
            })

        # Monthly rent
        if current.day == 5:
            amount = 15_000
            balance -= amount

            transactions.append({
                "transaction_id": str(uuid.uuid4()),
                "account_id": savings_account["account_id"],
                "date": current.isoformat(),
                "description": "Monthly Rent",
                "merchant": "Landlord",
                "category": "Rent",
                "type": "expense",
                "amount": amount,
                "balance_after": balance,
            })

        # Random daily expenses
        if random.random() < 0.65:
            merchant = random.choice(
                [
                    merchant
                    for merchant, category in MERCHANTS.items()
                    if category not in {"Income", "Rent"}
                ]
            )

            category = MERCHANTS[merchant]

            if category == "Food":
                amount = random.randint(150, 800)

            elif category == "Groceries":
                amount = random.randint(500, 3_000)

            elif category == "Transport":
                amount = random.randint(100, 700)

            elif category == "Shopping":
                amount = random.randint(500, 5_000)

            elif category == "Entertainment":
                amount = random.randint(100, 1_000)

            elif category == "Bills":
                amount = random.randint(500, 3_000)

            elif category == "Healthcare":
                amount = random.randint(200, 2_000)

            elif category == "Travel":
                amount = random.randint(1_000, 10_000)

            elif category == "Education":
                amount = random.randint(500, 5_000)

            else:
                amount = random.randint(200, 2_000)

            balance -= amount

            transactions.append({
                "transaction_id": str(uuid.uuid4()),
                "account_id": random.choice(account_ids),
                "date": current.isoformat(),
                "description": f"Payment at {merchant}",
                "merchant": merchant,
                "category": category,
                "type": "expense",
                "amount": amount,
                "balance_after": balance,
            })

        current += timedelta(days=1)

    return transactions
