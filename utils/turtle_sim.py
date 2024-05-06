# # Setup the main window and canvas
# import tkinter as tk
# from tkinter import Canvas, PhotoImage
# from cars import Car

# root = tk.Tk()
# canvas = Canvas(root, width=800, height=600, bg='dark gray')
# canvas.pack()

# class Background:
#     def __init__(self, canvas, image_path):
#         self.canvas = canvas
#         self.image = PhotoImage(file=image_path)
#         self.id = canvas.create_image(0, 0, image=self.image, anchor='nw')
#         self.width = self.image.width()

#     def scroll(self, speed):
#         self.canvas.move(self.id, -speed, 0)
#         x1 = self.canvas.coords(self.id)[0]
#         if x1 <= -self.width:
#             self.canvas.move(self.id, self.width, 0)

# image_paths = {
#     'redbull': 'utils/sprites/redbull.png',
#     'ferrari': 'utils/sprites/ferrari.png',
#     'mercedes': 'utils/sprites/mercedes.png',
#     'mclaren': 'utils/sprites/mclaren.png',
#     'williams': 'utils/sprites/williams.png',
#     'rb': 'utils/sprites/rb.png',
#     'sauber': 'utils/sprites/sauber.png',
#     'haas': 'utils/sprites/haas.png',
#     'aston_martin': 'utils/sprites/aston_martin.png',
#     'alpine': 'utils/sprites/alpine.png',
# }
# # or it can be a 
    

# for i in range(20):
#     team = 
#     Car(canvas, 100, 100 + i * 50, 'redbull', 'PER', f'utils/sprites/{team}.png')
    

# # Create car and background objects
# bg = Background(canvas, 'utils/sprites/background.png')
# car = Car(canvas, 100, 250, 'redbull', 'PER', image_paths)

# def update():
#     bg.scroll(5)  # Scroll background by 5 pixels
#     car.move(0, 0)  # Update car's position, set dx, dy according to need
#     root.after(50, update)  # Continue to update every 50 milliseconds

# update()  # Start the animation loop
# root.mainloop()  # Start the GUI loop


import tkinter as tk

# Constants
NUM_CARS = 20
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500

def create_race_simulation(root, car_data):
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
    canvas.pack()

    # Load car images and create car image objects on the canvas
    car_images = {team: tk.PhotoImage(file=path) for team, path in car_data['images'].items()}
    cars = []
    for i in range(NUM_CARS):
        team = car_data['teams'][i]
        driver_code = car_data['codes'][i]
        y_position = CANVAS_HEIGHT / NUM_CARS * i + 20
        # Create the car image
        car_image = car_images[team]
        car = canvas.create_image(50, y_position, image=car_image, anchor='nw')
        # Create text for the driver code
        canvas.create_text(10, y_position + 10, text=driver_code, font=('Arial', 12, 'bold'), fill='white', anchor='nw')
        cars.append(car)
    
    def update_positions():
        for i, car in enumerate(cars):
            # Simulate movement based on dynamic factors or static for illustration
            canvas.move(car, 2, 0)
        root.after(50, update_positions)

    update_positions()

root = tk.Tk()
root.title("Race Simulation")

# Data structure for car images and teams
car_data = {
    'images': {
        'RedBull': 'path_to_redbull_image.png',
        'Mercedes': 'path_to_mercedes_image.png',
        # Add paths for all teams
    },
    'teams': ['RedBull', 'Mercedes'] * 10,  # Example: Adjust based on actual team assignments
    'codes': ['VER', 'HAM'] * 10  # Example: Adjust based on actual driver codes
}

create_race_simulation(root, car_data)
root.mainloop()
