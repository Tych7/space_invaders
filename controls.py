import pygame
import os
import sys
import json


from classes import global_game_functions, Button


class Controls:
    images = []
    win = None
    ratio = 0
    buttons = []

    running = True

    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]

    def init_game(self, game_functions):
        pygame.init()

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Controls")

        images = [
            "keyboard_controls.png",
            "SFX.png",
            "button.png",
        ]
        loaded_images = game_functions.load_images(images)
        self.set_ratio()
        self.images = game_functions.scale_images(loaded_images)

    def update_screen(self, game_functions):
        game_functions.display_image(self.images[0], 0 , 0, self.win)

        game_functions.display_text(80, 'Keyboard Controls'             , 0, 160 * self.ratio, self.win)

        for button in self.buttons: button.draw(self.win, self.images[2])

        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["SFX"] == "false": game_functions.display_image(self.images[1], -720 * self.ratio, 90 * self.ratio, self.win)
        

    def main(self, game_functions):
        self.init_game(game_functions)

        quit_button = Button(1625, 1200, 300, 60, "Quit Game", 40, lambda: (pygame.quit(), sys.exit(0)))
        main_button = Button(635, 1200, 300, 60, "Main Menu", 40, lambda: setattr(self, 'running', False))
        self.buttons = [main_button, quit_button]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                main_button.handle_event(event)
                quit_button.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s: game_functions.mute_sound_toggle("SFX")
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit(0)
            if keys[pygame.K_m]:
                self.running = False

            pygame.display.update()
            self.update_screen(game_functions)