import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
import json
import webbrowser
import sys


class APIKeyDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.valid_keys = self.load_valid_keys()
        super().__init__(parent, "Enter API Key")

    def body(self, master):
        self.label = tk.Label(master, text="Enter your API key:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, width=40)
        self.entry.pack(pady=10)

        self.load_button = tk.Button(master, text="Load Previous Key", command=self.load_key)
        self.load_button.pack(pady=5)

        self.create_key_button = tk.Button(master, text="Create New Key", command=self.create_new_key)
        self.create_key_button.pack(pady=5)

    def validate(self):
        key = self.entry.get().strip()
        if self.is_valid_key(key):
            self.api_key = key
            self.save_valid_key(key)
            return True
        else:
            messagebox.showerror("Error", "API key is invalid. Please try again.")
            return False

    def is_valid_key(self, key):
        try:
            response = requests.get(f"https://api.freecurrencyapi.com/v1/latest?apikey={key}&base_currency=USD")
            return response.status_code == 200
        except Exception as e:
            return False

    def load_valid_keys(self):
        try:
            with open('keys.json', 'r') as file:
                data = json.load(file)
            return data.get("valid_keys", [])
        except FileNotFoundError:
            return []

    def save_valid_key(self, key):
        self.valid_keys.append(key)
        with open('keys.json', 'w') as file:
            json.dump({"valid_keys": self.valid_keys}, file)

    def load_key(self):
        if self.valid_keys:
            key = simpledialog.askstring("Load Key", "Choose a key:", initialvalue=self.valid_keys[-1])
            self.entry.delete(0, tk.END)
            self.entry.insert(0, key)
        else:
            messagebox.showinfo("Information", "No saved keys found.")

    def create_new_key(self):
        webbrowser.open("https://www.freecurrencyapi.com/")

    def on_closing(self):
        if not hasattr(self, "api_key"):
            sys.exit(0)


def get_valid_api_key():
    root = tk.Tk()
    root.withdraw()
    api_key = None

    while not api_key:
        dialog = APIKeyDialog(root)
        api_key = getattr(dialog, "api_key", None)
        root.update()

    root.destroy()
    return api_key





