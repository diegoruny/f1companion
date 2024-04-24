import tkinter as tk
from tkinter import ttk
from .next_race import NextRaceView

class TopBar(ttk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent

        # Frame container for both the last and the next race
        self.top_bar_frame = ttk.Frame(self)
        self.top_bar_frame.pack(fill=tk.BOTH, expand=True)

        self.next_race_card()
        self.last_race_card()

    def last_race_card(self):
        ttk.Label(self, text="Last race", font=("Arial", 16, "bold"), borderwidth=4, relief="solid").pack(pady=10)
        self.last_race_view = LastRaceView(self, self.api_handler)
        # need to finish the func in nextRace.py

    def next_race_card(self):
        ttk.Label(self, text="Upcoming Race", font=("Arial", 16, "bold"), borderwidth=4, relief="solid").pack(pady=10)
        self.next_race_view = NextRaceView(self, self.api_handler)
        self.next_race_view.pack(pady=10, fill=tk.BOTH, expand=True)