import pandas as pd
from datetime import datetime
import tkinter as tk
import os
from PIL import Image, ImageTk

class Car:
    def __init__(self, canvas, image, x, y, name, code):
        self.canvas = canvas
        self.image = image
        self.sprite = canvas.create_image(x, y, image=image, anchor='nw')
        self.name = name
        self.x = x
        self.y = y
        self.code = code
        # Displaying the driver code next to the car sprite
        self.label = canvas.create_text(x + image.width() + 25, y + image.height() / 2, text=f"[{self.code}]", fill="white", font=("Helvetica", 12))
    
    def move(self, dx, dy):
        """Method to move the car on the canvas."""
        self.x += dx
        self.y += dy
        # self.speed = speed #Valocidad de movimiento del carro 0 a 2 siendo 2 la velocidad maxima verificar
        self.canvas.move(self.sprite, dx, dy)
        self.canvas.move(self.label, dx, dy)

def load_data():
    

    # Cargar sólo las columnas necesarias y convertir fechas directamente
    drivers_df = pd.read_csv('./api/localData/drivers.csv', usecols=['driverId', 'driverRef', 'number', 'code'])
    results_df = pd.read_csv('./api/localData/results.csv', usecols=['raceId', 'driverId', 'constructorId', 'statusId'])
    constructors_df = pd.read_csv('./api/localData/constructors.csv', usecols=['constructorId', 'constructorRef'])
    races_df = pd.read_csv('./api/localData/races.csv', usecols=['raceId', 'circuitId', 'date'], parse_dates=['date'])
    lap_times_df = pd.read_csv('./api/localData/lap_times.csv', usecols=['raceId', 'driverId', 'lap', 'position', 'time'])
    circuits_df = pd.read_csv('./api/localData/circuits.csv', usecols=['circuitId', 'circuitRef'])
    qualifying_df = pd.read_csv('./api/localData/qualifying.csv', usecols=['raceId', 'driverId', 'constructorId', 'position'])
    status_df = pd.read_csv('./api/localData/status.csv', usecols=['statusId', 'status'])

    # Filtrar la última carrera que ya ocurrió
    last_race = races_df[races_df['date'] <= datetime.now()].iloc[-1]

    # Fusiones eficientes
    race_details = results_df[results_df['raceId'] == last_race['raceId']]
    race_details = race_details.merge(races_df, on='raceId')
    race_details = race_details.merge(drivers_df, on='driverId')
    race_details = race_details.merge(constructors_df, on='constructorId')
    race_details = race_details.merge(circuits_df, on='circuitId')
    race_details = race_details.merge(lap_times_df, on=['raceId', 'driverId'], how='left')
    race_details = race_details.merge(qualifying_df, on=['raceId', 'driverId', 'constructorId'], how='left')
    race_details = race_details.merge(status_df, on='statusId')

    # Guardar datos procesados
    race_details.to_csv("final_race_data2.csv", index=False)

    return race_details


def setup_canvas(root):
    """
    Sets up the tkinter canvas.
    """
    canvas_width = 1500
    canvas_height = 700
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="dark gray")
    canvas.pack()
    return canvas

def load_car_images(race_details):

    images = {}
    new_height = 25  # New height to fit 20 cars vertically
    aspect_ratio = 186 / 69  # Original width to height ratio

    for constructor in race_details['constructorRef'].unique():
        path = f'./utils/sprites/{constructor}.png'
        if os.path.exists(path):
            with Image.open(path) as img:
                new_width = int(new_height * aspect_ratio)  # Calculate new width to maintain aspect ratio
                # Use Image.Resampling.LANCZOS instead of Image.ANTIALIAS
                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                images[constructor] = ImageTk.PhotoImage(resized_img)
                print(f"Loaded and resized image for {constructor}")
        else:
            print(f"Image not found for constructor {constructor} at path: {path}")

    return images




def create_car_sprites(canvas, images, race_details):
    car_sprites = {}
    y_pos = 50  # Initial y position for the first car sprite
    x_pos = 50  # Initial x position for all car sprites
    space = 5  # Space between cars for visibility

    unique_drivers = race_details.drop_duplicates(subset=['driverRef', 'constructorRef'])
    print(f"Creating car sprites for {len(unique_drivers)} unique drivers.")
    # Iterate over each row in race_details to create a sprite for each driver
    for index, row in unique_drivers.iterrows():
        constructor = row['constructorRef']
        driver_name = row['driverRef']  
        driver_code = row['code']
        print(f"Processing {driver_name} in {constructor}")

        if constructor in images:
            car = Car(canvas, images[constructor], x_pos, y_pos, driver_name, driver_code)
            car_sprites[driver_name] = car
            y_pos += images[constructor].height() + space  # Adjust y position for the next car

            
        else:
            print(f"No image available for {constructor}")

    print(f"Created {len(car_sprites)} car sprites.")
    return car_sprites



def move_cars(car_sprites, canvas, race_details):
    lap_data = race_details[['driverRef', 'lap', 'position_x', 'time']].drop_duplicates()
    total_width = canvas.winfo_width()
    start_x = 50
    car_width = next(iter(car_sprites.values())).image.width()
    edge_buffer = 20  # Buffer to stop before the edge of the canvas
    max_x = total_width - car_width - edge_buffer

    # This dict maps current positions to y-coordinates
    y_positions_coordinates = {i + 1: 50 + i * 30 for i in range(len(car_sprites))}

    def animate(lap=1):
        nonlocal car_sprites
        if lap > lap_data['lap'].max():
            return  # Stops the animation after the last lap

        current_lap_data = lap_data[lap_data['lap'] == lap]
        for car in car_sprites.values():
            driver_lap_data = current_lap_data[current_lap_data['driverRef'] == car.name]
            if not driver_lap_data.empty:
                new_position = int(driver_lap_data['position_x'].iloc[0])
                new_y = y_positions_coordinates[new_position]
                race_details['time'] = pd.to_timedelta('0:' + race_details['time'])
                race_details['speed'] = max_x / race_details['time'].dt.total_seconds()

                # Move the car to the new position and adjust speed
                car.move(speed_adjustment if car.x + speed_adjustment < max_x else 0, new_y - car.y)

        canvas.after(50, animate, lap + 1)

    animate()  # Start the animation




def main():
    """
    Main function to run the simulation.
    """
    root = tk.Tk()
    root.title("F1 Race Simulation")
    canvas = setup_canvas(root)
    
    race_details = load_data()
    images = load_car_images(race_details)
    car_sprites = create_car_sprites(canvas, images, race_details)
    
    move_cars(car_sprites, canvas, race_details)
    root.mainloop()

if __name__ == '__main__':
    main()