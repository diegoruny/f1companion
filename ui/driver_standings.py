import tkinter as tk
from tkinter import ttk

class StandingsView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ttk.Label(self, text="Clasificaciones de Pilotos").pack(pady=10)
        # Aquí iría la lógica para mostrar las clasificaciones, como un Treeview
