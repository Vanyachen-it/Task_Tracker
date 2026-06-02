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

        self.db.execute_secure("INSERT OR IGNORE INTO roles (id,role_name) VALUES (1, 'Admin')")
        SecurityProvider.register_secure_user("Иван Кашко", "secure_root_2026", 1)
        self.prime_database_relations()

        self.assamble_modular_inteface()
        self.sync_data_stream()

    def prime_database_relations(self):
        try:
            self.db.execute_secure("INSERT OR IGNORE INTO categories (id, name) VALUES (1, 'Архитектура ПО')")
            self.db.execute_secure("INSERT OR IGNORE INTO projects (id, project_name, owner_id, category_id) VALUES (1, 'Репозиторий Иван Кашко', 1, 1)")
        except Exception:
            pass

    def assamble_modular_inteface(self):
        self.grid_columnconfigure(0, weight=4, minsize=450)
        self.grid_columnconfigure(1, weight=3, minsize=350)
        self.grid_rowconfigure(0, weight=1)

        self.left_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.left_pane.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)