---
name: analyze-spending
description: Analyze spending by category, merchant, account, or time period.
---

# Analyze Spending

Use this skill when the user asks about spending patterns or wants to
understand where money is being spent.

## Responsibilities

- Retrieve the necessary data from Neo4j using the MCP tools.
- Summarize spending according to the user's request.
- Highlight notable trends and outliers.
- Base every conclusion on retrieved data.

## Do not

- Invent transactions.
- Estimate missing values.
- Perform writes to the database.
