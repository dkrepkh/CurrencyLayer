import tkinter as tk
from tkinter import ttk, messagebox

import api_tools
from currency_client import Client

class CurrencySelector:
    def __init__(self, api_key):
        self.client = Client(api_key)
        self.selections = []
        self.primary_currency = None

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Currency Selector")
        self.root.geometry("400x300")

        # Button to select the primary currency
        self.primary_currency_btn = ttk.Button(self.root, text="Select Primary Currency", command=self.select_primary_currency)
        self.primary_currency_btn.pack(pady=20)

        # Button to add another currency (initially hidden)
        self.add_currency_btn = ttk.Button(self.root, text="Add Currency", command=self.add_currency)

        # Button to get currency rates (initially hidden)
        self.submit_btn = ttk.Button(self.root, text="Get Rates", command=self.get_selected_currencies)

        # Assume this is your list of currencies
        self.all_currencies = ["USD", "RUB", "EUR", "GBP", "JPY", "AUD"]

        self.root.mainloop()

    def reset_selections(self):
        self.selections = []
        self.submit_btn.pack_forget()  # Hide the "Get Rates" button
        if self.primary_currency:
            self.add_currency_btn.pack_forget()  # Hide the button to add other currencies
            self.primary_currency = None

    def select_primary_currency(self):
        new_window = tk.Toplevel(self.root)
        listbox = tk.Listbox(new_window, height=10, width=20)

        for currency in self.all_currencies:
            listbox.insert(tk.END, currency)

        listbox.pack(padx=10, pady=10)
        select_btn = ttk.Button(new_window, text="Select", command=lambda: self.set_primary_currency(listbox, new_window))
        select_btn.pack(pady=10)

    def set_primary_currency(self, listbox, window):
        selected = listbox.curselection()
        if selected:
            self.reset_selections()  # Reset all previous selections
            self.primary_currency = self.all_currencies[selected[0]]
            print(f"Primary currency: {self.primary_currency}")
            self.add_currency_btn.pack(pady=20)  # Show the button to add other currencies
        window.destroy()

    def add_currency(self):
        new_window = tk.Toplevel(self.root)
        listbox = tk.Listbox(new_window, height=10, width=20)

        available_currencies = [curr for curr in self.all_currencies if curr != self.primary_currency and curr not in self.selections]
        for currency in available_currencies:
            listbox.insert(tk.END, currency)

        listbox.pack(padx=10, pady=10)
        select_btn = ttk.Button(new_window, text="Select", command=lambda: self.select_additional_currency(listbox, new_window))
        select_btn.pack(pady=10)

    def select_additional_currency(self, listbox, window):
        selected = listbox.curselection()
        if selected:
            available_currencies = [curr for curr in self.all_currencies if curr != self.primary_currency and curr not in self.selections]
            selected_currency = available_currencies[selected[0]]
            self.selections.append(selected_currency)
            print(f"Selected additional currency: {selected_currency}")
            if not self.submit_btn.winfo_ismapped():  # If the "Get Rates" button is not shown yet
                self.submit_btn.pack(pady=10)  # Show the "Get Rates" button
        window.destroy()

    def get_selected_currencies(self):
        if self.primary_currency and self.selections:
            try:
                rates = self.client.get_currencies(self.primary_currency, *self.selections)
                if rates:
                    messagebox.showinfo("Currency Rates", ', '.join([f"{key}: {value}" for key, value in rates.items()]))
                else:
                    messagebox.showerror("Error", "Failed to get currency rates.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please select a primary currency and at least one additional currency.")
