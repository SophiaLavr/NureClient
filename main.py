import tkinter as tk
from client import Client

if __name__ == "__main__":
    root = tk.Tk()
    client = Client(root)
    root.mainloop()
