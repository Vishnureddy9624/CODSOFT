import tkinter as tk
from tkinter import messagebox, simpledialog

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management Application")
        self.root.geometry("400x450")
        self.root.config(bg="#F7F7F7")  # Light grey background
        self.contacts = {}

        # Frame for the input fields
        self.frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief="groove")
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Labels and Entry fields for contact details
        tk.Label(self.frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        self.name_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#EAEAEA")
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="Phone Number:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        self.phone_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#EAEAEA")
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="Email:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#EAEAEA")
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="Address:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
        self.address_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#EAEAEA")
        self.address_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons with enhanced styles
        button_style = {
            "font": ("Arial", 12),
            "bg": "#6200EA",  # Deep purple background
            "fg": "white",
            "activebackground": "#3700B3",  # Darker purple on press
            "width": 12
        }

        tk.Button(root, text="Add Contact", **button_style, command=self.add_contact).pack(pady=5)
        tk.Button(root, text="View Contacts", **button_style, command=self.view_contacts).pack(pady=5)
        tk.Button(root, text="Search Contact", **button_style, command=self.search_contact).pack(pady=5)
        tk.Button(root, text="Update Contact", **button_style, command=self.update_contact).pack(pady=5)
        tk.Button(root, text="Delete Contact", **button_style, command=self.delete_contact).pack(pady=5)

        # Add some padding to the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if name and phone:
            self.contacts[name] = {
                "phone": phone,
                "email": email,
                "address": address
            }
            messagebox.showinfo("Success", f"Contact '{name}' added successfully!")
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Name and Phone Number are required!")

    def view_contacts(self):
        if not self.contacts:
            messagebox.showinfo("Contact List", "No contacts found!")
            return

        contact_list = "\n".join([f"{name}: {details['phone']}" for name, details in self.contacts.items()])
        messagebox.showinfo("Contact List", contact_list)

    def search_contact(self):
        name = simpledialog.askstring("Search Contact", "Enter the name to search:")
        if name:
            if name in self.contacts:
                details = self.contacts[name]
                contact_info = f"Name: {name}\nPhone: {details['phone']}\nEmail: {details['email']}\nAddress: {details['address']}"
                messagebox.showinfo("Contact Found", contact_info)
            else:
                messagebox.showinfo("Search Result", "Contact not found.")

    def update_contact(self):
        name = simpledialog.askstring("Update Contact", "Enter the name of the contact to update:")
        if name in self.contacts:
            phone = simpledialog.askstring("Update Phone Number", "Enter new phone number:", initialvalue=self.contacts[name]['phone'])
            email = simpledialog.askstring("Update Email", "Enter new email:", initialvalue=self.contacts[name]['email'])
            address = simpledialog.askstring("Update Address", "Enter new address:", initialvalue=self.contacts[name]['address'])

            self.contacts[name] = {
                "phone": phone if phone else self.contacts[name]['phone'],
                "email": email if email else self.contacts[name]['email'],
                "address": address if address else self.contacts[name]['address']
            }
            messagebox.showinfo("Success", f"Contact '{name}' updated successfully!")
        else:
            messagebox.showwarning("Update Error", f"Contact '{name}' not found!")

    def delete_contact(self):
        name = simpledialog.askstring("Delete Contact", "Enter the name of the contact to delete:")
        if name in self.contacts:
            del self.contacts[name]
            messagebox.showinfo("Success", f"Contact '{name}' deleted successfully!")
        else:
            messagebox.showwarning("Delete Error", f"Contact '{name}' not found!")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
