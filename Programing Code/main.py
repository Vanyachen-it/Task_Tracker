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
        
        tk.Label(input_frame, text="ID проекта:", bg = "#ffffff").grid(row=1,column=0, sticly="w", pady=5)
        self.project_id_entry = tk.Entry(input_frame, width=10)
        self.project_id_entry.insert(0, "1")
        self.project_id_entry.grid(row=1,column=1, sticky="w", pady=5, padx=5)

        add_btn = tk.Button(input_frame, text = "Создать задачу", command=self.add_task_action, bg="2ecc71", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=10)
        add_btn.grid(row=2, column=0, columnspan = 2, pady=10)

        list_frame = tk.LabelFrame(self.root, text="Текущие задачи в базе данных", bg="#ffffff", font("Helvetica", 10, "bold"), padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=20,pady=10)

        columbs = ("id", "name", "project", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height = 8)
        sel.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название задачи")
        self.tree.heading("project", text = "ID Проекта")
        self.tree.heading("status", text = "Статус")

        self.tree.column("id", width= 50, anchor="center")
        self.tree.column("name", width = 250)
        self.tree.column("project", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

    def add_task_action(self):
        name = self.task_name_entry.get().strip()
        proj_id_str = self.project_id_entry.get().strip()

        try:
            project_id = int (proj_id_str) if proj_id_str else None
        except ValueError:
            messagebox.showerror("Ошибка!", "ID проекта может состоять только из чисел!")
            return

        success = Task.set_new_task(name, project_id)

        if success:
            messagebox.showinfo("Успех", "Задача добавлена в базу данных!")
            self.task_nmae_entry.delete(0, tk.END)
            self.refresh_tasks_list()
        else:
            messagebox.showerror("Ошибка", "Поля не могут быть пустыми!")
    def refresh_tasks_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.db.execute_secure("SELECT id, task_name, project_id, status FROM tasks")
        for row in cursor.fetcall():
            self.tree.insert("", tk.END, values=row)

if __name__ == "__main__"
root = tk.Tk()
app = TaskTrackerApp(root)
root.mainloop()
        
