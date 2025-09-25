import mysql.connector
import pandas as pd
import os

# ------------------------------
# 1. MySQL Connection
# ------------------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "Hrushi@20"  # Change if needed
DB_NAME = "ai_chatbot"

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# ------------------------------
# 2. Create Database
# ------------------------------
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
print(f"Database '{DB_NAME}' created or already exists.")
cursor.execute(f"USE {DB_NAME}")

# ------------------------------
# 3. Create Tables
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    account_type VARCHAR(20),
    registration_date DATE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS portfolio (
    user_id VARCHAR(10),
    asset_type VARCHAR(50),
    quantity DECIMAL(10,2),
    last_updated DATE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(10) PRIMARY KEY,
    user_id VARCHAR(10),
    transaction_type VARCHAR(20),
    amount DECIMAL(10,2),
    date DATE,
    description VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

print("Tables created successfully!")

# ------------------------------
# 4. Load CSV Data
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

portfolio_df = pd.read_csv(os.path.join(DATA_DIR, "dummy_portfolio.csv"))
users_df = pd.read_csv(os.path.join(DATA_DIR, "dummy_users.csv"))
transactions_df = pd.read_csv(os.path.join(DATA_DIR, "dummy_transactions.csv"))

# ------------------------------
# 5. Insert Data into Tables
# ------------------------------
for _, row in users_df.iterrows():
    cursor.execute("""
    INSERT IGNORE INTO users (user_id, name, email, account_type, registration_date)
    VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))

for _, row in portfolio_df.iterrows():
    cursor.execute("""
    INSERT INTO portfolio (user_id, asset_type, quantity, last_updated)
    VALUES (%s, %s, %s, %s)
    """, tuple(row))

for _, row in transactions_df.iterrows():
    cursor.execute("""
    INSERT INTO transactions (transaction_id, user_id, transaction_type, amount, date, description)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
print("CSV data loaded into MySQL successfully!")

# ------------------------------
# 6. Close Connection
# ------------------------------
cursor.close()
conn.close()
