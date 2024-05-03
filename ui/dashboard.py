
import tkinter as tk
from .top_Bar import TopBar
from .list_builder import Standings
from tkinter import ttk
from ttkbootstrap import Notebook
class Dashboard(tk.Frame):
    def __init__(self, parent,api_handler, *args, **kwargs):
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

        notebook_frame.add(tab1, text='Driver Stantings')
        notebook_frame.add(tab2, text='Constructor Standings')


        #Drivers Standings

        standings_area = Standings(tab1, self.api_handler)
        standings_area.pack()
    
        
