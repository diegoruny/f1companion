import tkinter as tk
from tkinter import ttk

class NextRaceView(tk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.api_handler = api_handler
        self.last_race_card().pack()
        self.next_race_card().pack()

    def last_race_card(self):
        race_details = self.api_handler.get_last_race()[0]
        #print("Last Race json:\n", race_details)
        if race_details:
            # Frame for the card
            card_frame = ttk.Labelframe(self, text='LAST', bootstyle='danger')
            card_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)

            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Arial", 16, "bold"), bootstyle='inverse-dark').grid(padx=10, pady=10, sticky='ew')

            # Circuit y Location
            ttk.Label(card_frame, text=f"{race_details['circuit']}", font=("Arial", 12)).grid(padx=10, pady=10, sticky='ew')
            ttk.Label(card_frame, text=f'{race_details['location']}').grid(padx=10, pady=10, sticky='n')

            # Date and Time
            date_time_str = f"{race_details['date']}"
            ttk.Label(card_frame, text=date_time_str, font=("Arial", 12)).grid(padx=10, pady=10 , sticky='n')

            return card_frame

        else:
            print("Failed to retrieve complete race details or podium.")
            return None  # Explicitly return None if data is incomplete
        

    def next_race_card(self):
        race_details = self.api_handler.get_next_race()
        #print('Next race card:\n', race_details)
        if race_details:
            # Frame for the card
            card_frame = ttk.Labelframe(self, text='NEXT', bootstyle='danger')
            card_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Arial", 16, "bold")).grid(padx=10, pady=10 , sticky='n')

            # Circuit y Location
            ttk.Label(card_frame, text=f"{race_details['circuit']} - {race_details['location']}", font=("Arial", 12)).grid(padx=10, pady=10 , sticky='n')

            # Date and Time
            date_time_str = f"{race_details['date']} - {race_details['time']}"
            ttk.Label(card_frame, text=date_time_str, font=("Arial", 12)).grid(padx=10, pady=10 , sticky='n')
            return card_frame

        else:
            print("Failed to retrieve complete race details or podium.")
            return None  # Explicitly return None if data is incomplete
