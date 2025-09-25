import os
import pandas as pd
from faker import Faker
import random

# ------------------------------
# 1. Setup
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

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

    faq_data.append({
        "question": question,
        "answer": answer
    })

# ------------------------------
# 3. Save to CSV
# ------------------------------
faq_df = pd.DataFrame(faq_data)
faq_csv_path = os.path.join(DATA_DIR, "dummy_faq.csv")
faq_df.to_csv(faq_csv_path, index=False)
print(f"dummy_faq.csv created successfully at {faq_csv_path}!")
