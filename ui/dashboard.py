
import tkinter as tk
from .top_Bar import TopBar
from .list_builder import Standings
class Dashboard(tk.Frame):
    def __init__(self, parent,api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent

        # Top Bar
        self.top_bar = TopBar(self, self.api_handler)
        self.top_bar.pack(fill='x', side='top', anchor='ne')
        
        #Drivers Standings

        self.standings_area = Standings(self, self.api_handler)
        self.standings_area.pack(fill='x', side='bottom', anchor='se')
    
        
