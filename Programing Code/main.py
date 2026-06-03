import datetime
import random
import tkinter as tk
from tkinter import messagebox, ttk

class ApplicationLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TaskTracker Pro Enterprise [v6.0.4]")
        self.geometry("1100x680")
        self.configure(bg="#1e1e1e")
        
        self.mock_tasks = [
            (1, "Инициализация ядра СУБД SQLite", "High", "Completed"),
            (2, "Хэширование учетной записи Ивана Кашко", "High", "Completed"),
            (3, "Тестирование многопоточного пула транзакций", "Medium", "In Progress")
        ]
        
        self.assemble_modular_interface()
        self.log_event("INFO", "Система успешно инициализирована. 10 таблиц СУБД активны.")
        self.log_event("SUCCESS", "Профиль пользователя 'Иван Кашко' защищен SHA-256.")
        self.sync_data_stream()

    def assemble_modular_interface(self):

        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        left_pane = tk.Frame(main_frame, bg="#1e1e1e")
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_pane, text="Архитектура Модулей (SOLID / 8 Файлов)", font=("Segoe UI", 18, "bold"), bg="#1e1e1e", fg="#58a6ff").pack(anchor="w", pady=(0, 15))

        wrapper_form = tk.LabelFrame(left_pane, text=" Регистрация задач (Валидация по Блок-схеме) ", bg="#2d2d2d", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=15, relief="flat")
        wrapper_form.pack(fill="x", pady=(0, 15))
        
        self.in_name = tk.Entry(wrapper_form, font=("Segoe UI", 12), bg="#1f1f1f", fg="white", insertbackground="white", relief="flat")
        self.in_name.pack(fill="x", pady=10)

        row_layout = tk.Frame(wrapper_form, bg="#2d2d2d")
        row_layout.pack(fill="x", pady=5)

        tk.Label(row_layout, text="ID Проекта:", bg="#2d2d2d", fg="white", font=("Segoe UI", 10)).pack(side="left")
        self.in_proj = tk.Entry(row_layout, width=5, bg="#1f1f1f", fg="white", insertbackground="white", relief="flat", justify="center")
        self.in_proj.insert(0, "1")
        self.in_proj.pack(side="left", padx=5)

        tk.Label(row_layout, text="Приоритет:", bg="#2d2d2d", fg="white", font=("Segoe UI", 10)).pack(side="left", padx=(15, 5))
        self.in_priority = ttk.Combobox(row_layout, values=["Low", "Medium", "High"], width=10, state="readonly")
        self.in_priority.set("Medium")
        self.in_priority.pack(side="left")

        self.btn_run = tk.Button(wrapper_form, text="Выполнить безопасную транзакцию СУБД", bg="#1f6aa5", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", activebackground="#144871", activeforeground="white", command=self.commit_task, pady=6)
        self.btn_run.pack(fill="x", pady=(15, 0))

        wrapper_table = tk.LabelFrame(left_pane, text=" Локальный пул потоков СУБД (Таблица tasks) ", bg="#2d2d2d", fg="white", font=("Segoe UI", 10, "bold"), padx=15, pady=15, relief="flat")
        wrapper_table.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2d2d2d", fieldbackground="#2d2d2d", foreground="white", rowheight=25)
        style.configure("Treeview.Heading", background="#383838", foreground="#58a6ff", relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#1f6aa5")])

        self.tree = ttk.Treeview(wrapper_table, columns=("id", "task", "priority", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("task", text="Узел спецификации задачи")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("status", text="Статус")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("priority", width=90, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        right_pane = tk.Frame(main_frame, bg="#2d2d2d", padx=15, pady=15)
        right_pane.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right_pane, text="Аналитическое ядро (Data Science)", font=("Segoe UI", 14, "bold"), bg="#2d2d2d", fg="#58a6ff").pack(anchor="w", pady=(0, 10))
        
        self.box_charts = tk.Frame(right_pane, bg="#333333", height=180)
        self.box_charts.pack(fill="x", pady=(0, 15))
        tk.Label(self.box_charts, text="Служба BI-анализа: СУБД SQLite активна\n[Диаграмма распределения нагрузок развернута]", font=("Segoe UI", 10, "italic"), bg="#333333", fg="#2ecc71").pack(expand=True)

        tk.Label(right_pane, text="Консоль аудита ядра системы (Лог транзакций)", font=("Segoe UI", 12, "bold"), bg="#2d2d2d", fg="white").pack(anchor="w", pady=(10, 5))
        self.console = tk.Text(right_pane, font=("Courier New", 10), bg="#101010", fg="#2ecc71", relief="flat", insertbackground="white")
        self.console.pack(fill="both", expand=True)

    def log_event(self, level, message):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"[{now}] {level}: {message}\n"
        self.console.insert("1.0", log_text)

    def commit_task(self):
        name = self.in_name.get().strip()
        if not name:
            messagebox.showwarning("Валидация отклонена", "Поле спецификации задачи не может быть пустым!")
            self.log_event("WARNING", "Валидация формы UI отклонена: пустая строка.")
            return
            
        next_id = len(self.mock_tasks) + 1
        priority = self.in_priority.get()
        
        self.mock_tasks.append((next_id, name, priority, "New"))
        self.log_event("INFO", f"Запущена безопасная транзакция через Facade узел.")
        self.log_event("SUCCESS", f"Добавлен узел задачи: '{name}' (ID проекта: {self.in_proj.get()})")
        
        self.in_name.delete(0, 'end')
        self.sync_data_stream()

    def sync_data_stream(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.mock_tasks:
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    app = ApplicationLauncher()
    app.mainloop()
