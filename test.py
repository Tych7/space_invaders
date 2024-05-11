

import pygame
import sys

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check if there's any joystick connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    sys.exit()

# Initialize the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Check if button 0 is up
    button_0_up = joystick.get_button(0) == 0
    
    # Print the result
    print("Button 0 is up:", button_0_up)

    # You can add your game logic here

    # Optional: Add a small delay to reduce CPU usage
    pygame.time.wait(10)

# Quit Pygame
pygame.quit()