import tkinter as tk
from tkinter import ttk
from .next_race import NextRaceView

class TopBar(ttk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent

        # Frame container for both the last and the next race
        self.top_bar_frame = ttk.Frame(self, bootstyle='dark.TFrame')
        self.top_bar_frame.grid(padx=0, pady=0, sticky='EW')

        self.next_race_card()
        #self.last_race_card()

    # def last_race_card(self):
    #     ttk.Label(self, text="Last race from top_Bar.py", font=("Arial", 16, "bold"), borderwidth=4, relief="solid").grid(padx=10, pady=10, sticky='n')
    #     self.last_race_view = NextRaceView.last_race_card(self)
    #     # need to finish the func in nextRace.py

    def next_race_card(self):
        self.next_race_view = NextRaceView(self, self.api_handler)
        self.next_race_view.grid(padx=10, pady=10, sticky='s')