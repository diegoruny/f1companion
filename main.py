import tkinter as tk
from ui.dashboard import Dashboard
import sv_ttk
from api.api_handler import ErgastAPI

def main():
    root = tk.Tk()
    root.title('F1 Race Companion')
    root.geometry("1024x768")
    # Use the silicon_valley dark theme for the ttk widgets
    sv_ttk.use_dark_theme()

    # Create an instance of the API handler
    api_handler = ErgastAPI()
    
    # Launch and shows the dashboard
    dashboard_frame = Dashboard(root, api_handler)
    dashboard_frame.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()
