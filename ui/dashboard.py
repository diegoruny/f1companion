
import tkinter as tk
from tkinter import ttk
from tkinter import font
# from api.api_handler import ErgastAPI
from .driver_standings import StandingsView
from .next_race import NextRaceView

class Dashboard(tk.Frame):
    def __init__(self, parent,api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent
        ttk.Label(self, text="F1 Race Companion Dashboard", font=("Arial", 20, "bold")).pack(pady=20)
        self.next_race_card()
        # Botón para cambiar a la vista de clasificaciones, como ejemplo
        self.standings_button = ttk.Button(self, text="Standings", command=self.show_standings)
        self.standings_button.pack(pady=10)
    
    def show_standings(self):
        self.pack_forget()  # Oculta el dashboard
        standings_view = StandingsView(self.parent)
        standings_view.pack(fill=tk.BOTH, expand=True)

    def next_race_card(self):
        ttk.Label(self, text="Upcoming Race", font=("Arial", 16, "bold")).pack(pady=10)
        self.next_race_view = NextRaceView(self, self.api_handler)
        self.next_race_view.pack(pady=10, fill=tk.BOTH, expand=True)