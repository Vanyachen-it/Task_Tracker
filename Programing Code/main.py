import customtkinter as ctk
from tkinter import messagebox
from config import DEFAULT_THEME, COLOR_THEME, APP_VERSION
from database import DatabaseManager
from security import SecurityProvider
from facade import TaskTrackerFacade
from analytics import AnalyticsEngine
from ui_components import UIStyleHelper

ctk.set_appearance_mode(DEFAULT_THEME)
ctk.set_default_color_theme(COLOR_THEME)

class ApplicationLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"TaskTracker Pro Enterprise [{APP_VERSION}]")
        self.geometry("1100x680")

        self.db = DatabaseManager()
        self.facade = TaskTrackerFacade()

        self.db.conn.execute("INSERT OR IGNORE INTO roles (id, role_name) VALUES (1, 'Admin')")
        SecurityProvider.register_secure_user("Иван Кашко", "secure_root_2026", 1)
        self.prime_database_relations()

        self.assamble_modular_inteface()
        self.sync_data_stream()

    def prime_database_relations(self):
        try:
            self.db.conn.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Архитектура ПО')")
            self.db.conn.execute("INSERT OR IGNORE INTO projects (id, project_name, owner_id, category_id) VALUES (1, 'Репозиторий Иван Кашко', 1, 1)")
        except Exception:
            pass

    def assamble_modular_inteface(self):
        self.grid_columnconfigure(0, weight=4, minsize=450)
        self.grid_columnconfigure(1, weight=3, minsize=350)
        self.grid_rowconfigure(0, weight=1)

        self.left_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.left_pane.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(self.left_pane, text="Архитектура модулей (8 файлов)", font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", pady=(0,15))

        self.wrapper_form = ctk.CTkFrame(self.left_pane, corner_radius=12)
        self.wrapper_form.pack(fill="x", pady=(0, 15))

        self.in_name = ctk.CTkEntry(self.wrapper_form, placeholder_text="Спецификация новой задачи...", height=35)
        self.in_name.pack(fill="x", padx=15, pady=10)

        self.row_layout = ctk.CTkFrame(self.wrapper_form, fg_color="transparent")
        self.row_layout.pack(fill="x", padx=15, pady=5)

        self.in_proj = ctk.CTkEntry(self.row_layout, placeholder_text="ID Проекта", width=90)
        self.in_proj.insert(0, "1")
        self.in_proj.pack(side="left")

        self.in_priority = ctk.CTkComboBox(self.row_layout, values=["Low", "Medium", "High"], width=120)
        self.in_priority.set("Medium")
        self.in_priority.pack(side="left", padx=10)

        self.btn_run = ctk.CTkButton(self.wrapper_form, text="Выполнить безопасную транзакцию", fg_color="#1f6aa5", command=self.commit_task)
        self.btn_run.pack(fill="x", padx=15, pady=15)

        self.wrapper_table = ctk.CTkFrame(self.left_pane, corner_radius=12)
        self.wrapper_table.pack(fill="both", expand=True)

        UIStyleHelper.configure_treeview_theme()
        from tkinter import ttk
        self.tree = ttk.Treeview(self.wrapper_table, columns=("id", "task", "priority", "status"), show="headings")
        self.tree.heading("id", text="ID"); self.tree.heading("task", text="Узел задачи"); self.tree.heading("priority", text="Приоритет"); self.tree.heading("status", text="Статус")
        self.tree.column("id", width=40, anchor="center"); self.tree.column("priority", width=80, anchor="center"); self.tree.column("status", width=90, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

        self.right_pane = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e1e1e" if ctk.get_appearance_mode() == "Dark" else "#eaeaea")
        self.right_pane.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        ctk.CTkLabel(self.right_pane, text="Аналитическое ядро (Data Science)", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=20, pady=15)
        self.box_charts = ctk.CTkFrame(self.right_pane, fg_color="transparent", height=240)
        self.box_charts.pack(fill="x", padx=20)

        ctk.CTkLabel(self.right_pane, text="Консоль аудита ядра системы (Лог транзакций)", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        self.console = ctk.CTkTextbox(self.right_pane, font=("Courier New", 11), fg_color="#101010", text_color="#2ecc71")
        self.console.pack(fill="both", expand=True, padx=20, pady=(0, 20))

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