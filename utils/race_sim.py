import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("F1 Race Visualization")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (230, 230, 230)
DARK_GRAY = (100, 100, 100)
BG_COLOR = (71, 73, 80)

# Clock to control the frame rate
clock = pygame.time.Clock()

# Initial background position
background_x = 0

# Car positions (static for now)
car_positions = [(screen_width // 3, screen_height // 2 + i * 50) for i in range(5)]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the background
    background_x -= 2
    if background_x < -screen_width:
        background_x = 0

    # Fill the screen with black
    screen.fill(BG_COLOR)

    # Draw the lines that will divide the laps and the start/finish line)
    pygame.draw.line(screen, GRAY, (background_x, 0), (background_x, screen_height), 2)
    
    pygame.draw.line(screen, GRAY, (background_x + screen_width // 2, 0), (background_x + screen_width // 2, screen_height), 2)

    # Draw static cars using the image of the car loaded from the disk for each car position
    
    
    for pos in car_positions:
        sprite_path = os.path.join(os.path.dirname(__file__), "sprites", "williams.bmp")
        screen.blit(pygame.image.load(sprite_path), (50, 30))
        pygame.draw.rect(screen, WHITE, pygame.Rect(pos[0], pos[1], 50, 30))


    # Update the display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
