import tkinter as tk
import random

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Game")
        self.root.geometry("400x350")
        self.root.config(bg="#EAEAEA")  # Light background color

        self.choices = ["rock", "paper", "scissors"]
        self.user_score = 0
        self.computer_score = 0

        # Title Label
        self.title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 24, "bold"), bg="#EAEAEA")
        self.title_label.pack(pady=10)

        # User choice buttons with emojis
        self.buttons_frame = tk.Frame(root, bg="#EAEAEA")
        self.buttons_frame.pack(pady=10)

        self.rock_button = tk.Button(self.buttons_frame, text="🪨", font=("Arial", 50), width=2, bg="#FF5733", fg="white", command=lambda: self.play("rock"))
        self.rock_button.grid(row=0, column=0, padx=10)

        self.paper_button = tk.Button(self.buttons_frame, text="📄", font=("Arial", 50), width=2, bg="#33FF57", fg="white", command=lambda: self.play("paper"))
        self.paper_button.grid(row=0, column=1, padx=10)

        self.scissors_button = tk.Button(self.buttons_frame, text="✂️", font=("Arial", 50), width=2, bg="#3357FF", fg="white", command=lambda: self.play("scissors"))
        self.scissors_button.grid(row=0, column=2, padx=10)

        # Result Label
        self.result_label = tk.Label(root, text="", font=("Arial", 16), fg="blue", bg="#EAEAEA")
        self.result_label.pack(pady=10)

        # Score Display
        self.score_label = tk.Label(root, text="User: 0  Computer: 0", font=("Arial", 16), bg="#EAEAEA")
        self.score_label.pack(pady=10)

        # Play Again Button with return arrow
        self.play_again_button = tk.Button(root, text="🔄", font=("Arial", 14), bg="#FFC300", command=self.reset_game)
        self.play_again_button.pack(pady=10)

    def play(self, user_choice):
        computer_choice = random.choice(self.choices)
        user_emoji = self.get_emoji(user_choice)
        computer_emoji = self.get_emoji(computer_choice)

        # Animate the result label
        self.result_label.config(text=f"You chose: {user_emoji}, Computer chose: {computer_emoji}")
        self.animate_result()

        winner = self.determine_winner(user_choice, computer_choice)

        if winner == "user":
            self.user_score += 1
            self.result_label.config(text=f"{self.result_label.cget('text')}\n🎉 You win! 🎉")
        elif winner == "computer":
            self.computer_score += 1
            self.result_label.config(text=f"{self.result_label.cget('text')}\n🤖 Computer wins! 🤖")
        else:
            self.result_label.config(text=f"{self.result_label.cget('text')}\n🤝 It's a tie! 🤝")

        self.update_score()

    def get_emoji(self, choice):
        """ Return emoji representation for the user's choice. """
        emojis = {
            "rock": "🪨",        # Rock emoji
            "paper": "📄",       # Paper emoji
            "scissors": "✂️"     # Scissors emoji
        }
        return emojis.get(choice, "")

    def determine_winner(self, user, computer):
        if user == computer:
            return "tie"
        elif (user == "rock" and computer == "scissors") or \
             (user == "scissors" and computer == "paper") or \
             (user == "paper" and computer == "rock"):
            return "user"
        else:
            return "computer"

    def update_score(self):
        self.score_label.config(text=f"User: {self.user_score}  Computer: {self.computer_score}")

    def reset_game(self):
        self.result_label.config(text="")
        self.user_score = 0
        self.computer_score = 0
        self.update_score()

    def animate_result(self):
        """ Simple animation for result label to make it more engaging. """
        self.result_label.config(fg="red")
        self.root.after(300, lambda: self.result_label.config(fg="blue"))

if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsGame(root)
    root.mainloop()
