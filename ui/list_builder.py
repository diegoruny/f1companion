import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.constants import * 


class Standings(ttk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.api_handler = api_handler
        ttk.Label(self, text="Clasificaciones de Pilotos").pack(pady=10)
        self.standings_area = ttk.Frame(self)

        self.drivers_data = self.api_handler.get_driver_standings()
        print("self.drivers_data in Standings", self.drivers_data)

        # #Scrollable frame
        # self.sf = ScrolledFrame(self.parent, autohide=True, style='dark.TFrame', bootstyle='ligth-round')
        # self.sf.pack(fill=BOTH, expand=YES, padx=0, pady=0)

        
        # Create sample driver entries
        # self.drivers = 

        team_colors = {
            'red_bull': '#1E41FF',  # Un azul distintivo
            'mercedes': '#00D2BE',  # Un turquesa brillante
            'ferrari': '#DC0000',   # Rojo Ferrari
            'mclaren': '#FF8700',   # Naranja McLaren
            'aston_martin': '#006F62',  # Verde oscuro de Aston Martin
            'alpine': '#0090FF',    # Azul de Alpine
            'sauber': '#900000',  # Rojo oscuro
            'haas': '#E6002B',      # Blanco (o puede usar un gris oscuro)
            'williams': '#005AFF',  # Azul de Williams
            'rb': '#2B4562',  # Azul marino
        }

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
                #Get the team color
                team_name = driver['TEAM']['name']
                team_id = driver['TEAM']['teamId']
                color = team_colors.get(team_id, '#FFFFFF')
                print('\nTeamId: ', team_id, '\nTeam name: ', team_name, '\nTeam color: ', color, )
                #Insert the row info
                tree.insert('', 'end', values=(
                    driver['POS'],
                    driver['NAME'],
                    driver['NATIONALITY'],
                    driver['TEAM']['name'],
                    driver['PTS']
                ), tags=(team_id,))

                #style the rows to use the team color
                tree.tag_configure(team_id, background=color)

            # Add a scrollbar
            scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview, bootstyle='round')
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side='right', fill='y')

            tree.pack(fill='both', expand=True)
        create_standings_table(self.parent, self.drivers_data)

        # Crear un widget para cada piloto
        # def drivers_list(driver_standings):
        #     """
        #         this function get the dicctionary of the drivers standings and return 
        #         a string with the rounded picture of the driver his lastname and name of, and the 
        #         with a background color of the team that is on a dictionary above
        #     """
        #     print(f'Drivers Standings on func drivers_list {driver_standings}\n')
        #     for driver in driver_standings:
        #         print(driver)
        #         color = team_colors.get(driver['TEAM'])
        #         driver_frame = ttk.Label(self.sf, bootstyle='light', background=color)
        #         driver_position = ttk.Label(driver_frame, text=driver['POS'], bootstyle='inverse', background=color, font=(None, 14))
        #         driver_position.grid(pady=0, padx=0, row=0, column=0, sticky='w')
        #         driver_label = ttk.Label(driver_frame, text=driver['NAME'], bootstyle='inverse', background=color,  font=(None, 14))
        #         driver_label.grid(pady=0, padx=0, row=0, column=1, sticky='w')
                
        #         driver_frame.pack(padx=(10, 20), pady=5, fill='x')

        # drivers_list(self.drivers_data)

        
        # Crear un widget para cada equipo

        # for team, color in team_colors.items():

        #     team_frame = ttk.Frame(self.sf, bootstyle='secondary')
        #     team_label = ttk.Label(team_frame, text=team, bootstyle='dark', background=color, width=50)
        #     team_label.pack(pady=0, padx=0, fill=X)
        #     team_frame.pack(padx=10, pady=5, fill=X)
