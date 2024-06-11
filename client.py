import socket
import json
import textwrap
import threading
import tkinter as tk
from tkinter import messagebox
from gui.authorization import setup_login_screen, setup_register_screen
from gui.chat import setup_chat_screen
from uuid import uuid4  # To generate unique message IDs


class Client:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.username = None
        self.server_ip = None
        self.client_socket = None
        self.messages = []
        self.conversations = {}
        self.connected_users = []
        self.current_chat = None

        setup_login_screen(self)

    def display_messages(self, chat_with):
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete("all")
        if chat_with in self.conversations:
            y_offset = 20
            for message in self.conversations[chat_with]:
                text = message['text']
                sender = message['from']
                recipient = message['to']

                wrapped_text = textwrap.fill(text, width=40)
                text_lines = wrapped_text.split('\n')
                text_height = len(text_lines) * 30
                text_width = 300

                if sender == self.username:
                    x1, y1, x2, y2 = 660 - text_width - 10, y_offset, 660 - 10, y_offset + text_height + 20
                    self.message_display.create_rectangle(x1, y1, x2, y2, fill="#35384F", outline="")
                    self.message_display.create_text(x2 - 10, y1 + 10, anchor="ne", text=sender, fill="#FFFFFF",
                                                     font=("Inter", 12, "bold"))
                    self.message_display.create_text(x2 - 10, y1 + 30, anchor="ne", text=wrapped_text, fill="#FFFFFF",
                                                     font=("Inter", 12), width=text_width)
                else:
                    x1, y1, x2, y2 = 10, y_offset, 10 + text_width, y_offset + text_height + 20
                    self.message_display.create_rectangle(x1, y1, x2, y2, fill="#35384F", outline="")
                    self.message_display.create_text(x1 + 10, y1 + 10, anchor="nw", text=sender, fill="#FFFFFF",
                                                     font=("Inter", 12, "bold"))
                    self.message_display.create_text(x1 + 10, y1 + 30, anchor="nw", text=wrapped_text, fill="#FFFFFF",
                                                     font=("Inter", 12), width=text_width)

                y_offset += text_height + 40
            self.message_display.config(scrollregion=self.message_display.bbox("all"))
        self.message_display.config(state=tk.DISABLED)

    def connect_to_server(self):
        self.server_ip = self.server_ip_entry.get()
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        if not self.server_ip or not self.username or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, введите IP, имя пользователя и пароль")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, 5555))
        except ConnectionRefusedError:
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу")
            return

        self.client_socket.sendall(
            json.dumps({"type": "login", "username": self.username, "password": password}).encode())
        response = self.client_socket.recv(1024).decode()
        response_data = json.loads(response)

        if response_data["status"] == "ok":
            setup_chat_screen(self)
            threading.Thread(target=self.receive_messages).start()
        else:
            messagebox.showerror("Ошибка", response_data["message"])

    def register_on_server(self):
        self.server_ip = self.server_ip_entry.get()
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        if not self.server_ip or not self.username or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, введите IP, имя пользователя и пароль")
            return

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, 5555))
        except ConnectionRefusedError:
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу")
            return

        self.client_socket.sendall(
            json.dumps({"type": "register", "username": self.username, "password": password}).encode())
        response = self.client_socket.recv(1024).decode()
        response_data = json.loads(response)

        if response_data["status"] == "ok":
            setup_chat_screen(self)
            threading.Thread(target=self.receive_messages).start()
        else:
            messagebox.showerror("Ошибка", response_data["message"])

    def update_user_list(self):
        self.user_list.delete(0, tk.END)
        for user in self.connected_users:
            self.user_list.insert(tk.END, user)

    def receive_messages(self):
        buffer = ""
        while True:
            try:
                buffer += self.client_socket.recv(1024).decode()
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    message_data = json.loads(message)
                    self.process_message(message_data)
            except ConnectionResetError:
                print("Connection was reset. Attempting to reconnect.")
                self.handle_reconnect()
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def handle_reconnect(self):
        try:
            self.client_socket.close()
        except Exception as e:
            print(f"Error closing socket: {e}")

        self.setup_reconnect_screen()

    def setup_reconnect_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        reconnect_label = tk.Label(self.root, text="Attempting to reconnect...", font=("Inter", 20), bg="#202227",
                                   fg="#FFFFFF")
        reconnect_label.pack(expand=True)

        reconnect_button = tk.Button(self.root, text="Reconnect", command=self.connect_to_server, font=("Inter", 16),
                                     bg="#DC0E2D", fg="#FFFFFF")
        reconnect_button.pack(pady=20)

    def process_message(self, message_data):
        message_type = message_data.get("type")
        if message_type == "message":
            if "id" not in message_data:
                print("Invalid message data received:", message_data)
                return
            message_id = message_data.get("id")
            if not any(msg["id"] == message_id for msg in self.messages):
                sender = message_data["from"]
                recipient = message_data["to"]
                text = message_data["text"]

                self.messages.append(message_data)

                if sender not in self.conversations:
                    self.conversations[sender] = []
                if recipient not in self.conversations:
                    self.conversations[recipient] = []

                if self.username == recipient:
                    self.conversations[sender].append(message_data)
                else:
                    self.conversations[recipient].append(message_data)

                if self.current_chat == sender or self.current_chat == recipient:
                    self.display_messages(self.current_chat)
        elif message_type == "user_list":
            self.connected_users = message_data["users"]
            self.update_user_list()
        elif message_type == "conversations":
            for user, messages in message_data["conversations"].items():
                if user not in self.conversations:
                    self.conversations[user] = messages
                else:
                    self.conversations[user].extend(
                        msg for msg in messages if
                        not any(existing_msg["id"] == msg["id"] for existing_msg in self.conversations[user])
                    )
            if self.current_chat:
                self.display_messages(self.current_chat)

    def send_message(self):
        text = self.message_entry.get()
        if text and self.current_chat:
            message_data = {
                "type": "message",
                "id": str(uuid4()),  # Add a unique ID to the message
                "from": self.username,
                "to": self.current_chat,
                "text": text
            }
            self.client_socket.sendall((json.dumps(message_data) + "\n").encode())
            self.message_entry.delete(0, tk.END)
            self.process_message(message_data)

    def search_users(self, event):
        search_term = self.search_entry.get().lower()
        self.user_list.delete(0, tk.END)
        for user in self.connected_users:
            if search_term in user.lower():
                self.user_list.insert(tk.END, user)

    def load_conversation(self, event):
        selection = self.user_list.curselection()
        if selection:
            self.current_chat = self.user_list.get(selection[0])
            self.request_conversation(self.current_chat)
            self.display_messages(self.current_chat)

    def request_conversation(self, user):
        request = {
            "type": "request_conversation",
            "user": user
        }
        try:
            self.client_socket.sendall((json.dumps(request) + "\n").encode())
        except ConnectionResetError:
            print("Connection was reset. Attempting to reconnect.")
            self.handle_reconnect()
