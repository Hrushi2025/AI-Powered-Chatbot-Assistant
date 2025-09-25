import logging

logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_query(user_id, query, response):
    logging.info(f"User: {user_id} | Query: {query} | Response: {response}")
