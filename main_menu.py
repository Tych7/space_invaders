import pygame
import os
import sys
import json


from classes import global_game_functions, Button
from controls import Controls
from level_template import level


class Game:
    images = []
    win = None
    controller = None
    ratio = 0
    lvl_count = 0
    home_pushbuttons_circle = []

    entered_number = 0
    first_order_entered = False
    second_order_entered = False

    settings_open = False
    settings_pushbuttons = []
    settings_switches = []

    def set_ratio(self, loaded_images, game_functions):
        bg_width = loaded_images[0].get_size()[0]
        screen_width = pygame.display.get_surface().get_size()[0]

        self.ratio = screen_width / bg_width
        with open("settings.json", 'r') as file: data = json.load(file)
        data["ratio"] = self.ratio
        with open("settings.json", 'w') as file: json.dump(data, file, indent=4)
        game_functions.set_ratio()
        
        
    def init_game(self, game_functions):
        pygame.init()
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Main Menu")

        images = [
            "bgB.png",              #0
            "mainmenu.png",         #1
            "selected_lvl.png",     #2
            "alien_A.png",          #3
            "SFX.png",              #4
            "music.png",            #5
            "pauze_menu.png",       #6
            "icon_settings.png",    #7
            "icon_controls.png",    #8
            "icon_quit.png",        #9
            "button_border.png",    #10
        ]
        loaded_images = game_functions.load_images(images)
        self.set_ratio(loaded_images, game_functions)
        self.images = game_functions.scale_images(loaded_images)

        # load mixer with music
        pygame.mixer.music.load('sounds/spaceinvaders1.mp3')
        pygame.mixer.music.play(-1)
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["Music"] == "false": pygame.mixer.music.pause()


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
        game_functions.display_image(self.images[1], 0 , 240 * self.ratio, self.win)
        game_functions.display_image(self.images[2], 0 , 975 * self.ratio, self.win)
        game_functions.display_image(self.images[10], 0 , 1210, self.win)

        game_functions.display_text(50, 'Select a Level'              , 0, 760 * self.ratio, self.win)
        game_functions.display_text(50, 'Press [ENTER] to start'      , 0, 800 * self.ratio, self.win)
        game_functions.display_text(50, 'Selected Level = ' + str(game_1.entered_number), 0, 995 * self.ratio, self.win)
        game_functions.display_text(30, 'Max lvl: ' + str(game_1.lvl_count), 580 * self.ratio, 90 * game_1.ratio, game_1.win)
        
        game_functions.display_image(self.images[3], 400 * self.ratio, 1000 * self.ratio, self.win)
        game_functions.display_image(self.images[3], -400 * self.ratio, 1000 * self.ratio, self.win)

        for button in self.home_pushbuttons_circle: button.draw_pushbutton_circle(self.win)

        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["SFX"] == "false": game_functions.display_image(self.images[4], -700 * self.ratio, 90 * self.ratio, self.win)
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["Music"] == "false": game_functions.display_image(self.images[5], -750 * self.ratio, 90 * self.ratio, self.win)
        
        if self.settings_open:
            overlay_color = (0, 0, 0, 170)
            overlay = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
            overlay.fill(overlay_color)
            self.win.blit(overlay, (0, 0))

            game_functions.display_image(self.images[6], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, 'SETTINGS', 0 , 515 * self.ratio, self.win)
            for button in self.settings_pushbuttons: button.draw_pushbutton_rect(self.win)
            for switch in self.settings_switches: switch.draw_switch(self.win)

#MAIN LOOP
while True:
    game_1 = Game()
    game_functions = global_game_functions()
    game_1.init_game(game_functions)

    settings_button = Button(1280, 1290, 50, 50, "Settings", 40, lambda: setattr(game_1, 'settings_open', True), game_1.images[7])
    controls_button = Button(1100, 1290, 50, 50, "Controls", 40, lambda: Controls().main(game_functions), game_1.images[8])
    quit_button = Button(1460, 1290, 50, 50, "Quit Game", 40, lambda: (pygame.quit(), sys.exit(0)), game_1.images[9])
    game_1.home_pushbuttons_circle = [settings_button, controls_button, quit_button]

    music_switch = Button(1270, 600, 100, 40, "Music", 25, lambda: game_functions.mute_sound_toggle("Music"))
    sfx_switch = Button(1270, 650, 100, 40, "SFX", 25, lambda: game_functions.mute_sound_toggle("SFX"))
    back_button = Button(1130, 820, 300, 60, "Back", 40, lambda: setattr(game_1, 'settings_open', False))
    game_1.settings_pushbuttons = [back_button]
    game_1.settings_switches = [sfx_switch, music_switch]

    with open("settings.json", 'r') as file: data = json.load(file)
    data["Music"] = "false"
    data["SFX"] = "false"
    with open("settings.json", 'w') as file: json.dump(data, file, indent=4)

    button_9_pressed = False
    button_10_pressed = False

    #Show amount of levels
    files = os.listdir("levels/")
    game_1.lvl_count = len(files)
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if game_1.settings_open:
                music_switch.handle_event(event)
                sfx_switch.handle_event(event)
                back_button.handle_event(event)
            else:
                quit_button.handle_event(event)
                controls_button.handle_event(event)
                settings_button.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_1.update_entered_number(1)
                elif event.key == pygame.K_2:
                    game_1.update_entered_number(2)
                elif event.key == pygame.K_3:
                    game_1.update_entered_number(3)
                elif event.key == pygame.K_4:
                    game_1.update_entered_number(4)
                elif event.key == pygame.K_5:
                    game_1.update_entered_number(5)
                elif event.key == pygame.K_6:
                    game_1.update_entered_number(6)
                elif event.key == pygame.K_7:
                    game_1.update_entered_number(7)
                elif event.key == pygame.K_8:
                    game_1.update_entered_number(8)
                elif event.key == pygame.K_9:
                    game_1.update_entered_number(9)
                elif event.key == pygame.K_0:
                    game_1.update_entered_number(0)
                elif event.key == pygame.K_BACKSPACE:
                    game_1.update_entered_number(-1)
                elif event.key == pygame.K_RETURN:
                    file_path = "levels/lvl_" + str(game_1.entered_number) + ".csv"
                    if os.path.exists(file_path):
                        obj = level()
                        obj.main(game_functions, "Level " + str(game_1.entered_number), file_path)
                    else:
                        print("Error: File not found:", file_path)
                        
            elif event.type == pygame.JOYBUTTONDOWN:
                if game_1.controller.get_button(9) and game_1.entered_number > 0: 
                    game_1.entered_number -= 1
                elif game_1.controller.get_button(10): game_1.entered_number += 1
                if game_1.controller.get_button(5):
                    file_path = "levels/lvl_" + str(game_1.entered_number) + ".csv"
                    if os.path.exists(file_path):
                        obj = level()
                        obj.main(game_functions, "Level " + str(game_1.entered_number), file_path)
                    else:
                        print("Error: File not found:", file_path)
        
        pygame.display.update()
        game_1.update_screen(game_functions)
