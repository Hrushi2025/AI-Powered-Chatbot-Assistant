conversation_history = {}

def add_to_history(user_id, user_query, bot_response):
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append({"user": user_query, "bot": bot_response})

def get_history(user_id):
    return conversation_history.get(user_id, [])

