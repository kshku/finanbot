// Person
CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE;


// Account
CREATE CONSTRAINT account_id_unique IF NOT EXISTS
FOR (a:Account)
REQUIRE a.id IS UNIQUE;


// Transaction
CREATE CONSTRAINT transaction_id_unique IF NOT EXISTS
FOR (t:Transaction)
REQUIRE t.id IS UNIQUE;


// Merchant
CREATE CONSTRAINT merchant_name_unique IF NOT EXISTS
FOR (m:Merchant)
REQUIRE m.name IS UNIQUE;


// Category
CREATE CONSTRAINT category_name_unique IF NOT EXISTS
FOR (c:Category)
REQUIRE c.name IS UNIQUE;
