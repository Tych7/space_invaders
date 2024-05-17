import pygame
import json
import math

class Button:
    ratio = 0
    controller = None

    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)	


    def __init__(self, x, y, width, height, text, font_size, action, image=None):
        self.set_ratio()
        self.x = x * self.ratio
        self.y = y * self.ratio
        self.width = width * self.ratio
        self.height = height * self.ratio
        self.text = text
        self.font_size = font_size
        self.action = action
        self.image = image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_event(self, event):
        raise NotImplementedError("Subclasses must implement handle_event.")

    def draw(self, win):
        raise NotImplementedError("Subclasses must implement draw.")


class RectButton(Button):
    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), self.rect, 0, border_radius=int(22 * self.ratio))

        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)
        if mouse_over: pygame.draw.rect(win, (255, 140 ,68), self.rect, int(6 * self.ratio), border_radius=int(22 * self.ratio))
        else: pygame.draw.rect(win, (195, 195, 195), self.rect, int(6 * self.ratio), border_radius=int(22 * self.ratio))

        font_size = int(self.font_size * min(self.ratio, self.ratio))
        font = pygame.font.SysFont('couriernew', font_size, True)

        renderd_text = font.render(self.text, 1, (112, 228, 209))
        text_x = (self.width / 2) - (font.size(self.text)[0] / 2)
        text_y = (self.height / 2) - (font.size(self.text)[1] / 2)
        win.blit(renderd_text, (self.x + text_x, self.y + text_y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


class CircleButton(Button):
    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.width)
        image_width, image_height = self.image.get_size()
        centered_x = self.x - (image_width / 2)
        centered_y = self.y - (image_height / 2)
        win.blit(self.image, (centered_x, centered_y))

        mouse_pos = pygame.mouse.get_pos()
        distance_mouse = math.sqrt((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)
        mouse_over = distance_mouse <= self.width
        if mouse_over: pygame.draw.circle(win, (255, 140 ,68), (self.x, self.y), self.width, int(6 * self.ratio))
        else: pygame.draw.circle(win, (195, 195, 195), (self.x, self.y), self.width, int(6 * self.ratio))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            distance = math.sqrt((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)
            if distance <= self.width:	
                self.action()


class SwitchButton(Button):
    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), self.rect, 0, border_radius=int(22 * self.ratio))
        pygame.draw.rect(win, (195, 195, 195), self.rect, int(5 * self.ratio), border_radius=int(22 * self.ratio))
        font_size = int(self.font_size * min(self.ratio, self.ratio))
        font = pygame.font.SysFont('couriernew', font_size, True)
        text = ""
        text_y = (self.height / 2) - (font.size(self.text)[1] / 2)

        lable_text = font.render(self.text + ":", 1, (112, 228, 209))
        win.blit(lable_text, (self.x - (100 * self.ratio), self.y + text_y))

        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)
        if mouse_over: pygame.draw.rect(win, (255, 140 ,68), self.rect, int(6 * self.ratio), border_radius=int(22 * self.ratio))
        else: pygame.draw.rect(win, (195, 195, 195), self.rect, int(6 * self.ratio), border_radius=int(22 * self.ratio))

        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data[self.text] == "true": 
                text = "ON"
                renderd_text = font.render(text, 1, (4, 245, 4))
                pygame.draw.circle(win, (195, 195, 195), (self.x + (20 * self.ratio), self.y + self.height/2), (12 * self.ratio))
                win.blit(renderd_text, (self.x + (50 * self.ratio), self.y + text_y))
            else: 
                text = "OFF"
                renderd_text = font.render(text, 1, (255, 0, 0))
                pygame.draw.circle(win, (195, 195, 195), (self.x + (80 * self.ratio), self.y + self.height/2), (12 * self.ratio))
                win.blit(renderd_text, (self.x + (10 * self.ratio), self.y + text_y + (3 * self.ratio)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

class controller_pointer():
    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)


    def __init__(self, x, y, radius):
        self.set_ratio()
        self.x = x
        self.y = y
        self.radius = radius
        self.con_x_lock = False
        self.con_y_lock = False
        self.button_lock = False


    def draw(self, win, buttons):
        if pygame.joystick.get_count() > 0:
            #pygame.draw.circle(win, (255, 0, 0), (self.x, self.y), int(self.radius * self.ratio)) #pointer
            for button in buttons:
                if isinstance(button, CircleButton):
                    distance = math.sqrt((self.x - button.x) ** 2 + (self.y - button.y) ** 2)
                    if distance <= self.radius + button.width:
                        pygame.draw.circle(win, (255, 140 ,68), (button.x, button.y), button.width, int(6 * button.ratio))
                elif isinstance(button, RectButton) or isinstance(button, SwitchButton):
                    if button.rect.collidepoint((self.x, self.y)):
                        pygame.draw.rect(win, (255, 140 ,68), button.rect, int(6 * button.ratio), border_radius=int(22 * button.ratio))

    def move_pointer(self, buttons):
        button_positions = []
        for button in buttons:
            if isinstance(button, CircleButton):
                button_positions.append((button.x, button.y))
            elif isinstance(button, RectButton) or isinstance(button, SwitchButton):
                x_center = button.x + (button.width / 2)
                y_center = button.y + (button.height / 2)
                button_positions.append((x_center, y_center))

        if pygame.joystick.get_count() > 0:
            
            y_dif = float('inf')
            x_dif = float('inf')

            new_y = self.y
            new_x = self.x

            if (self.controller.get_button(11) and self.button_lock == False) or (self.controller.get_axis(1) < -0.5 and self.con_y_lock == False): # Up
                for position in button_positions:
                    if (position[1] < self.y) and ((self.y - position[1]) + abs(self.x - position[0])) < y_dif:  
                        y_dif = ((self.y - position[1]) + abs(self.x - position[0]))
                        new_x = position[0]
                        new_y = position[1]
            
            if (self.controller.get_button(12) and self.button_lock == False) or (self.controller.get_axis(1) > 0.5 and self.con_y_lock == False): # Down
                for position in button_positions:
                    if (position[1] > self.y) and ((position[1] + self.y) + abs(self.x - position[0])) < y_dif:
                        y_dif = ((position[1] + self.y) + abs(self.x - position[0]))
                        new_x = position[0]
                        new_y = position[1]
            
            if (self.controller.get_button(13) and self.button_lock == False) or (self.controller.get_axis(0) < -0.5 and self.con_x_lock == False): # Left
                for position in button_positions:
                    if (position[0] < self.x) and ((self.x - position[0]) + abs(self.y - position[1])) < x_dif:
                        x_dif = ((self.x - position[0]) + abs(self.y - position[1]))
                        new_x = position[0]
                        new_y = position[1]
                
            if (self.controller.get_button(14) and self.button_lock == False) or (self.controller.get_axis(0) > 0.5 and self.con_x_lock == False): # Right
                for position in button_positions:
                    if (position[0] > self.x) and ((position[0] + self.x) + abs(self.y - position[1])) < x_dif:
                        x_dif = ((position[0] + self.x) + abs(self.y - position[1]))
                        new_x = position[0]
                        new_y = position[1]

            #joystick lock
            if -0.5 < self.controller.get_axis(1) < 0.5: self.con_y_lock = False
            else: self.con_y_lock = True
            if -0.5 < self.controller.get_axis(0) < 0.5: self.con_x_lock = False
            else: self.con_x_lock = True

            #button lock
            if (self.controller.get_button(11) or self.controller.get_button(12) or self.controller.get_button(13) or self.controller.get_button(14)):
                self.button_lock = True
            else:
                self.button_lock = False

            #pointer always on button
            if (self.x, self.y) not in button_positions:
                new_x, new_y = button_positions[0]

                                
            self.x, self.y = new_x, new_y

    def handle_event(self, buttons):
        if pygame.joystick.get_count() > 0:
            for button in buttons:
                if isinstance(button, CircleButton):
                    distance = math.sqrt((self.x - button.x) ** 2 + (self.y - button.y) ** 2)
                    if distance <= self.radius + button.width:
                        if self.controller.get_button(0):
                            button.action()
                elif isinstance(button, RectButton) or isinstance(button, SwitchButton):
                    if button.rect.collidepoint((self.x, self.y)):
                        if self.controller.get_button(0):
                            button.action()   