import pygame
import os
import sys
import json


from classes import global_game_functions


class Controls:
    images = []
    win = None
    ratio = 0

    running = True

    def set_ratio(self, loaded_images, game_functions):
        bg_width, bg_height = loaded_images[0].get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()

        self.ratio = screen_width / bg_width
        game_functions.ratio = self.ratio

    def init_game(self, game_functions):
        pygame.init()

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Main Menu")

        images = [
            "keyboard_controls.png",
            "mute.png"
        ]
        loaded_images = game_functions.load_images(images)
        self.set_ratio(loaded_images, game_functions)
        self.images = game_functions.scale_images(loaded_images)

        # Start music
        # pygame.mixer.music.load('sounds/spaceinvaders1.mp3')
        # pygame.mixer.music.play(-1)

    def update_entered_number(self, number):
        if number == -1:
            if self.second_order_entered:
                self.entered_number = self.entered_number // 10
                self.second_order_entered = False
            elif self.first_order_entered:
                self.entered_number = 0
                self.first_order_entered = False
        elif not self.first_order_entered:
            self.entered_number = number
            self.first_order_entered = True
        elif self.first_order_entered and not self.second_order_entered:
            if number == 0:
                self.entered_number *= 10
            else:
                self.entered_number = self.entered_number * 10 + number
            self.second_order_entered = True
        

    def update_screen(self, game_functions):
        game_functions.display_image(self.images[0], 0 , 0, self.win)

        game_functions.display_text(80, 'Keyboard Controls'             , 0, 160 * self.ratio, self.win)
        game_functions.display_text(40, '[M] - Main Menu '             , -240 * self.ratio, 1200 * self.ratio, self.win)
        game_functions.display_text(40, '[Q] - Quit      '             , 320 * self.ratio, 1200 * self.ratio, self.win)
        
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["music"] == "false": game_functions.display_image(self.images[1], -720 * self.ratio, 90 * self.ratio, self.win)
        

    def main(self):
        game_functions = global_game_functions()
        self.init_game(game_functions)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s: game_functions.mute_sound_toggle()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit(0)
            if keys[pygame.K_m]:
                self.running = False

            pygame.display.update()
            self.update_screen(game_functions)