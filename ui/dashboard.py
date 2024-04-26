
import tkinter as tk
from tkinter import ttk
from tkinter import font
# from api.api_handler import ErgastAPI
# from .driver_standings import StandingsView
from .top_Bar import TopBar
class Dashboard(tk.Frame):
    def __init__(self, parent,api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent
        dashboard_Title = ttk.Label(self, text="F1 Race Companion Dashboard", font=("Arial", 20, "bold"))
        #border for design
        dashboard_Title.config(borderwidth=2, relief="solid")
        dashboard_Title.pack(pady=20)
        # Top Bar
        self.top_bar = TopBar(self, self.api_handler)
        self.top_bar.pack(fill=tk.BOTH, expand=True)
    
        
        # # Botón para cambiar a la vista de clasificaciones, como ejemplo
        # self.standings_button = ttk.Button(self, text="Standings", command=self.show_standings)
        # self.standings_button.pack(pady=10)
    
    # def show_standings(self):
    #     self.pack_forget()  # Oculta el dashboard
    #     standings_view = StandingsView(self.parent)
    #     standings_view.pack(fill=tk.BOTH, expand=True)

