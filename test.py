import pygame
import sys

# Define some colors


class Button:
    def __init__(self, x, y, width, height, text, font_size, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)
        
        if mouse_over:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 3, border_radius=10)
        font = pygame.font.SysFont('couriernew', self.font_size, True)
        renderd_text = font.render(self.text, 1, (4, 245, 4))

        text_x = (self.width / 2) - (font.size(self.text)[0] / 2)
        text_y = (self.height / 2) - (font.size(self.text)[1] / 2)

        screen.blit(renderd_text, (self.x + text_x, self.y + text_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Clickable Buttons in Pygame")

# Create buttons
button1 = Button(100, 100, 200, 50, "Button 1", 30, lambda: print("Button 1 clicked"))
button2 = Button(100, 200, 200, 50, "Button 2", 30, lambda: print("Button 2 clicked"))

buttons = [button1, button2]

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for button in buttons:
            button.handle_event(event)

    # Fill the screen with background color
    screen.fill((255,255,255))

    # Draw buttons
    for button in buttons:
        button.draw(screen)

    # Update the display
    pygame.display.flip()
