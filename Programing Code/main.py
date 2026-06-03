import tkinter as tk
from tkinter import messagebox, ttk
from config import APP_VERSION
from database import DatabaseManager
from security import SecurityProvider
from facade import TaskTrackerFacade
from analytics import AnalyticsEngine
from ui_components import UIStyleHelper

class ApplicationLauncher(tk.Tk):
    def init(self):
        super().init()
        self.title(f"TaskTracker Pro Enterprise [{APP_VERSION}]")
        self.geometry("1100x680")
        self.configure(bg="#2a2a2a")

        self.db = DatabaseManager()
        self.facade = TaskTrackerFacade()

        self.db.execute_secure("INSERT OR IGNORE INTO roles (id, role_name) VALUES (1, 'Admin')")
        SecurityProvider.register_secure_user("Иван Кашко", "secure_root_2026", 1)
        self.prime_database_relations()

        self.assemble_modular_interface()
        self.sync_data_stream() 
        def prime_database_relations(self):
        try:
            self.db.execute_secure("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Архитектура ПО')")
            self.db.execute_secure("INSERT OR IGNORE INTO projects (id, project_name, owner_id, category_id) VALUES (1, 'Репозиторий Ивана Кашко', 1, 1)")
        except Exception:
            pass

    def assemble_modular_interface(self):
        main_frame = tk.Frame(self, bg="#2a2a2a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        left_pane = tk.Frame(main_frame, bg="#2a2a2a")
        left_pane.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(left_pane, text="Архитектура Модулей (8 Файлов)", font=("Helvetica", 18, "bold"), bg="#2a2a2a", fg="white").pack(anchor="w", pady=(0, 15))

        wrapper_form = tk.LabelFrame(left_pane, text=" Регистрация задач ", bg="#333333", fg="white", font=("Helvetica", 10, "bold"), padx=15, pady=15)
        wrapper_form.pack(fill="x", pady=(0, 15))

        self.in_name = tk.Entry(wrapper_form, font=("Helvetica", 12), bg="#444444", fg="white", insertbackground="white")
        self.in_name.pack(fill="x", pady=10)

        row_layout = tk.Frame(wrapper_form, bg="#333333")
        row_layout.pack(fill="x", pady=5)
        row_layout = tk.Frame(wrapper_form, bg="#333333")
        row_layout.pack(fill="x", pady=5)

        tk.Label(row_layout, text="ID Проекта:", bg="#333333", fg="white").pack(side="left")
        self.in_proj = tk.Entry(row_layout, width=5, bg="#444444", fg="white", insertbackground="white")
        self.in_proj.insert(0, "1")
        self.in_proj.pack(side="left", padx=5)

        tk.Label(row_layout, text="Приоритет:", bg="#333333", fg="white").pack(side="left", padx=(15, 5))
        self.in_priority = ttk.Combobox(row_layout, values=["Low", "Medium", "High"], width=10, state="readonly")
        self.in_priority.set("Medium")
        self.in_priority.pack(side="left")

        self.btn_run = tk.Button(wrapper_form, text="Выполнить безопасную транзакцию", bg="#1f6aa5", fg="white", font=("Helvetica", 11, "bold"), relief="flat", command=self.commit_task, pady=5)
        self.btn_run.pack(fill="x", pady=(15, 0))

        wrapper_table = tk.LabelFrame(left_pane, text=" Локальный пул потоков задач СУБД ", bg="#333333", fg="white", font=("Helvetica", 10, "bold"), padx=15, pady=15)
        wrapper_table.pack(fill="both", expand=True)

        UIStyleHelper.configure_treeview_theme()
        self.tree = ttk.Treeview(wrapper_table, columns=("id", "task", "priority", "status"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("task", text="Узел задачи")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("status", text="Статус")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("priority", width=80, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.pack(fill="both", expand=True)

        right_pane = tk.Frame(main_frame, bg="#1e1e1e", padx=15, pady=15)
        right_pane.pack(side="right", fill="both", expand=True, padx=(10, 0))

        tk.Label(right_pane, text="Аналитическое ядро (Data Science)", font=("Helvetica", 12, "bold"), bg="#1e1e1e", fg="white").pack(anchor="w", pady=(0, 15))
        self.box_charts = tk.Frame(right_pane, bg="#1e1e1e", height=240)
        self.box_charts.pack(fill="x")

        tk.Label(right_pane, text="Консоль аудита ядра системы (Лог транзакций)", font=("Helvetica", 11, "bold"), bg="#1e1e1e", fg="white").pack(anchor="w", pady=(15, 5))
        self.console = tk.Text(right_pane, font=("Courier New", 10), bg="#101010", fg="#2ecc71", relief="flat")
        self.console.pack(fill="both", expand=True)

    def commit_task(self):
        name = self.in_name.get().strip()
        try:
            p_id = int(self.in_proj.get().strip())
        except ValueError:
            return
        self.facade.async_add_task_pipeline(name, p_id, self.in_priority.get(), self.post_commit_callback)

    def post_commit_callback(self, success, msg):
        if success:
            self.in_name.delete(0, 'end')
            self.sync_data_stream()

    def sync_data_stream(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor = self.db.execute_secure("SELECT id, task_name, priority, status FROM tasks")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
            
        AnalyticsEngine.render_horizontal_bar_chart(self.box_charts, self.facade.fetch_bi_metrics())
        
        self.console.delete("1.0", "end")
        cursor_logs = self.db.execute_secure("SELECT timestamp, level, message FROM audit_logs ORDER BY id DESC LIMIT 20")
        for log in cursor_logs.fetchall():
            self.console.insert("end", f"[{log[0]}] {log[1]}: {log[2]}\n")

if __name__ == "__main__":
    app = ApplicationLauncher()
    app.mainloop()