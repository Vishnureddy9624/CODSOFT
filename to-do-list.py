import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
import threading
import time
from datetime import datetime
import pygame  # Import pygame for sound playback

# Initialize the mixer for pygame
pygame.mixer.init()

# Load your alarm sound (ensure you have a .wav file in the same directory or provide the correct path)
ALARM_SOUND = "C:/Users/hp/Desktop/internshihp/alarm.wav"  # Replace with your alarm sound file path

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('todo_with_alarm.db')
cursor = conn.cursor()

# Create the tasks table if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    due_date TEXT NOT NULL,
    alarm_time TEXT
)
''')
conn.commit()

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List with Alarm")
        self.root.geometry("600x600")
        self.root.config(bg="#f0f4f8")  # Light background

        # Set up frames
        self.setup_frames()

        # Load existing tasks
        self.load_tasks()

    def setup_frames(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg="#3e64ff")
        title_frame.pack(pady=10, fill='x')
        title_label = tk.Label(title_frame, text="To-Do List with Alarm", font=("Arial", 20, "bold"), fg="white", bg="#3e64ff")
        title_label.pack(pady=10)

        # Task Form Frame
        form_frame = tk.Frame(self.root, bg="#f0f4f8")
        form_frame.pack(pady=10)

        self.desc_entry = tk.Entry(form_frame, width=40, font=("Arial", 12))
        self.desc_entry.grid(row=0, column=0, padx=10, pady=10)
        self.desc_entry.insert(0, "Task Description")  # Placeholder

        self.calendar = Calendar(form_frame, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        self.calendar.grid(row=1, column=0, padx=10, pady=10)

        self.alarm_hour_var = tk.StringVar(value='12')  # Default hour
        self.alarm_minute_var = tk.StringVar(value='00')  # Default minute
        self.am_pm_var = tk.StringVar(value='AM')  # Default AM/PM

        # Hour Dropdown
        self.hour_dropdown = tk.OptionMenu(form_frame, self.alarm_hour_var, *[f"{hour:02}" for hour in range(1, 13)])
        self.hour_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # Minute Dropdown
        self.minute_dropdown = tk.OptionMenu(form_frame, self.alarm_minute_var, *[f"{minute:02}" for minute in range(0, 60)])
        self.minute_dropdown.grid(row=0, column=2, padx=10, pady=10)

        # AM/PM Dropdown
        self.am_pm_dropdown = tk.OptionMenu(form_frame, self.am_pm_var, "AM", "PM")
        self.am_pm_dropdown.grid(row=0, column=3, padx=10, pady=10)

        self.add_task_button = tk.Button(form_frame, text="Add Task", command=self.create_task, bg="#3e64ff", fg="white", font=("Arial", 12))
        self.add_task_button.grid(row=2, columnspan=4, pady=10)

        self.modify_task_button = tk.Button(form_frame, text="Modify Task", command=self.modify_task, bg="#3e64ff", fg="white", font=("Arial", 12))
        self.modify_task_button.grid(row=3, columnspan=4, pady=5)

        self.delete_task_button = tk.Button(form_frame, text="Delete Task", command=self.delete_task, bg="#ff4c4c", fg="white", font=("Arial", 12))
        self.delete_task_button.grid(row=4, columnspan=4, pady=5)

        # Task List Frame
        self.task_frame = tk.Frame(self.root, bg="#f0f4f8")
        self.task_frame.pack(pady=10)

        self.task_list = tk.Listbox(self.task_frame, width=70, height=10, font=("Arial", 12), bg="#fff", fg="#333")
        self.task_list.pack(side="left", fill="both", expand=True)

        # Scrollbar for task list
        scrollbar = tk.Scrollbar(self.task_frame)
        scrollbar.pack(side="right", fill="y")
        self.task_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_list.yview)

        # Bind selection event to load task data
        self.task_list.bind('<<ListboxSelect>>', self.on_task_select)

    def create_task(self):
        description = self.desc_entry.get().strip()
        due_date = self.calendar.get_date()
        alarm_hour = self.alarm_hour_var.get()
        alarm_minute = self.alarm_minute_var.get()
        am_pm = self.am_pm_var.get()

        if description and due_date and alarm_hour and alarm_minute:
            alarm_time = f"{alarm_hour}:{alarm_minute} {am_pm}"
            cursor.execute("INSERT INTO tasks (description, due_date, alarm_time) VALUES (?, ?, ?)", (description, due_date, alarm_time))
            conn.commit()
            self.load_tasks()
            threading.Thread(target=self.check_alarm, args=(alarm_time,), daemon=True).start()  # Start alarm check in a new thread
            messagebox.showinfo("Success", "Task Created!")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")

    def load_tasks(self):
        self.task_list.delete(0, tk.END)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        for task in tasks:
            task_info = f"{task[0]}: {task[1]} (Due: {task[2]}, Alarm: {task[3]})"
            self.task_list.insert(tk.END, task_info)

    def on_task_select(self, event):
        """Fill the entry fields with the selected task's details."""
        try:
            selected_index = self.task_list.curselection()[0]
            selected_task = self.task_list.get(selected_index)
            task_id = int(selected_task.split(":")[0])  # Extract the task ID

            cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
            task = cursor.fetchone()

            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, task[1])
            self.calendar.selection_set(task[2])  # Set calendar to the task's due date

            # Parse the alarm time for dropdowns
            alarm_hour, alarm_minute_am_pm = task[3].split(':')
            alarm_minute, am_pm = alarm_minute_am_pm.split(' ')
            self.alarm_hour_var.set(alarm_hour)
            self.alarm_minute_var.set(alarm_minute)
            self.am_pm_var.set(am_pm)
        except IndexError:
            pass

    def modify_task(self):
        selected_index = self.task_list.curselection()
        if not selected_index:
            messagebox.showwarning("Select a task", "Please select a task to modify.")
            return

        task_id = int(self.task_list.get(selected_index).split(":")[0])
        description = self.desc_entry.get().strip()
        due_date = self.calendar.get_date()
        alarm_hour = self.alarm_hour_var.get()
        alarm_minute = self.alarm_minute_var.get()
        am_pm = self.am_pm_var.get()

        if description and due_date:
            alarm_time = f"{alarm_hour}:{alarm_minute} {am_pm}"
            cursor.execute("UPDATE tasks SET description=?, due_date=?, alarm_time=? WHERE id=?", (description, due_date, alarm_time, task_id))
            conn.commit()
            self.load_tasks()
            messagebox.showinfo("Success", "Task Modified!")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields!")

    def delete_task(self):
        selected_index = self.task_list.curselection()
        if not selected_index:
            messagebox.showwarning("Select a task", "Please select a task to delete.")
            return

        task_id = int(self.task_list.get(selected_index).split(":")[0])
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        self.load_tasks()
        messagebox.showinfo("Success", "Task Deleted!")

    def check_alarm(self, alarm_time):
        """Check if the current time matches the alarm time."""
        try:
            hour, minute_am_pm = alarm_time.split(':')
            minute, am_pm = minute_am_pm.split(' ')
            hour = int(hour)
            minute = int(minute)

            if am_pm == "PM" and hour != 12:
                hour += 12
            elif am_pm == "AM" and hour == 12:
                hour = 0
        except ValueError as e:
            print(f"Error parsing alarm time: {e}")
            return

        while True:
            now = datetime.now()
            if now.hour == hour and now.minute == minute:
                self.ring_alarm()
                break
            time.sleep(10)  # Check every 10 seconds

    def ring_alarm(self):
        """Play the alarm sound."""
        try:
            pygame.mixer.music.load(ALARM_SOUND)
            pygame.mixer.music.play()

            # Wait for the alarm to finish
            while pygame.mixer.music.get_busy():
                time.sleep(1)
        except pygame.error as e:
            print(f"Error playing alarm sound: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    todo_app = TodoApp(root)
    root.mainloop()

# Close the database connection when the program exits
conn.close()
