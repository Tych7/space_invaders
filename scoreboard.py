import pygame
import os
import sys
import json


from entities import global_game_functions
from GUI import Button, RectButton, CircleButton, SwitchButton, controller_pointer



class scoreboard:
    images = []
    win = None
    ratio = 0
    home_buttons = []
    settings_buttons = []
    switch_controls = False
    scores = []

    running = True
    settings_open = False

    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]

    def init_game(self, game_functions):
        pygame.init()

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("scoreboard")

        images = [
            "scoreboard.png",           #0
            "SFX.png",                  #1
            "music.png",                #2
            "icon_back.png",            #3
            "icon_quit.png",            #4
            "button_border.png",        #5
            "icon_settings.png",        #6
            "pauze_menu.png",           #7
        ]
        loaded_images = game_functions.load_images(images)
        self.set_ratio()
        self.images = game_functions.scale_images(loaded_images)

    def update_board(self, score):
        with open("settings.json", 'r') as file:
            data = json.load(file)
            scores = data["scores"]

        if len(scores) < 10:
            scores.append(score)
        else:
            if score > min(scores):
                scores.append(score)
                scores.sort(reverse=True)
                scores = scores[:10]
        
        data["scores"] = scores
        
        with open("settings.json", 'w') as file:
            json.dump(data, file, indent=4)


    def update_screen(self, game_functions, pointer):
        game_functions.display_image(self.images[0], 0 , 0, self.win)
        game_functions.display_text(80, 'Highscores', 0, 160 * self.ratio, (112, 228, 209), self.win)
        game_functions.display_image(self.images[5], 0 , 1210  * self.ratio, self.win)

        game_functions.display_text(40, "#" , -250 * self.ratio, 340 * self.ratio, (112, 228, 209), self.win)
        game_functions.display_text(40, "Scores" , -10 * self.ratio, 340 * self.ratio, (112, 228, 209), self.win)

        for i in range(10):
            correction = 0
            if i == 9: correction = 10
            game_functions.display_text(40, str(i + 1) , (-250 + correction) * self.ratio, (415 + i * 71) * self.ratio, (112, 228, 209), self.win)
            game_functions.display_text(40, str(self.scores[i]) , -100 * self.ratio, (415 + i * 71) * self.ratio, (255, 140 ,68), self.win)

        for button in self.home_buttons: button.draw(self.win)

        if self.settings_open:
            overlay_color = (0, 0, 0, 170)
            overlay = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
            overlay.fill(overlay_color)
            self.win.blit(overlay, (0, 0))

            game_functions.display_image(self.images[7], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, 'SETTINGS', 0 , 515 * self.ratio, (112, 228, 209), self.win)
            for button in self.settings_buttons: button.draw(self.win)
            pointer.draw(self.win, self.settings_buttons)
        else:
            pointer.draw(self.win, self.home_buttons)

        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["SFX"] == "false": game_functions.display_image(self.images[1], -700 * self.ratio, 90 * self.ratio, self.win)
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["Music"] == "false": game_functions.display_image(self.images[2], -750 * self.ratio, 90 * self.ratio, self.win)
        

    def main(self, game_functions):
        self.init_game(game_functions)
        pointer = controller_pointer(1280 * self.ratio, 1290 * self.ratio, 12)

        main_button = CircleButton(1150, 1290, 50, 50, "Main Menu", 40, lambda: setattr(self, 'running', False), self.images[3])
        settings_button = CircleButton(1410, 1290, 50, 50, "Settings", 40, lambda: setattr(self, 'settings_open', True), self.images[6])

        music_switch = SwitchButton(1270, 600, 100, 40, "Music", 25, lambda: game_functions.mute_sound_toggle("Music"))
        sfx_switch = SwitchButton(1270, 650, 100, 40, "SFX", 25, lambda: game_functions.mute_sound_toggle("SFX"))
        back_button = RectButton(1130, 820, 300, 60, "Back", 40, lambda: setattr(self, 'settings_open', False))

        self.settings_buttons = [back_button, music_switch, sfx_switch]
        self.home_buttons = [main_button, settings_button]

        with open("settings.json", 'r') as file:
            data = json.load(file)
            self.scores = data["scores"]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if self.settings_open:
                    for button in self.settings_buttons:
                        button.handle_event(event)
                    pointer.move_pointer(self.settings_buttons)
                else:
                    for button in self.home_buttons:
                        button.handle_event(event)
                    pointer.move_pointer(self.home_buttons)

                if event.type == pygame.JOYBUTTONDOWN:
                    if self.settings_open: pointer.handle_event(self.settings_buttons)
                    else: pointer.handle_event(self.home_buttons)


            pygame.display.update()
            self.update_screen(game_functions, pointer)