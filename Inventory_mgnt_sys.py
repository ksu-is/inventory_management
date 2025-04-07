import pandas as pd
import os
import tkinter as tk
from tkinter import messagebox, ttk

INVENTORY_FILE = 'inventory.csv'
COLUMNS = ['ID', 'Name', 'Quantity', 'Price']


class Inventory:
    def __init__(self, filename):
        self.filename = filename
        self.df = self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.filename):
            df = pd.read_csv(self.filename)
            df['Quantity'] = df['Quantity'].astype(int)
            df['Price'] = df['Price'].astype(float)
        else:
            df = pd.DataFrame(columns=COLUMNS)
        return df

    def save_inventory(self):
        self.df.to_csv(self.filename, index=False)

    def get_inventory(self):
        return self.df

    def add_item(self, item_id, name, quantity, price):
        if str(item_id) in self.df['ID'].astype(str).values:
            return "Item ID already exists."
        new_item = pd.DataFrame([[item_id, name, int(quantity), float(price)]], columns=COLUMNS)
        self.df = pd.concat([self.df, new_item], ignore_index=True)
        self.save_inventory()
        return "Item added successfully!"

    def update_item(self, item_id, quantity=None, price=None):
        mask = self.df['ID'].astype(str) == str(item_id)
        if mask.any():
            if quantity is not None:
                self.df.loc[mask, 'Quantity'] = int(quantity)
            if price is not None:
                self.df.loc[mask, 'Price'] = float(price)
            self.save_inventory()
            return "Item updated successfully!"
        return "Item not found."

    def delete_item(self, item_id):
        initial_len = len(self.df)
        self.df = self.df[self.df['ID'].astype(str) != str(item_id)]
        if len(self.df) < initial_len:
            self.save_inventory()
            return "Item deleted successfully!"
        return "Item not found."


class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.inventory = Inventory(INVENTORY_FILE)

        # Table for inventory
        self.tree = ttk.Treeview(root, columns=COLUMNS, show='headings')
        for col in COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Item", command=self.add_item).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update Item", command=self.update_item).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Item", command=self.delete_item).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_inventory).grid(row=0, column=3, padx=5)

        # Load inventory initially
        self.refresh_inventory()

    def refresh_inventory(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row in self.inventory.get_inventory().iterrows():
            self.tree.insert("", "end", values=(row['ID'], row['Name'], row['Quantity'], row['Price']))

    def add_item(self):
        self.show_item_window("Add Item", self.inventory.add_item)

    def update_item(self):
        self.show_item_window("Update Item", self.inventory.update_item, update=True)

    def delete_item(self):
        item_id = self.get_selected_item_id()
        if item_id:
            message = self.inventory.delete_item(item_id)
            messagebox.showinfo("Delete Item", message)
            self.refresh_inventory()

    def get_selected_item_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item)['values'][0]
        messagebox.showwarning("Warning", "Please select an item.")
        return None

    def show_item_window(self, title, action, update=False):
        window = tk.Toplevel(self.root)
        window.title(title)

        tk.Label(window, text="Item ID:").grid(row=0, column=0)
        entry_id = tk.Entry(window)
        entry_id.grid(row=0, column=1)

        if not update:
            tk.Label(window, text="Name:").grid(row=1, column=0)
            entry_name = tk.Entry(window)
            entry_name.grid(row=1, column=1)

        tk.Label(window, text="Quantity:").grid(row=2, column=0)
        entry_quantity = tk.Entry(window)
        entry_quantity.grid(row=2, column=1)

        tk.Label(window, text="Price:").grid(row=3, column=0)
        entry_price = tk.Entry(window)
        entry_price.grid(row=3, column=1)

        def on_submit():
            item_id = entry_id.get()
            quantity = entry_quantity.get()
            price = entry_price.get()

            if not item_id or (not update and not entry_name.get()):
                messagebox.showerror("Error", "All fields must be filled.")
                return

            quantity = int(quantity) if quantity else None
            price = float(price) if price else None

            if update:
                message = action(item_id, quantity=quantity, price=price)
            else:
                name = entry_name.get()
                message = action(item_id, name, quantity, price)

            messagebox.showinfo(title, message)
            window.destroy()
            self.refresh_inventory()

        tk.Button(window, text="Submit", command=on_submit).grid(row=4, columnspan=2, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop()
