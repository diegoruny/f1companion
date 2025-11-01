
import tkinter as tk

from ui.constructors_standings import Constructor_standings
from .top_Bar import TopBar
from .list_builder import Driver_standings
from tkinter import ttk
from ttkbootstrap import Notebook

class Dashboard(tk.Frame):
    """Main dashboard container for the F1 Race Companion application.
    
    Displays the top navigation bar with race information and tabbed interface
    containing driver standings and constructor standings.
    
    Args:
        parent: Parent Tkinter widget
        api_handler: Instance of ErgastAPI for fetching race data
    """
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent

        # Top Bar
        self.top_bar = TopBar(self, self.api_handler)
        self.top_bar.pack(fill='x', side='top', anchor='ne', padx=10, pady=10)
        
        #Content Section on notebooks
        notebook_frame = Notebook(self, bootstyle='dark')
        notebook_frame.pack(fill='both', expand=True, padx=10, pady=10, side='bottom')

        tab1 = ttk.Frame(notebook_frame)
        tab2 = ttk.Frame(notebook_frame)

        notebook_frame.add(tab1, text='Driver Standings')
        notebook_frame.add(tab2, text='Constructor Standings')


        #Drivers Standings

        standings_area = Driver_standings(tab1, self.api_handler)
        standings_area.pack()

        # Adding Constructor Standings to tab2
        constructor_standings_area = Constructor_standings(tab2, self.api_handler)
        constructor_standings_area.pack()

    
        
