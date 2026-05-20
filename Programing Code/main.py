import tkinter as tk
from tkinter import messagebox, ttk
from database import DatabaseManager
from models impor Task

class TaskTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskTracker")
        self.root.configure(bg="#f4f6f9")

        self.db = DatabaseManager()
        self.setup_dummy_data()
        self.create_widgets()
        self.refresh_tasks_list()

    def setup_dummy_data(self):
        try:
            self.db.execute_secure("INSERT OR IGNORE INTO users (id, nickname, password, role) VALUES (1, 'Ivan Kashko', 'pass', 'admin')")
            self.db.execute_secure("INSERT OR IGNORE INTO projects (id, project_name, owner_id) VALUES (1, 'РАЗРАБОТКА сайта ТЗ, 1)")
        except Exception:
            pass
    
    def create_widgets(self):
        title_label = tk.Label(self.root, text = "TaskTracker System", font = ("Helvetica", 16, "bold"), bg="f4f6f9", fg="2c3e50")
        title_label.pack(pady=10)

        input_frame = tk.LabelFrame(self.root, text="Доавблена новая задача", bg="#ffffff", font=("Helvetica", 10, "bold"), padx=10, pady=10)
        input_frame.pack(fill="x", padx=20,pady=10)

        tk.Label(input_frame, text="Название задачи: ", bg="ffffff").grid(row=0,column=0, stiky="w", pady=5)
        self.task_name_entryy = tk.Entry(input_frame, width=30)
        self.task_name_entry.grid(row=0,column=1,pady=5,padx=5)
        