from tkinter import ttk
import customtkinter as ctk

class UIStyleHelper:
    @staticmethod
    def configure_treeview_theme():
        """Стилизация классического Treeview под современный Fluent/Dark UI"""
        style = ttk.Style()
        style.theme_use("default")
        is_dark = ctk.get_appearance_mode() == "Dark"

        style.configure(
            "Treeview",
            background="#2a2a2a" if is_dark else "#ffffff",
            foreground="white" if is_dark else "black",
            fieldbackground="#2a2a2a" if is_dark else "#ffffff",
            rowheight=28
        )
        style.configure(
            "Treeview.Heading",
            background="#3e3e3e" if is_dark else "#e6e6e6",
            foreground="white" if is_dark else "black",
            font=("Helvetica", 10, "bold")
        )
        style.map("Treeview", background=[("selected", "#1f6aa5")])