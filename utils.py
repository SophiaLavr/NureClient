import json
import socket

def connect_to_server(server_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, port))
        return client_socket
    except ConnectionRefusedError:
        return None

def handle_reconnect(client_socket):
    try:
        client_socket.close()
    except Exception as e:
        print(f"Помилка закриття сокета: {e}")

def send_json_data(sock, data):
    try:
        sock.sendall(json.dumps(data).encode())
    except Exception as e:
        print(f"Помилка відправки даних: {e}")

def receive_json_data(sock):
    try:
        data = sock.recv(1024).decode()
        return json.loads(data)
    except Exception as e:
        print(f"Помилка отримання даних: {e}")
        return None

def process_message(messages, conversations, message_data, username):
    message_type = message_data.get("type")
    if message_type == "message":
        if "id" not in message_data:
            print("Отримано невірні дані повідомлення:", message_data)
            return messages, conversations
        message_id = message_data["id"]
        if not any(msg["id"] == message_id for msg in messages):
            sender = message_data["from"]
            recipient = message_data["to"]
            text = message_data["text"]

            messages.append(message_data)

            if sender not in conversations:
                conversations[sender] = []
            if recipient not in conversations:
                conversations[recipient] = []

            if username == recipient:
                conversations[sender].append(message_data)
            else:
                conversations[recipient].append(message_data)
    elif message_type == "user_list":
        users = message_data["users"]
        conversations[username] = users
    return messages, conversations
