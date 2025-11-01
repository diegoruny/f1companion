import tkinter as tk
from tkinter import ttk
from .next_race import NextRaceView

class TopBar(ttk.Frame):
    """Top navigation bar widget for the F1 Race Companion application.
    
    Displays the F1 logo, refresh button, and race information cards (last race and next race).
    
    Args:
        parent: Parent Tkinter widget
        api_handler: Instance of ErgastAPI for fetching race information
    """
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.parent = parent

        # Frame container for both the last and the next race
        self.top_bar_frame = ttk.Frame(self)
        self.top_bar_frame.pack(fill='x', side='top', anchor='ne')

        #Main Image label
        self.main_logo_image = tk.PhotoImage(file="ui/assets/f1_logo.png")
        self.menu_label = ttk.Label(self.top_bar_frame, text='F1 Companion App', image=self.main_logo_image, compound='top', font=("Helvetica", 16))
        self.menu_label.pack(padx=10, pady=10, side='left')

        # Refresh button frame
        refresh_frame = ttk.Frame(self.top_bar_frame)
        refresh_frame.pack(side='left', padx=5, pady=5)
        
        self.refresh_button = ttk.Button(
            refresh_frame,
            text="🔄 Refresh",
            command=self.refresh_data,
            bootstyle='info-outline'
        )
        self.refresh_button.pack(pady=5)
        
        # Cache status label
        self.status_label = ttk.Label(
            refresh_frame,
            text="",
            font=("Helvetica", 9),
            foreground='gray'
        )
        self.status_label.pack()
        self.update_status()

        #Cards for the last and next race
        self.race_view = NextRaceView(self.top_bar_frame, self.api_handler)
        self.race_view.pack(side='right', padx=10, pady=10, fill='x', expand=True)
    
    def refresh_data(self):
        """Manually refresh all data from API."""
        self.refresh_button.config(state='disabled', text="🔄 Refreshing...")
        self.status_label.config(text="Refreshing data...")
        self.parent.update()
        
        try:
            self.api_handler.refresh_all_data()
            # Refresh the race view
            self.race_view.destroy()
            self.race_view = NextRaceView(self.top_bar_frame, self.api_handler)
            self.race_view.pack(side='right', padx=10, pady=10, fill='x', expand=True)
            self.status_label.config(text="✓ Data refreshed", foreground='green')
        except Exception as e:
            self.status_label.config(text="✗ Refresh failed", foreground='red')
            import logging
            logging.error(f"Refresh failed: {e}")
        finally:
            self.refresh_button.config(state='normal', text="🔄 Refresh")
            self.parent.after(3000, self.update_status)  # Reset status after 3 seconds
    
    def update_status(self):
        """Update the cache status display."""
        try:
            status = self.api_handler.get_cache_status()
            # Show most recent update time
            last_update = None
            for key, info in status.items():
                if info['last_update']:
                    if not last_update or info['last_update'] > last_update:
                        last_update = info['last_update']
            
            if last_update:
                from datetime import datetime
                update_time = datetime.fromisoformat(last_update)
                time_diff = datetime.now() - update_time
                hours_ago = int(time_diff.total_seconds() / 3600)
                if hours_ago < 1:
                    status_text = "Updated <1h ago"
                elif hours_ago < 24:
                    status_text = f"Updated {hours_ago}h ago"
                else:
                    days_ago = int(hours_ago / 24)
                    status_text = f"Updated {days_ago}d ago"
                self.status_label.config(text=status_text, foreground='gray')
            else:
                self.status_label.config(text="No cache", foreground='gray')
        except Exception:
            pass  # Silently fail if status can't be retrieved