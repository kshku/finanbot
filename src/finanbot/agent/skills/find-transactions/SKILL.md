---
name: find-transactions
description: Search and retrieve specific transactions using dates, merchants, categories, amounts, or descriptions.
---

# Find Transactions

Use this skill whenever the user wants to locate transactions.

Examples:

- Transactions from Amazon
- Food expenses in January
- Expenses above ₹5000
- Payments to Swiggy
- Transactions between two dates

## Process

1. Translate the request into Cypher.
2. Execute the read query.
3. Return matching transactions.
4. Mention applied filters.
