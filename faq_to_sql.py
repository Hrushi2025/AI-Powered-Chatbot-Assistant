import os
import pandas as pd
import mysql.connector
from faker import Faker
import random

# ------------------------------
# 1. Setup
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "Hrushi@20"
DB_NAME = "ai_chatbot"

fake = Faker()

# ------------------------------
# 2. Generate 100 FAQ entries
# ------------------------------
faq_data = []
categories = ["account", "password", "portfolio", "loan", "market", "transactions"]

for i in range(100):
    category = random.choice(categories)
    if category == "account":
        question = f"How do I update my account details? #{i+1}"
        answer = "You can update your account details from the profile settings page."
    elif category == "password":
        question = f"How do I reset my password? #{i+1}"
        answer = "Go to settings → security → reset password to update your password."
    elif category == "portfolio":
        question = f"How do I check my portfolio balance? #{i+1}"
        answer = "Your portfolio can be viewed from the dashboard → portfolio section."
    elif category == "loan":
        question = f"Am I eligible for a loan? #{i+1}"
        answer = "Loan eligibility is based on your account type and transaction history."
    elif category == "market":
        question = f"What is the current market trend? #{i+1}"
        answer = "The market trend is updated daily; check the market section for details."
    else:  # transactions
        question = f"How can I view my past transactions? #{i+1}"
        answer = "All your transactions are available under dashboard → transactions."

    faq_data.append({"question": question, "answer": answer})

faq_df = pd.DataFrame(faq_data)
faq_csv_path = os.path.join(DATA_DIR, "dummy_faq.csv")
faq_df.to_csv(faq_csv_path, index=False)
print(f"dummy_faq.csv created successfully at {faq_csv_path}!")

# ------------------------------
# 3. Connect to MySQL
# ------------------------------
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# ------------------------------
# 4. Create Database
# ------------------------------
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")
print(f"Database '{DB_NAME}' ready!")

# ------------------------------
# 5. Create FAQ Table
# ------------------------------
cursor.execute("DROP TABLE IF EXISTS faq")  # Ensure table is recreated
cursor.execute("""
CREATE TABLE faq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(255) NOT NULL,
    answer TEXT NOT NULL
)
""")
print("FAQ table created successfully!")

# ------------------------------
# 6. Load FAQ CSV into MySQL
# ------------------------------
for _, row in faq_df.iterrows():
    cursor.execute("""
    INSERT INTO faq (question, answer)
    VALUES (%s, %s)
    """, (row['question'], row['answer']))

conn.commit()
print("FAQ data loaded into MySQL successfully!")

cursor.close()
conn.close()
