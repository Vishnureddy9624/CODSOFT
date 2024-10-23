import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x500")
        self.root.config(bg="#333")  # Dark background for calculator body
        
        # Styling options
        self.button_font = ("Arial", 16, "bold")
        self.result_font = ("Arial", 20, "bold")
        self.num_color = "#fff"  # White color for number buttons
        self.op_color = "#ff9500"  # Orange color for operation buttons
        self.bg_color = "#4d4d4d"  # Gray background for the buttons
        self.display_bg = "#000"  # Black background for display
        self.display_fg = "#0f0"  # Green for text in display
        
        # Display
        self.display = tk.Entry(root, font=self.result_font, fg=self.display_fg, bg=self.display_bg, borderwidth=0, justify="right")
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=20, padx=10, pady=10)
        
        # Buttons layout
        button_texts = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("+", 4, 2), ("=", 4, 3),
            ("C", 5, 0, 3), ("⌫", 5, 3)  # Clear button across 3 columns, backspace next to it
        ]

        # Create buttons
        for (text, row, col, *colspan) in button_texts:
            self.create_button(text, row, col, colspan[0] if colspan else 1)

    def create_button(self, text, row, col, colspan=1):
        button_color = self.op_color if text in "+-*/=⌫" else self.bg_color
        button = tk.Button(
            self.root, 
            text=text, 
            font=self.button_font, 
            fg=self.num_color if button_color == self.bg_color else "#fff",
            bg=button_color, 
            activebackground="#f2f2f2", 
            command=lambda t=text: self.on_button_click(t)
        )
        button.grid(row=row, column=col, columnspan=colspan, ipadx=20, ipady=20, padx=5, pady=5)

    def on_button_click(self, char):
        if char == "=":
            self.calculate()
        elif char == "C":
            self.display.delete(0, tk.END)
        elif char == "⌫":
            current_text = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current_text[:-1])  # Remove last character
        else:
            self.display.insert(tk.END, char)

    def calculate(self):
        try:
            result = eval(self.display.get())  # Caution: eval can be dangerous
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
        except Exception:
            messagebox.showerror("Error", "Invalid Input")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
