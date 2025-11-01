import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import * 


class Driver_standings(ttk.Frame):
    """Widget for displaying driver championship standings.
    
    Displays a table with driver position, name, nationality, team, and points.
    
    Args:
        parent: Parent Tkinter widget
        api_handler: Instance of ErgastAPI for fetching driver standings
    """
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.api_handler = api_handler
        self.standings_area = ttk.Frame(self)
        self.drivers_data = self.api_handler.get_driver_standings()

        table_title = ttk.Label(self.parent, text="DRIVERS STANDINGS", font=('Helvetica', 22), bootstyle='inverse-danger').pack(pady=10)
        

        def create_standings_table(parent, driver_standings):

            # Define the columns
            columns = ('pos', 'name', 'nationality', 'team', 'pts')
            tree = ttk.Treeview(parent, columns=columns, show='headings', bootstyle='danger-inverted')

            # Define the column headings
            tree.heading('pos', text='POS', anchor='w', )
            tree.heading('name', text='DRIVER', anchor='w')
            tree.heading('nationality', text='NATIONALITY', anchor='w')
            tree.heading('team', text='TEAM', anchor='w')
            tree.heading('pts', text='PTS', anchor='w')

            # Adjust the column widths to the content
            tree.column('pos', width=50)
            tree.column('name', width=150)
            tree.column('nationality', width=150)
            tree.column('team', width=150)
            tree.column('pts', width=50)

            # Insert the driver data
            for driver in driver_standings:
                
                #Get the driver position
                position = driver['POS']
                
                #Insert the row info
                tree.insert('', 'end', values=(
                    driver['POS'],
                    driver['NAME'],
                    driver['NATIONALITY'],
                    driver['TEAM']['name'],
                    driver['PTS']
                ), tags=(position,))                

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview, bootstyle='round')
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side='right', fill='y')

            tree.pack(fill='both', expand=True)
        create_standings_table(self.parent, self.drivers_data)
