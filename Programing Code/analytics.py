import customtkinter as ctk

class AnalyticsEngine:
    @staticmethod
    def render_horizontal_var_chart(container, data):
        for widget in container.winfo_children():
            widget.destroy()
        
        lbl = ctk.CTkLabel(
            container,
            text= "СУБД SQLite активна\n",
            font=ctk.CTkFont(size=12, slant="italic"),
            text_color="#7f8c8d"
        )
        lbl,pack(expand=True)