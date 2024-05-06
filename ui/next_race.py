import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

class NextRaceView(tk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.api_handler = api_handler
        
        style = Style(theme='darkly')

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
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Helvetica", 16, "bold")).pack(padx=10, pady=10)

            # Circuit y Location
            ttk.Label(card_frame, text=f"{race_details['circuit']}", font=("Helvetica", 12)).pack(padx=10, pady=10)
            ttk.Label(card_frame, text=f'{race_details['location']}', font=('Helvetica', 12)).pack(padx=10, pady=10)

            # Date and Time
            date_time_str = f"{race_details['date']}"
            ttk.Label(card_frame, text=date_time_str, font=("Helvetica", 12)).pack(padx=10, pady=10)

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
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Helvetica", 16, "bold")).pack(padx=10, pady=10)

            # Circuit y Location
            ttk.Label(card_frame, text=f"{race_details['circuit']} - {race_details['location']}", font=("Helvetica", 12)).pack(padx=10, pady=10)

            # Date and Time
            date_time_str = f"{race_details['date']} - {race_details['time']}"
            ttk.Label(card_frame, text=date_time_str, font=("Helvetica", 12)).pack(padx=10, pady=10)
            return card_frame

        else:
            print("Failed to retrieve complete race details or podium.")
            return None  # Explicitly return None if data is incomplete


    