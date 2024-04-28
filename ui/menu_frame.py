import tkinter as tk
import tkinter.ttk as ttk

class MenuFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.parent

        # Create a label for the menu
        self.main_logo_image = tk.PhotoImage(file="ui/assets/f1_logo.png")
        self.menu_label = ttk.Label(self, text='F1 Companion App', image=self.main_logo_image, compound='top')
        self.menu_label.pack(padx=10, pady=10)
        

        self.menu_text = ttk.Label(self, text="F1 Label", font=("Helvetica", 16))
        self.menu_text.pack(pady=10)