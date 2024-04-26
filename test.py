import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Controller")

controller = pygame.joystick.Joystick(0)

done = False

# Create a red block
block_width = 50
block_height = 50
block_x = 375
block_y = 275

clock = pygame.time.Clock()

while not done:
    window.fill((255, 255, 255))  # Clear the window

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update block position based on joystick axes
    block_x += controller.get_axis(0) * 5  # Left stick horizontal axis
    block_y += controller.get_axis(1) * 5  # Left stick vertical axis

    if controller.get_button(15): pygame.draw.rect(window, (255, 0, 0), [0, 0, 800, 600]) #RED
    if controller.get_button(16): pygame.draw.rect(window, (0, 255, 0), [0, 0, 800, 600]) #GREEN
    # if controller.get_button(17): pygame.draw.rect(window, (0, 0, 255), [0, 0, 800, 600]) #BLUE
    # if controller.get_button(18): pygame.draw.rect(window, (0, 0, 0), [0, 0, 800, 600]) #BLACK
    # if controller.get_button(19): pygame.draw.rect(window, (255, 255, 0), [0, 0, 800, 600]) #YELLOW

    # Clamp block position within window bounds
    block_x = max(0, min(block_x, 800 - block_width))
    block_y = max(0, min(block_y, 600 - block_height))

    # Draw the block
    pygame.draw.rect(window, (255, 0, 0), [block_x, block_y, block_width, block_height])

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
