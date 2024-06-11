from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Listbox, Frame, Scrollbar, VERTICAL, HORIZONTAL
import gui.utils_ui
import tkinter as tk
import textwrap
import json

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_image(image_name):
    try:
        return PhotoImage(file=relative_to_assets(image_name))
    except Exception as e:
        print(f"Error loading image {image_name}: {e}")
        return None

def setup_chat_screen(client):
    client.root.title("Chat")
    client.root.geometry("1085x808")
    client.root.configure(bg="#202227")

    # Clear existing widgets
    for widget in client.root.winfo_children():
        widget.destroy()

    canvas = Canvas(
        client.root,
        bg="#202227",
        height=808,
        width=1085,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        9.0,
        0.0,
        679.0,
        808.0,
        fill="#1A1B21",
        outline="")

    canvas.create_rectangle(
        700.0,
        0.0,
        1099.0,
        825.0,
        fill="#1A1B20",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        549.0,
        767.0,
        image=image_image_1
    )

    client.image = load_image("image_2.png")
    canvas.create_image(773.0, 53.0, image=client.image)

    canvas.create_text(
        818.0,
        43.0,
        anchor="nw",
        text=client.username,
        fill="#FFFFFF",
        font=("Inter Bold", 24 * -1)
    )

    client.message_entry = gui.utils_ui.PlaceholderEntry(
        client.root,
        placeholder="Введіть повідомлення",
        color='grey',
        bd=0,
        bg="#3A3A3A",
        fg="#FFFFFF",
        font=("Inter", 14)
    )
    client.message_entry.place(x=104.0, y=748.0, width=400, height=40)

    send_image = PhotoImage(file=relative_to_assets("image_1.png"))
    client.send_button = tk.Button(client.root, image=send_image, command=client.send_message, bg="#1A1B21", bd=0)
    client.send_button.image = send_image
    client.send_button.place(x=532.0, y=750.0, width=34, height=34)

    client.search_entry = gui.utils_ui.PlaceholderEntry(
        client.root,
        placeholder="Пошук користувачів",
        color='grey',
        bd=0,
        bg="#3A3A3A",
        fg="#FFFFFF",
        font=("Inter", 14)
    )
    client.search_entry.place(x=745.0, y=104.0, width=295, height=40)
    client.search_entry.bind("<KeyRelease>", lambda event: client.search_users(event))

    # Scrollable chat display area
    chat_frame = Frame(client.root, bg="#1A1B21")
    chat_frame.place(x=10, y=10, width=660, height=720)

    scrollbar_v = Scrollbar(chat_frame, orient=VERTICAL)
    scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_h = Scrollbar(chat_frame, orient=HORIZONTAL)
    scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)

    client.message_display = Canvas(chat_frame, bg="#1A1B21", bd=0, highlightthickness=0, yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
    client.message_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar_v.config(command=client.message_display.yview)
    scrollbar_h.config(command=client.message_display.xview)

    client.message_display.bind('<Configure>', lambda e: client.message_display.config(scrollregion=client.message_display.bbox("all")))

    # User list frame
    client.user_list_frame = Canvas(
        client.root,
        bg="#1A1B20",
        height=800,
        width=380,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    client.user_list_frame.place(x=700, y=150)

    # User list
    client.user_list = Listbox(client.root, bg="#1A1B20", fg="#FFFFFF")
    client.user_list.place(x=710, y=200, width=360, height=600)
    client.user_list.bind("<<ListboxSelect>>", lambda event: client.load_conversation(event))

    client.display_messages = lambda chat_with: display_messages(client, chat_with)

    return client.message_entry, client.message_display, client.search_entry, client.user_list

def display_messages(client, chat_with):
    client.message_display.delete("all")
    if chat_with in client.conversations:
        y_offset = 20
        for message in client.conversations[chat_with]:
            text = message['text']
            sender = message['from']
            recipient = message['to']

            wrapped_text = textwrap.fill(text, width=40)
            text_lines = wrapped_text.split('\n')
            text_height = len(text_lines) * 35
            text_width = 350

            if sender == client.username:
                x1, y1, x2, y2 = 660 - text_width - 10, y_offset, 660 - 10, y_offset + text_height + 20
                client.message_display.create_rectangle(x1, y1, x2, y2, fill="#35384F", outline="")
                client.message_display.create_text(x2 - 10, y1 + 10, anchor="ne", text=sender, fill="#FFFFFF", font=("Inter", 12, "bold"))
                client.message_display.create_text(x2 - 10, y1 + 30, anchor="ne", text=wrapped_text, fill="#FFFFFF", font=("Inter", 12), width=text_width)
            else:
                x1, y1, x2, y2 = 10, y_offset, 10 + text_width, y_offset + text_height + 20
                client.message_display.create_rectangle(x1, y1, x2, y2, fill="#35384F", outline="")
                client.message_display.create_text(x1 + 10, y1 + 10, anchor="nw", text=sender, fill="#FFFFFF", font=("Inter", 12, "bold"))
                client.message_display.create_text(x1 + 10, y1 + 30, anchor="nw", text=wrapped_text, fill="#FFFFFF", font=("Inter", 12), width=text_width)

            y_offset += text_height + 40
        client.message_display.config(scrollregion=client.message_display.bbox("all"))

def send_message(client):
    text = client.message_entry.get()
    if text and client.current_chat:
        message_data = {
            "type": "message",
            "from": client.username,
            "to": client.current_chat,
            "text": text
        }
        client.client_socket.sendall((json.dumps(message_data) + "\n").encode())
        client.message_entry.delete(0, tk.END)
        client.process_message(message_data)

