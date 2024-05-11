import pygame
import os
import sys
import json


from classes import global_game_functions
from GUI import Button, RectButton, CircleButton, SwitchButton, controller_pointer



class Controls:
    images = []
    win = None
    ratio = 0
    home_buttons = []
    settings_buttons = []
    switch_controls = False

    running = True
    settings_open = False

    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]

    def init_game(self, game_functions):
        pygame.init()

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Controls")

        images = [
            "keyboard_controls.png",    #0
            "SFX.png",                  #1
            "music.png",                #2
            "icon_home.png",            #3
            "icon_quit.png",            #4
            "button_border.png",        #5
            "icon_settings.png",        #6
            "pauze_menu.png",           #7
            "icon_swap.png",            #8
            "controller_controls.png"   #9

        ]
        loaded_images = game_functions.load_images(images)
        self.set_ratio()
        self.images = game_functions.scale_images(loaded_images)

    def update_screen(self, game_functions, pointer):
        
        if self.switch_controls:    
            game_functions.display_image(self.images[9], 0 , 0  * self.ratio, self.win)
            game_functions.display_text(80, 'Controller', 0, 160 * self.ratio, self.win)
        else:                       
            game_functions.display_image(self.images[0], 0 , 0, self.win)
            game_functions.display_text(80, 'Keyboard', 0, 160 * self.ratio, self.win)


        game_functions.display_image(self.images[5], 0 , 1210  * self.ratio, self.win)

        for button in self.home_buttons: button.draw(self.win)

        if self.settings_open:
            overlay_color = (0, 0, 0, 170)
            overlay = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
            overlay.fill(overlay_color)
            self.win.blit(overlay, (0, 0))

            game_functions.display_image(self.images[7], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, 'SETTINGS', 0 , 515 * self.ratio, self.win)
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

        main_button = CircleButton(1040, 1290, 50, 50, "Main Menu", 40, lambda: setattr(self, 'running', False), self.images[3])
        settings_button = CircleButton(1200, 1290, 50, 50, "Settings", 40, lambda: setattr(self, 'settings_open', True), self.images[6])
        switch_controls = CircleButton(1360, 1290, 50, 50, "Switch Controls", 40, lambda: setattr(self, 'switch_controls',  not self.switch_controls), self.images[8])
        quit_button = CircleButton(1520, 1290, 50, 50, "Quit Game", 40, lambda: (pygame.quit(), sys.exit(0)), self.images[4])

        music_switch = SwitchButton(1270, 600, 100, 40, "Music", 25, lambda: game_functions.mute_sound_toggle("Music"))
        sfx_switch = SwitchButton(1270, 650, 100, 40, "SFX", 25, lambda: game_functions.mute_sound_toggle("SFX"))
        back_button = RectButton(1130, 820, 300, 60, "Back", 40, lambda: setattr(self, 'settings_open', False))

        self.settings_buttons = [back_button, music_switch, sfx_switch]
        self.home_buttons = [main_button, quit_button, settings_button, switch_controls]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if self.settings_open:
                    music_switch.handle_event(event)
                    sfx_switch.handle_event(event)
                    back_button.handle_event(event)
                    pointer.move_pointer(self.settings_buttons)
                else:
                    main_button.handle_event(event)
                    quit_button.handle_event(event)
                    settings_button.handle_event(event)
                    switch_controls.handle_event(event)
                    pointer.move_pointer(self.home_buttons)

                if event.type == pygame.JOYBUTTONDOWN:
                    if self.settings_open: pointer.handle_event(self.settings_buttons)
                    else: pointer.handle_event(self.home_buttons)

            pygame.display.update()
            self.update_screen(game_functions, pointer)