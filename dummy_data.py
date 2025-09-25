import os
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# ------------------------------
# 1. Create Project Folders
# ------------------------------
folders = [
    "data",
    "models",
    "services",
    "api",
    "db",
    "frontend"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
print("Folders created successfully!")

# ------------------------------
# 2. Generate Dummy Users
# ------------------------------
fake = Faker()
num_users = 100

users_data = []
for i in range(num_users):
    users_data.append({
        "user_id": f"U{i+1:03d}",
        "name": fake.name(),
        "email": fake.email(),
        "account_type": random.choice(["basic", "premium"]),
        "registration_date": fake.date_between(start_date='-2y', end_date='today')
    })

users_df = pd.DataFrame(users_data)
users_df.to_csv("data/dummy_users.csv", index=False)
print("dummy_users.csv created!")

# ------------------------------
# 3. Generate Dummy Portfolio
# ------------------------------
assets = ["gold", "silver", "bitcoin", "ethereum", "stocks"]
portfolio_data = []
for i in range(num_users):
    portfolio_data.append({
        "user_id": f"U{i+1:03d}",
        "asset_type": random.choice(assets),
        "quantity": round(random.uniform(0.5, 100), 2),
        "last_updated": fake.date_between(start_date='-1y', end_date='today')
    })

portfolio_df = pd.DataFrame(portfolio_data)
portfolio_df.to_csv("data/dummy_portfolio.csv", index=False)
print("dummy_portfolio.csv created!")

# ------------------------------
# 4. Generate Dummy Transactions
# ------------------------------
transactions_data = []
for i in range(100):
    transactions_data.append({
        "transaction_id": f"T{i+1:04d}",
        "user_id": f"U{random.randint(1,num_users):03d}",
        "transaction_type": random.choice(["buy", "sell", "deposit", "withdraw"]),
        "amount": round(random.uniform(10, 5000), 2),
        "date": fake.date_between(start_date='-1y', end_date='today'),
        "description": fake.sentence(nb_words=6)
    })

transactions_df = pd.DataFrame(transactions_data)
transactions_df.to_csv("data/dummy_transactions.csv", index=False)
print("dummy_transactions.csv created!")

# ------------------------------
# 5. Generate Dummy FAQ (100 rows)
# ------------------------------
faq_templates = [
    ("How do I reset my password?", "To reset your password, go to settings → security → reset password."),
    ("How to check account statement?", "You can download your account statement from the dashboard → statements."),
    ("Am I eligible for a loan?", "You are eligible for a loan if your account is active for more than 6 months."),
    ("How to contact support?", "You can contact support via email support@example.com or call 1800-123-456."),
    ("How to change email?", "Go to settings → account → change email to update your email address."),
    ("How to upgrade account?", "Go to settings → subscription → upgrade to premium."),
    ("How to deposit funds?", "Use the deposit option in your wallet dashboard to add funds."),
    ("How to withdraw funds?", "Use the withdraw option in your wallet dashboard to transfer money to your bank."),
    ("How to invest in bitcoin?", "Go to the market section → bitcoin → buy or sell based on your choice."),
    ("How to view portfolio?", "Go to your portfolio section to see your assets and quantities."),
]

faq_data = []
for i in range(100):
    template = random.choice(faq_templates)
    faq_data.append({
        "question": template[0],
        "response": template[1]
    })

faq_df = pd.DataFrame(faq_data)
faq_df.to_csv("data/dummy_faq.csv", index=False)
print("dummy_faq.csv created with 100 rows!")
