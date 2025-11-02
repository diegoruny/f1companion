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

        last_card = self.last_race_card()
        next_card = self.next_race_card()
        
        if last_card:
            last_card.pack(side='left', padx=10, pady=10, fill='both', expand=True)
        if next_card:
            next_card.pack(side='right', padx=10, pady=10, fill='both', expand=True)

    def last_race_card(self):
        """Create and return a card displaying the last completed race information."""
        race_details, podium = self.api_handler.get_last_race()
        
        # Frame for the card
        card_frame = ttk.Labelframe(self, text='LAST RACE', bootstyle='danger')
        
        if race_details:
            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Helvetica", 16, "bold")).pack(padx=10, pady=10)
            # Circuit and Location
            ttk.Label(card_frame, text=f"{race_details['circuit']}", font=("Helvetica", 12)).pack(padx=10, pady=10)
            ttk.Label(card_frame, text=f"{race_details['location']}", font=('Helvetica', 12)).pack(padx=10, pady=10)
            # Date and Time
            date_time_str = f"{race_details['date']}"
            ttk.Label(card_frame, text=date_time_str, font=("Helvetica", 12)).pack(padx=10, pady=10)
        else:
            # Show placeholder when no data available
            ttk.Label(card_frame, text="No data available", font=("Helvetica", 12, "italic")).pack(padx=10, pady=10)
            ttk.Label(card_frame, text="Check your connection", font=("Helvetica", 10)).pack(padx=10, pady=5)
        
        return card_frame

    def next_race_card(self):
        """Create and return a card displaying the next upcoming race information."""
        race_details = self.api_handler.get_next_race()
        
        # Frame for the card
        card_frame = ttk.Labelframe(self, text='NEXT', bootstyle='danger')

        if race_details:
            # Race Title
            ttk.Label(card_frame, text=f"{race_details['name']}", font=("Helvetica", 16, "bold")).pack(padx=10, pady=10)
            # Circuit and Location
            ttk.Label(card_frame, text=f"{race_details['circuit']} - {race_details['location']}", font=("Helvetica", 12)).pack(padx=10, pady=10)
            # Date and Time
            date_time_str = f"{race_details['date']} - {race_details['time']}"
            ttk.Label(card_frame, text=date_time_str, font=("Helvetica", 12)).pack(padx=10, pady=10)
        else:
            # Show placeholder when no data available
            ttk.Label(card_frame, text="No data available", font=("Helvetica", 12, "italic")).pack(padx=10, pady=10)
            ttk.Label(card_frame, text="Check your connection", font=("Helvetica", 10)).pack(padx=10, pady=5)
        
        return card_frame
