import tkinter as tk
from tkinter import ttk

class NextRaceView(tk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.api_handler = api_handler
        self.last_race_card().grid(row=0, column=0)
        self.next_race_card().grid(row=0, column=1)

    def last_race_card(self):
        race_details = self.api_handler.get_last_race()[0]
        print(race_details)
        if race_details:
            # Frame for the card
            card_frame = ttk.Frame(self, padding="10", relief="raised", borderwidth=2)
            card_frame.pack(padx=10, pady=10, fill="both", expand=True)

            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Arial", 16, "bold")).pack()

            # Circuit y Location
            ttk.Label(card_frame, text=f"Circuit: {race_details['circuit']} - {race_details['location']}", font=("Arial", 12)).pack()

            # Date and Time
            date_time_str = f"Date: {race_details['date']} - Time: {race_details['time']}"  #Here the time is not being received
            ttk.Label(card_frame, text=date_time_str, font=("Arial", 12)).pack()

            return card_frame

        else:
            print("Failed to retrieve complete race details or podium.")
            return None  # Explicitly return None if data is incomplete
        

    def next_race_card(self):
        race_details = self.api_handler.get_next_race()
        if race_details:
            # Frame for the card
            card_frame = ttk.Frame(self, padding="10", relief="raised", borderwidth=2)
            card_frame.pack(padx=10, pady=10, fill="both", expand=True)

            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Arial", 16, "bold")).pack()

            # Circuit y Location
            ttk.Label(card_frame, text=f"Circuit: {race_details['circuit']} - {race_details['location']}", font=("Arial", 12)).pack()

            # Date and Time
            date_time_str = f"Date: {race_details['date']} - Time: {race_details['time']}"
            ttk.Label(card_frame, text=date_time_str, font=("Arial", 12)).pack()
            return card_frame

        else:
            print("Failed to retrieve complete race details or podium.")
            return None  # Explicitly return None if data is incomplete
