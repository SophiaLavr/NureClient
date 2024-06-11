import tkinter as tk
from tkinter import Canvas, PhotoImage, Button, messagebox
from pathlib import Path
from gui.utils_ui import PlaceholderEntry

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./build/assets1/Authorizationframe")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_image(image_name):
    try:
        return PhotoImage(file=relative_to_assets(image_name))
    except Exception as e:
        print(f"Error loading image {image_name}: {e}")
        return None

def setup_login_screen(client):
    client.root.title("Login")
    client.root.geometry("877x537")
    client.root.resizable(False, False)

    canvas = Canvas(
        client.root,
        bg="#FFFFFF",
        height=537,
        width=877,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Adding gradient
    for i in range(0, 537):
        color = "#%02x%02x%02x" % (
            64 + i * (233 - 64) // 537, 65 + i * (102 - 65) // 537, 84 + i * (110 - 84) // 537)
        canvas.create_line(0, i, 398, i, fill=color)

    # Adding text on the gradient
    canvas.create_text(
        19.0, 22.0,
        anchor="nw",
        text="by Lavrynenko",
        fill="#FFFFFF",
        font=("Inter Black", 32 * -1)
    )

    canvas.create_text(
        19.0, 73.0,
        anchor="nw",
        text="Kharkiv National University of Radio Electronics\n",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    # Load and place the image
    client.image = load_image("image_1.png")  # Ensure you have the image.png in the correct path
    canvas.create_image(199, 330, image=client.image)

    # Adding title
    canvas.create_text(
        422.0, 93.0,
        anchor="nw",
        text="Авторизація",
        fill="#44454A",
        font=("Inter ExtraBold", 40 * -1)
    )

    # Entry for IP address
    client.entry_ip_bg = load_image("entry_1.png")
    canvas.create_image(581.5, 180, image=client.entry_ip_bg)

    client.server_ip_entry = PlaceholderEntry(
        client.root,
        placeholder="IP-адреса",
        color='grey',
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    client.server_ip_entry.place(x=430, y=162, width=303, height=33)

    # Entry for username
    client.entry_username_bg = load_image("entry_1.png")
    canvas.create_image(581.5, 240, image=client.entry_username_bg)

    client.username_entry = PlaceholderEntry(
        client.root,
        placeholder="Ім'я користувача",
        color='grey',
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    client.username_entry.place(x=430, y=222, width=303, height=33)

    # Entry for password
    client.entry_password_bg = load_image("entry_1.png")
    canvas.create_image(581.5, 300, image=client.entry_password_bg)

    client.password_entry = PlaceholderEntry(
        client.root,
        placeholder="Пароль",
        color='grey',
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    client.password_entry.place(x=430, y=282, width=303, height=33)

    # Button for login
    login_button = Button(
        client.root,
        text="Увійти",
        borderwidth=0,
        highlightthickness=0,
        command=client.connect_to_server,
        relief="flat",
        bg="#DC0E2D",
        fg="#FFFFFF",
        font=("Inter", 16, "bold")
    )
    login_button.place(x=430, y=340, width=303, height=52)

    # Registration link
    canvas.create_text(
        422.0, 445.0,
        anchor="nw",
        text="Для створення аккаунту ",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        600.0, 445.0,
        anchor="nw",
        text="зареєструйтесь",
        fill="#DC0E2D",
        font=("Inter", 16 * -1),
        tags="register"
    )
    canvas.tag_bind("register", "<Button-1>", lambda event: setup_register_screen(client))

    client.root.mainloop()

def setup_register_screen(client):
    client.root.title("Register")
    for widget in client.root.winfo_children():
        widget.destroy()

    client.root.geometry("877x537")
    client.root.resizable(False, False)

    canvas = Canvas(
        client.root,
        bg="#FFFFFF",
        height=537,
        width=877,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Adding gradient
    for i in range(0, 537):
        color = "#%02x%02x%02x" % (
            64 + i * (233 - 64) // 537, 65 + i * (102 - 65) // 537, 84 + i * (110 - 84) // 537)
        canvas.create_line(0, i, 398, i, fill=color)

    # Adding text on the gradient
    canvas.create_text(
        19.0, 22.0,
        anchor="nw",
        text="by Lavrynenko",
        fill="#FFFFFF",
        font=("Inter Black", 32 * -1)
    )

    canvas.create_text(
        19.0, 73.0,
        anchor="nw",
        text="Kharkiv National University of Radio Electronics\n",
        fill="#FFFFFF",
        font=("Inter", 15 * -1)
    )

    # Load and place the image
    client.image2 = load_image("image_1.png")  # Ensure you have the image.png in the correct path
    canvas.create_image(199, 330, image=client.image2)

    # Adding title
    canvas.create_text(
        422.0, 93.0,
        anchor="nw",
        text="Реєстрація",
        fill="#44454A",
        font=("Inter ExtraBold", 40 * -1)
    )

    # Entry for IP address
    client.entry_ip_bg2 = load_image("entry_2.png")
    canvas.create_image(581.5, 180, image=client.entry_ip_bg2)

    client.server_ip_entry = PlaceholderEntry(
        client.root,
        placeholder="IP-адреса",
        color='grey',
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    client.server_ip_entry.place(x=430, y=162, width=303, height=33)

    # Entry for username
    client.entry_username_bg2 = load_image("entry_2.png")
    canvas.create_image(581.5, 240, image=client.entry_username_bg2)

    client.username_entry = PlaceholderEntry(
        client.root,
        placeholder="Ім'я користувача",
        color='grey',
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    client.username_entry.place(x=430, y=222, width=303, height=33)

    # Entry for password
    client.entry_password_bg2 = load_image("entry_2.png")
    canvas.create_image(581.5, 300, image=client.entry_password_bg2)

    client.password_entry = PlaceholderEntry(
        client.root,
        placeholder="Пароль",
        color='grey',
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0,
        show="*"
    )
    client.password_entry.place(x=430, y=282, width=303, height=33)

    # Button for register
    register_button = Button(
        client.root,
        text="Зареєструватись",
        borderwidth=0,
        highlightthickness=0,
        command=client.register_on_server,
        relief="flat",
        bg="#DC0E2D",
        fg="#FFFFFF",
        font=("Inter", 16, "bold")
    )
    register_button.place(x=430, y=340, width=303, height=52)

    # Back to login link
    canvas.create_text(
        422.0, 445.0,
        anchor="nw",
        text="Повернутись до ",
        fill="#000000",
        font=("Inter", 16 * -1)
    )

    canvas.create_text(
        550.0, 445.0,
        anchor="nw",
        text="авторизації",
        fill="#DC0E2D",
        font=("Inter", 16 * -1),
        tags="login"
    )
    canvas.tag_bind("login", "<Button-1>", lambda event: setup_login_screen(client))
