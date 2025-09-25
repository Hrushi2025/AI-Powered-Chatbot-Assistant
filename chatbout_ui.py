import tkinter as tk
from tkinter import scrolledtext
import requests
import threading
import subprocess
import sys
import os
import time

# ------------------------------
# 1. Start FastAPI server in background
# ------------------------------
def start_server():
    # Absolute path to chatbot_api.py (one level up from frontend/)
    server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chatbot_api.py"))

    # Start FastAPI server in a subprocess
    subprocess.run([sys.executable, server_path])

# Run server in a separate thread to avoid blocking GUI
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Wait a few seconds for the server to start
time.sleep(3)

# ------------------------------
# 2. GUI setup
# ------------------------------
root = tk.Tk()
root.title("AI-Powered Chatbot Assistant")
root.geometry("600x500")

# Chat display
chat_display = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# User input
user_input = tk.Entry(root, width=80)
user_input.pack(padx=10, pady=(0,10), side=tk.LEFT, expand=True, fill=tk.X)

# Send button
def send_message():
    query = user_input.get().strip()
    if not query:
        return

    # Display user query
    chat_display.config(state='normal')
    chat_display.insert(tk.END, f"You: {query}\n")
    chat_display.config(state='disabled')
    chat_display.yview(tk.END)

    user_input.delete(0, tk.END)

    # Send to FastAPI server
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"user_id": "U001", "query": query}
        )
        answer = response.json().get("response", "No response from server.")
    except Exception as e:
        answer = f"Error connecting to server: {e}"

    # Display bot response
    chat_display.config(state='normal')
    chat_display.insert(tk.END, f"Bot: {answer}\n\n")
    chat_display.config(state='disabled')
    chat_display.yview(tk.END)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=10, pady=(0,10), side=tk.RIGHT)

# Enter key binding
def on_enter(event):
    send_message()

user_input.bind("<Return>", on_enter)

# ------------------------------
# 3. Run GUI
# ------------------------------
root.mainloop()
