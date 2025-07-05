import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkinter import ttk
import os
from db import init_db
from auth import login, register
from inventory import *
from report import generate_summary

def apply_styles():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton',
                    font=('Segoe UI', 10),
                    padding=6,
                    background='#4CAF50',
                    foreground='white')
    style.map('TButton',
              background=[('active', '#45a049')])

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("600x400")
        self.root.iconphoto(False, PhotoImage(file=os.path.abspath("assets/logo.png")))
        apply_styles()
        self.login_screen()

    def login_screen(self):
        self.clear()
        logo_path = os.path.abspath(os.path.join("assets", "logo.png"))
        if os.path.exists(logo_path):
            self.logo_img = PhotoImage(file=logo_path)
            tk.Label(self.root, image=self.logo_img).pack(pady=10)
        tk.Label(self.root, text="Login or Register", font=('Segoe UI', 14, 'bold'), fg="#333").pack(pady=5)
        
        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack(pady=5)

        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack(pady=5)

        ttk.Button(self.root, text="Login", command=self.handle_login).pack(pady=5)
        ttk.Button(self.root, text="Register", command=self.handle_register).pack(pady=5)

    def handle_login(self):
        if login(self.username.get(), self.password.get()):
            self.main_screen()
        else:
            messagebox.showerror("Error", "Invalid login")

    def handle_register(self):
        result = register(self.username.get(), self.password.get())
        if result == "success":
            messagebox.showinfo("Success", "Registered successfully")
        elif result == "exists":
            messagebox.showerror("Error", "User already exists")
        elif result == "empty":
            messagebox.showerror("Error", "Username or password cannot be empty")
        else:
            messagebox.showerror("Error", "Registration failed")

    def main_screen(self):
        self.clear()
        tk.Label(self.root, text="Inventory Dashboard", font=('Segoe UI', 14, 'bold')).pack(pady=10)
        ttk.Button(self.root, text="Add Product", command=self.add_product_popup).pack(pady=5)
        ttk.Button(self.root, text="View Inventory", command=self.view_inventory).pack(pady=5)
        ttk.Button(self.root, text="Low Stock Report", command=self.low_stock_report).pack(pady=5)
        ttk.Button(self.root, text="Sales Summary", command=self.sales_summary).pack(pady=5)
        ttk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)

    def add_product_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Add Product")
        win.geometry("300x200")

        name = tk.Entry(win)
        name.insert(0, "Product Name")
        name.pack(pady=5)

        qty = tk.Entry(win)
        qty.insert(0, "Quantity")
        qty.pack(pady=5)

        price = tk.Entry(win)
        price.insert(0, "Price")
        price.pack(pady=5)

        ttk.Button(win, text="Add", command=lambda: [add_product(name.get(), int(qty.get()), float(price.get())), win.destroy(), self.view_inventory()]).pack(pady=5)

    def view_inventory(self):
        self.clear()
        tk.Label(self.root, text="Inventory List", font=('Segoe UI', 14, 'bold')).pack()
        for p in get_all_products():
            tk.Label(self.root, text="ID: {}, {} | Qty: {} | ₹{}".format(p[0], p[1], p[2], p[3])).pack()

        ttk.Button(self.root, text="Back", command=self.main_screen).pack(pady=10)

    def low_stock_report(self):
        self.clear()
        tk.Label(self.root, text="Low Stock Products", font=('Segoe UI', 14, 'bold')).pack()
        for p in get_low_stock():
            tk.Label(self.root, text="{} (Qty: {})".format(p[1], p[2])).pack()

        ttk.Button(self.root, text="Back", command=self.main_screen).pack(pady=10)

    def sales_summary(self):
        self.clear()
        summary = generate_summary()
        tk.Label(self.root, text="Total Products: {}".format(summary['total_products'])).pack()
        tk.Label(self.root, text="Inventory Value: ₹{}".format(summary['inventory_value'])).pack()
        tk.Label(self.root, text="Low Stock Items:").pack()
        for p in summary['low_stock']:
            tk.Label(self.root, text="{} (Qty: {})".format(p[1], p[2])).pack()

        ttk.Button(self.root, text="Back", command=self.main_screen).pack(pady=10)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize database and launch GUI
init_db()
root = tk.Tk()
app = InventoryApp(root)
root.mainloop()
