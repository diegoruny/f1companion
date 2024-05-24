import pygame
import pandas as pd
from datetime import datetime
import os

# Constants
WIDTH, HEIGHT = 1500, 700
FPS = 60
START_LINE_Y = 50
FINISH_LINE_Y = HEIGHT - 50
THIRD_WIDTH = WIDTH // 3
HALF_WIDTH = WIDTH // 2
FINISH_LINE_X = WIDTH - 50

# Car class for creating car sprites
class Car(pygame.sprite.Sprite):
    def __init__(self, image, x, y, name, code):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.name = name
        self.code = code
        self.velocity = 0

    # Update the position of the car
    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

# Load data from CSV files
def load_data():
    # Load data from CSV files
    drivers_df = pd.read_csv('./api/localData/drivers.csv', usecols=['driverId', 'driverRef', 'number', 'code'])
    results_df = pd.read_csv('./api/localData/results.csv', usecols=['raceId', 'driverId', 'constructorId', 'statusId'])
    constructors_df = pd.read_csv('./api/localData/constructors.csv', usecols=['constructorId', 'constructorRef'])
    races_df = pd.read_csv('./api/localData/races.csv', usecols=['raceId', 'circuitId', 'date'], parse_dates=['date'])
    lap_times_df = pd.read_csv('./api/localData/lap_times.csv', usecols=['raceId', 'driverId', 'lap', 'position', 'time'])
    circuits_df = pd.read_csv('./api/localData/circuits.csv', usecols=['circuitId', 'circuitRef'])
    qualifying_df = pd.read_csv('./api/localData/qualifying.csv', usecols=['raceId', 'driverId', 'constructorId', 'position'])
    status_df = pd.read_csv('./api/localData/status.csv', usecols=['statusId', 'status'])

    # Filter past races
    past_races = races_df[races_df['date'] <= datetime.now()]
    if past_races.empty:
        print("No past races found.")
        return pd.DataFrame()

    # Get the last race
    last_race = past_races.iloc[-1]
    if last_race['raceId'] not in results_df['raceId'].values:
        latest_race_id = results_df['raceId'].max()
        race_details = results_df[results_df['raceId'] == latest_race_id]
    else:
        race_details = results_df[results_df['raceId'] == last_race['raceId']]

    # Merge dataframes to get race details
    race_details = race_details.merge(races_df, on='raceId')
    race_details = race_details.merge(drivers_df, on='driverId')
    race_details = race_details.merge(constructors_df, on='constructorId')
    race_details = race_details.merge(circuits_df, on='circuitId')
    race_details = race_details.merge(lap_times_df, on=['raceId', 'driverId'], how='left')
    race_details = race_details.merge(qualifying_df, on=['raceId', 'driverId', 'constructorId'], how='left')
    race_details = race_details.merge(status_df, on='statusId')

    # Fill missing positions and convert time to timedelta
    if 'position' not in race_details.columns:
        race_details['position'] = race_details['position_x']
    race_details['time'] = pd.to_timedelta('0:' + race_details['time'].fillna('0:00.000'))

    # Save race details to CSV
    race_details.to_csv("final_race_data2.csv", index=False)

    return race_details

# Load car images
def load_car_images(race_details):
    images = {}
    new_height = 25
    aspect_ratio = 186 / 69

    # Load images for each constructor
    for constructor in race_details['constructorRef'].unique():
        path = f'./utils/sprites/{constructor}.png'
        if os.path.exists(path):
            img = pygame.image.load(path)
            new_width = int(new_height * aspect_ratio)
            resized_img = pygame.transform.scale(img, (new_width, new_height))
            images[constructor] = resized_img
        else:
            print(f"Image not found for constructor {constructor} at path: {path}")

    return images

# Create car sprites
def create_car_sprites(images, race_details):
    car_sprites = pygame.sprite.Group()
    y_pos = 50
    x_pos = 50
    space = 5

    # Create a car sprite for each driver
    unique_drivers = race_details.drop_duplicates(subset=['driverRef', 'constructorRef'])
    for index, row in unique_drivers.iterrows():
        constructor = row['constructorRef']
        driver_name = row['driverRef']
        driver_code = row['code']

        if constructor in images:
            car = Car(images[constructor], x_pos, y_pos, driver_name, driver_code)
            car_sprites.add(car)
            y_pos += images[constructor].get_height() + space
            x_pos -= 5

    return car_sprites

# Easing function for smooth movement
def ease_in_out_quad(t):
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t

# Move cars based on lap data
def move_cars(car_sprites, race_details, elapsed_time, total_duration, race_phase):
    laps = sorted(race_details['lap'].unique())
    num_laps = len(laps)
    if num_laps == 0:
        print("No lap data available.")
        return

    # Calculate current lap and time within lap
    frame_duration = total_duration / num_laps
    current_lap_index = min(int(elapsed_time / frame_duration), num_laps - 1)
    t = (elapsed_time % frame_duration) / frame_duration

    # Get data for current and next lap
    lap_data = race_details[race_details['lap'] == laps[current_lap_index]]
    next_lap_data = race_details[race_details['lap'] == laps[current_lap_index + 1]] if current_lap_index + 1 < num_laps else lap_data

    # Apply easing function
    t = ease_in_out_quad(t)

    # Move each car based on lap data
    for index, row in lap_data.iterrows():
        driver_name = row['driverRef']
        car = next((c for c in car_sprites if c.name == driver_name), None)
        if car:
            new_y = START_LINE_Y + (row['position'] - 1) * 30
            next_row = next_lap_data[next_lap_data['driverRef'] == driver_name]
            if not next_row.empty:
                next_row = next_row.iloc[0]
                next_new_y = START_LINE_Y + (next_row['position'] - 1) * 30

                # Calculate movement based on race phase
                if race_phase == 'start':
                    dx = (THIRD_WIDTH - car.rect.x) * t
                elif race_phase == 'middle':
                    dx = 0
                elif race_phase == 'end':
                    dx = (FINISH_LINE_X - car.rect.x) * t
                else:
                    dx = 0

                dy = (next_new_y - car.rect.y) * t
                car.update(dx, dy)

# Run the simulation
def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("F1 Race Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    # Load race data
    race_details = load_data()
    if race_details.empty:
        print("Race details are empty. Exiting.")
        return

    # Load car images and create car sprites
    images = load_car_images(race_details)
    car_sprites = create_car_sprites(images, race_details)

    total_duration = 60  # Duration of the simulation in seconds
    elapsed_time = 0
    phase_duration = 10  # Duration of each phase in seconds

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((169, 169, 169))  # Dark gray background

        # Draw start and finish lines
        pygame.draw.line(screen, (255, 255, 255), (0, START_LINE_Y), (WIDTH, START_LINE_Y), 5)
        pygame.draw.line(screen, (255, 255, 255), (0, FINISH_LINE_Y), (WIDTH, FINISH_LINE_Y), 5)

        # Determine race phase
        if elapsed_time < phase_duration:
            race_phase = 'start'
        elif elapsed_time < total_duration - phase_duration:
            race_phase = 'middle'
        else:
            race_phase = 'end'

        # Move cars and draw them
        move_cars(car_sprites, race_details, elapsed_time, total_duration, race_phase)
        car_sprites.draw(screen)

        # Update and display current lap
        current_lap = min(int(elapsed_time / (total_duration / len(race_details['lap'].unique()))), len(race_details['lap'].unique()))
        lap_text = font.render(f"Lap: {current_lap + 1}", True, (255, 255, 255))
        screen.blit(lap_text, (WIDTH // 2 - lap_text.get_width() // 2, 10))

        pygame.display.flip()
        clock.tick(FPS)
        elapsed_time += clock.get_time() / 1000  # Update elapsed time in seconds

    pygame.quit()

if __name__ == '__main__':
    run_simulation()