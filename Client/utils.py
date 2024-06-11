import tkinter as tk

def load_conversation(client, event):
    selection = client.user_list.curselection()
    if selection:
        client.current_chat = client.user_list.get(selection[0])
        display_messages(client, client.current_chat)

def process_message(client, message_data):
    message_type = message_data.get("type")
    if message_type == "message":
        sender = message_data["from"]
        recipient = message_data["to"]
        text = message_data["text"]

        client.messages.append(message_data)

        if sender not in client.conversations:
            client.conversations[sender] = []
        if recipient not in client.conversations:
            client.conversations[recipient] = []

        if client.username == recipient:
            client.conversations[sender].append(message_data)
        else:
            client.conversations[recipient].append(message_data)

        if client.current_chat == sender or client.current_chat == recipient:
            display_messages(client, client.current_chat)
    elif message_type == "user_list":
        client.connected_users = message_data["users"]
        update_user_list(client)

def search_users(client, event):
    search_term = client.search_entry.get().lower()
    client.user_list.delete(0, tk.END)
    for user in client.connected_users:
        if search_term in user.lower():
            client.user_list.insert(tk.END, user)



