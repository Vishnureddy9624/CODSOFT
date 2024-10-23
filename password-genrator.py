import tkinter as tk
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x300")
        self.root.config(bg="#f2f2f2")

        # Title label
        self.title_label = tk.Label(root, text="Password Generator", font=("Arial", 20, "bold"), bg="#f2f2f2")
        self.title_label.pack(pady=10)

        self.length_label = tk.Label(root, text="Enter password length:", font=("Arial", 14), bg="#f2f2f2")
        self.length_label.pack(pady=10)

        self.length_entry = tk.Entry(root, font=("Arial", 14), width=5)
        self.length_entry.pack(pady=5)

        self.complexity_var = tk.StringVar(value="All")  # Default option

        self.complexity_frame = tk.Frame(root, bg="#f2f2f2")
        self.complexity_frame.pack(pady=10)

        # Radio buttons for complexity options
        self.all_chars_radio = tk.Radiobutton(self.complexity_frame, text="All Characters", variable=self.complexity_var, value="All",
                                               bg="#f2f2f2", font=("Arial", 12))
        self.all_chars_radio.pack(side=tk.LEFT, padx=5)

        self.alpha_numeric_radio = tk.Radiobutton(self.complexity_frame, text="Alphanumeric", variable=self.complexity_var, value="AlphaNumeric",
                                                   bg="#f2f2f2", font=("Arial", 12))
        self.alpha_numeric_radio.pack(side=tk.LEFT, padx=5)

        self.alpha_radio = tk.Radiobutton(self.complexity_frame, text="Alphabetic", variable=self.complexity_var, value="Alpha",
                                           bg="#f2f2f2", font=("Arial", 12))
        self.alpha_radio.pack(side=tk.LEFT, padx=5)

        # Generate Password button
        self.generate_button = tk.Button(root, text="Generate Password", font=("Arial", 14), command=self.generate_password,
                                          bg="#4CAF50", fg="white", activebackground="#45a049")
        self.generate_button.pack(pady=10)

        self.password_label = tk.Label(root, text="Generated Password:", font=("Arial", 14), bg="#f2f2f2")
        self.password_label.pack(pady=10)

        self.password_output = tk.Entry(root, font=("Arial", 14), fg="green", width=30, bg="#ffffff")
        self.password_output.pack(pady=5)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length <= 0:
                raise ValueError("Length must be greater than 0")

            if self.complexity_var.get() == "All":
                characters = string.ascii_letters + string.digits + string.punctuation
            elif self.complexity_var.get() == "AlphaNumeric":
                characters = string.ascii_letters + string.digits
            elif self.complexity_var.get() == "Alpha":
                characters = string.ascii_letters
            else:
                raise ValueError("Invalid complexity level selected")

            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_output.delete(0, tk.END)
            self.password_output.insert(0, password)
        except ValueError as e:
            self.password_output.delete(0, tk.END)
            self.password_output.insert(0, f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
