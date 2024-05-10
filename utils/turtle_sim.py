import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

# Cargar datasets
drivers_df = pd.read_csv('./api/localData/drivers.csv')
results_df = pd.read_csv('./api/localData/results.csv')
constructors_df = pd.read_csv('./api/localData/constructors.csv')
races_df = pd.read_csv('./api/localData/races.csv')
circuits_df = pd.read_csv('./api/localData/circuits.csv')
qualifying_df = pd.read_csv('./api/localData/qualifying.csv')
lap_times_df = pd.read_csv('./api/localData/lap_times.csv')

print(drivers_df.head())
print(results_df.head())
print(constructors_df.head())
print(races_df.head())
print(circuits_df.head())
print(qualifying_df.head())
print(lap_times_df.head())

# Check unique identifiers in each DataFrame to ensure they are correct for merging
print(drivers_df['driverId'].unique())
print(results_df['driverId'].unique())
print(constructors_df['constructorId'].unique())
print(races_df['raceId'].unique())
print(circuits_df['circuitId'].unique())
print(qualifying_df[['raceId', 'driverId', 'constructorId']].drop_duplicates())
print(lap_times_df[['raceId', 'driverId']].drop_duplicates())






# Fusionando datos básicos de carrera
race_details_df = pd.merge(results_df, drivers_df, on='driverId', how='left')
race_details_df = pd.merge(race_details_df, constructors_df[['constructorId', 'constructorRef', 'name']], on='constructorId', how='left', suffixes=('', '_constructor'))
race_details_df = pd.merge(race_details_df, races_df, on='raceId', how='left')
race_details_df = pd.merge(race_details_df, circuits_df, on='circuitId', how='left')
race_details_df = pd.merge(race_details_df, qualifying_df, on=['raceId', 'driverId', 'constructorId'], how='left')

# After each merge, add a print statement to check the DataFrame's size
print("After merging with drivers_df:", race_details_df.shape)
# Continue for each merge step


# Obtener la última carrera basado en la fecha o un identificador máximo
last_race_id = races_df['raceId'].max()

print(races_df[races_df['raceId'] >= races_df['raceId'].max() - 5])  # Checking last few races to verify data integrity


# Filtrar los detalles de la última carrera
last_race_details = race_details_df[race_details_df['raceId'] == last_race_id]

print("Last race ID:", last_race_id)
print("Filtered last race details:", last_race_details.shape)

print("Count of Races:", races_df.shape[0])
print("Count of Results for Last Race:", results_df[results_df['raceId'] == last_race_id].shape[0])

# Example checks
print("Unique Race IDs in Results:", results_df['raceId'].unique())
print("Last Race Details in Results:", results_df[results_df['raceId'] == last_race_id])


# Fusionar con los tiempos por vuelta
final_race_data = pd.merge(last_race_details, lap_times_df, on=['raceId', 'driverId'], how='left')

# Seleccionar columnas relevantes incluyendo los tiempos por vuelta
columns_to_select = ['raceId', 'driverId', 'code', 'surname', 'constructorId', 'constructorRef', 'name', 'grid', 'positionOrder', 'points', 'circuitRef', 'location', 'country', 'lat', 'lng', 'lap', 'time']
final_race_data = final_race_data[columns_to_select]
print(final_race_data[['code', 'constructorRef', 'time']].head())

# Function to create the race simulation
def create_race_simulation(root, race_data):
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
    canvas.pack()

    try:
        image_path = 'utils/sprites/alpine.png'  # Adjust the path as needed
        img = tk.PhotoImage(file=image_path)
        canvas.create_image(100, 100, image=img, anchor='nw')
        print("Image loaded successfully")
    except Exception as e:
        print(f"Failed to load image {image_path}: {e}")

    car_images = {}
    for constructor in race_data['constructorRef'].unique():
        image_path = f'utils/sprites/{constructor.lower()}.png'
        try:
            car_images[constructor] = tk.PhotoImage(file=image_path)
            print(f"Loaded image: {image_path}")
        except tk.TclError as e:
            print(f"Error loading image: {image_path} - {e}")
            continue

    cars = []

    if not car_images:
        print("No images loaded, check paths and files.")

    for index, row in race_data.iterrows():
        y_position = CANVAS_HEIGHT / len(race_data) * index + 20
        constructor = row['constructorRef']
        if constructor in car_images:
            car_image = car_images[constructor]
            car = canvas.create_image(50, y_position, image=car_image, anchor='nw')
            canvas.create_text(10, y_position + 10, text=row['code'], font=('Arial', 12, 'bold'), fill='white', anchor='nw')
            cars.append((car, row['time'].mean()))
        else:
            print(f"No image found for {constructor}")

    def update_positions():
        for car, speed in cars:
            canvas.move(car, 200 - speed / 50, 0)
        root.after(50, update_positions)

    if cars:
        update_positions()
    else:
        print("No cars added to canvas.")

root = tk.Tk()
root.title("Race Simulation")
create_race_simulation(root, final_race_data)
root.mainloop()
