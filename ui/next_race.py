import tkinter as tk
from tkinter import ttk
from api.api_handler import ErgastAPI

class NextRaceView(tk.Frame):
    def __init__(self, parent, api_handler, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.api_handler = api_handler
        self.init_ui()

    def init_ui(self):
        race_details = self.api_handler.get_next_race()
        if race_details:
            # Crear un Frame para la tarjeta
            card_frame = ttk.Frame(self, padding="10", relief="raised")
            card_frame.pack(padx=10, pady=10, fill="both", expand=True)

            # Título de la carrera
            ttk.Label(card_frame, text=race_details["name"], font=("Arial", 16, "bold")).pack()

            # Circuito y Ubicación
            ttk.Label(card_frame, text=f"Circuito: {race_details['circuit']} - {race_details['location']}", font=("Arial", 12)).pack()

            # Fecha y Hora
            date_time_str = f"Fecha: {race_details['date']} - Hora: {race_details['time']}"
            ttk.Label(card_frame, text=date_time_str, font=("Arial", 12)).pack()
