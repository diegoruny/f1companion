import tkinter as tk
from tkinter import ttk
from api.api_handler import ErgastAPI

class StandingsView(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        ttk.Label(self, text="Clasificaciones de Pilotos").pack(pady=10)
        self.standings_area = ttk.Frame(self)

        self.standings_data = ErgastAPI().get_driver_standings()
        print(self.standings_data)
    
        for driver in self.standings_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']:   
            entry_frame = tk.Frame(self.standings_area)
            entry_frame.pack(fill='x')

            # Populate the entry with data
            tk.Label(entry_frame, text=driver['position']).pack(side='left')
            tk.Label(entry_frame, text=driver['name']).pack(side='left')
            tk.Label(entry_frame, text=driver['team']).pack(side='left')
            tk.Label(entry_frame, text=f"{driver['points']} pts").pack(side='left')
        

    
print(ErgastAPI().get_driver_standings())
