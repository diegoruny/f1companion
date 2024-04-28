
import tkinter as tk
from tkinter import ttk
from tkinter import font
# from api.api_handler import ErgastAPI
# from .driver_standings import StandingsView
from .top_Bar import TopBar
from .menu_frame import MenuFrame
from .list_builder import Standings
class Dashboard(tk.Frame):
    def __init__(self, parent,api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent

        #Left Bar
        self.menu_frame = MenuFrame(self)
        self.menu_frame.pack(fill='y', side='left')
        
        # Top Bar
        self.top_bar = TopBar(self, self.api_handler)
        self.top_bar.pack(fill='x', side='right')

        #Drivers Standings

        self.standings_area = Standings(self, self.api_handler)
        self.top_bar.pack(fill='x', side='bottom')
    
        
        # # Botón para cambiar a la vista de clasificaciones, como ejemplo
        # self.standings_button = ttk.Button(self, text="Standings", command=self.show_standings)
        # self.standings_button.pack(pady=10)
    
    # def show_standings(self):
    #     self.pack_forget()  # Oculta el dashboard
    #     standings_view = StandingsView(self.parent)
    #     standings_view.pack(fill=tk.BOTH, expand=True)

