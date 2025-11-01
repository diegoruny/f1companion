"""F1 Race Companion - Main Entry Point

A desktop application for viewing Formula 1 racing information including
driver standings, constructor standings, and upcoming race details.
"""

import tkinter as tk
from ui.dashboard import Dashboard
import sv_ttk
from api.api_handler import ErgastAPI


def main():
    """Initialize and launch the F1 Race Companion application.
    
    Creates the main window, initializes the API handler, and displays
    the dashboard interface.
    """
    root = tk.Tk()
    root.title('F1 Race Companion')
    root.geometry("1024x768")

    # Create an instance of the API handler
    api_handler = ErgastAPI()
    
    # Launch and show the dashboard
    dashboard_frame = Dashboard(root, api_handler)
    dashboard_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()
