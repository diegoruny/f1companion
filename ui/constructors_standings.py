import tkinter as tk
from tkinter import ttk

class Constructor_standings(tk.Frame):
    """Widget for displaying constructor championship standings.
    
    Displays a table with constructor position, name, points, and wins.
    
    Args:
        parent: Parent Tkinter widget
        api_handler: Instance of ErgastAPI for fetching constructor standings
    """
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.setup_ui()

    def setup_ui(self):
        """Initialize and configure the standings table UI."""
        # Create table headers
        columns = ('Position', 'Constructor', 'Points', 'Wins')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        self.tree.pack(expand=True, fill='both')

        # Fetch and display the data
        self.update_standings()

    def update_standings(self):
        """Fetch and populate the constructor standings table with data from the API."""
        standings = self.api_handler.get_constructors_championship()
        for row in standings.itertuples():
            self.tree.insert("", "end", values=(row.Position, row.Constructor, row.Points, row.Wins))
