import matlotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backends_tkagg import FigureCanvasTkAgg
import customtkinter as ctk

class AnalyticsEngine:
    @staticmethod
    def render_horizontal_var_chart(container, data):
        for widget in container.winfo_children():
            widget.destroy()
        
        if not data:
            return

        labels = [row[0] for row in data]
        values = [row[1] for row in data]

        is_dark = ctk.get_appearance_mode() == "Dark"
        fig, ax = plt.subplots(figsize=(3.8, 2.4), facecolor="#1e1e1e" if is_dark else "#dbdbdb")
        ax.set_facecolor("#1e1e1e" if is_dark else "#dbdbdb")

        ax.barh(labels, values, color="#1f6aa5", edgecolor="none", height=0.4)
        ax.tick_params(colors='white' if is_dark else 'black', labelsize=9)

        for spine in ['top','right']:
            ax.spines[spine].set_visible(False)
        for spine in ['left', 'bottom']:
            ax.spines[spine].set_color('#333333' if is_dark else '#cccccc')

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
