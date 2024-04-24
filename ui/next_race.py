import tkinter as tk
from tkinter import ttk

class NextRaceView(tk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid([0, 1])  # Here I want to set the space as a grid layout with 1 row and 2 columns
        self.api_handler = api_handler
        self.last_race_card()
        self.next_race_card()

    def last_race_card(self):
        race_details = self.api_handler.get_last_race()
        if race_details:
            # Frame for the card
            card_frame = ttk.Frame(self, padding="10", relief="raised", borderwidth=2)
            card_frame.pack(padx=10, pady=10, fill="both", expand=True)
        

    def next_race_card(self):
        race_details = self.api_handler.get_next_race()
        if race_details:
            # Frame for the card
            card_frame = ttk.Frame(self, padding="10", relief="raised", borderwidth=2)
            card_frame.pack(padx=10, pady=10, fill="both", expand=True)

            # Race Title
            ttk.Label(card_frame, text=race_details["name"], font=("Arial", 16, "bold")).pack()

            # Circuit y Location
            ttk.Label(card_frame, text=f"Circuit: {race_details['circuit']} - {race_details['location']}", font=("Arial", 12)).pack()

            # Date and Time
            date_time_str = f"Date: {race_details['date']} - Time: {race_details['time']}"
            ttk.Label(card_frame, text=date_time_str, font=("Arial", 12)).pack()
