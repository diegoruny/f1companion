import tkinter as tk
from tkinter import ttk
# from ..utils.last_race_sim_data import run_simulation

class NextRaceView(tk.Frame):
    """Widget for displaying last race and next race information cards.
    
    Shows two side-by-side cards: one for the last completed race and one
    for the upcoming race.
    
    Args:
        parent: Parent Tkinter widget
        api_handler: Instance of ErgastAPI for fetching race information
    """
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.api_handler = api_handler

        self.last_race_card().pack(side='left', padx=10, pady=10, fill='both', expand=True)
        self.next_race_card().pack(side='right', padx=10, pady=10, fill='both', expand=True)

    def last_race_card(self):
        """Create and return a card displaying the last completed race information."""
        race_details = self.api_handler.get_last_race()[0]
        if race_details:
            # Frame for the card
            card_frame = ttk.Labelframe(self, text='LAST RACE', bootstyle='danger')
            
            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Helvetica", 16, "bold")).pack(padx=10, pady=10)
            # Circuit and Location
            ttk.Label(card_frame, text=f"{race_details['circuit']}", font=("Helvetica", 12)).pack(padx=10, pady=10)
            ttk.Label(card_frame, text=f"{race_details['location']}", font=('Helvetica', 12)).pack(padx=10, pady=10)
            # Date and Time
            date_time_str = f"{race_details['date']}"
            ttk.Label(card_frame, text=date_time_str, font=("Helvetica", 12)).pack(padx=10, pady=10)
            
            return card_frame
        else:
            return None  # Explicitly return None if data is incomplete

    def next_race_card(self):
        """Create and return a card displaying the next upcoming race information."""
        race_details = self.api_handler.get_next_race()
        if race_details:
            # Frame for the card
            card_frame = ttk.Labelframe(self, text='NEXT', bootstyle='danger')
            card_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Helvetica", 16, "bold")).pack(padx=10, pady=10)
            # Circuit and Location
            ttk.Label(card_frame, text=f"{race_details['circuit']} - {race_details['location']}", font=("Helvetica", 12)).pack(padx=10, pady=10)
            # Date and Time
            date_time_str = f"{race_details['date']} - {race_details['time']}"
            ttk.Label(card_frame, text=date_time_str, font=("Helvetica", 12)).pack(padx=10, pady=10)
            
            return card_frame
        else:
            return None  # Explicitly return None if data is incomplete
