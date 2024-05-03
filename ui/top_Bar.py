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
        self.top_bar_frame.pack(fill='x', side='top', anchor='ne')

        #Main Image label
        self.main_logo_image = tk.PhotoImage(file="ui/assets/f1_logo.png")
        self.menu_label = ttk.Label(self.top_bar_frame, text='F1 Companion App', image=self.main_logo_image, compound='top', font=("Helvetica", 16))
        self.menu_label.pack(padx=10, pady=10, side='left')

        #Cards for the last and nex race
        NextRaceView(self.top_bar_frame, self.api_handler).pack(side='right', padx=10, pady=10, fill='x', expand=True)