import pygame
import os
import sys
import json


from entities import global_game_functions
from GUI import Button, RectButton, CircleButton, SwitchButton, controller_pointer
from controls import Controls
from scoreboard import scoreboard
from level_template import level


class Game:
    images = []
    win = None
    controller = None
    ratio = 0
    lvl_count = 0

    entered_number = 0
    first_order_entered = False
    second_order_entered = False

    settings_open = False
    returned = False

    state = 'home'

    #Button Collections
    settings_buttons = []
    home_buttons = []
    state_buttons = []
    level_buttons = []

    active_buttons = []


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
            "alien_B.png",          #3
            "SFX.png",              #4
            "music.png",            #5
            "pauze_menu.png",       #6
            "icon_settings.png",    #7
            "icon_controls.png",    #8
            "icon_quit.png",        #9
            "button_border.png",    #10
            "icon_r1.png",          #11
            "icon_l1.png",          #12
            "icon_ranked.png",      #13
            "icon_target.png",      #14
            "icon_score.png",       #15
        ]
        loaded_images = game_functions.load_images(images)
        self.set_ratio(loaded_images, game_functions)
        self.images = game_functions.scale_images(loaded_images)

        # load mixer with music
        pygame.mixer.music.load('sounds/spaceinvaders1_music.mp3')
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

    def start_lvl(self):
        if self.entered_number > 0:
            file_path = "levels/lvl_" + str(self.entered_number) + ".csv"
            if os.path.exists(file_path):
                obj = level()
                obj.main(game_functions, "Level " + str(self.entered_number), file_path, self.state)
                self.returned = False
                self.state = 'home'
            else:
                print("Error: File not found:", file_path)
        

    def update_screen(self, game_functions, pointer):
        game_functions.display_image(self.images[0], 0 , 0, self.win)
        game_functions.display_image(self.images[1], 0 , 175 * self.ratio, self.win)
        game_functions.display_image(self.images[10], 0 , 1210 * self.ratio, self.win)
        
        game_functions.display_text(30, 'Max lvl: ' + str(self.lvl_count - 1), 580 * self.ratio, 90 * self.ratio, (112, 228, 209), self.win)

        for button in self.home_buttons: button.draw(self.win)
        for button in self.state_buttons: button.draw(self.win)

        game_functions.display_image(self.images[13], -400 * self.ratio, 965 * self.ratio, self.win)
        game_functions.display_image(self.images[14], 100 * self.ratio, 965 * self.ratio, self.win)

        if self.state == 'level':
            for button in self.level_buttons: button.draw(self.win)
            game_functions.display_text(50, 'Selected Level = ' + str(game_1.entered_number), 0, 970 * self.ratio, (112, 228, 209), self.win)
            pointer.draw(game_1.win, self.level_buttons)
            if pygame.joystick.get_count() > 0:
                game_functions.display_image(self.images[11], 520 , 960 * self.ratio, self.win)
                game_functions.display_image(self.images[12], -520 , 960 * self.ratio, self.win)
            game_functions.display_image(self.images[3], 400 * self.ratio, 975 * self.ratio, self.win)
            game_functions.display_image(self.images[3], -400 * self.ratio, 975 * self.ratio, self.win)
        
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
            game_functions.display_text(35, 'SETTINGS', 0 , 515 * self.ratio, (112, 228, 209), self.win)
            for button in self.settings_buttons: button.draw(self.win)
            pointer.draw(game_1.win, self.settings_buttons)
        else:
            pointer.draw(game_1.win, self.home_buttons)
            pointer.draw(game_1.win, self.state_buttons)        

#MAIN LOOP
while True:
    game_1 = Game()
    game_functions = global_game_functions()
    game_1.init_game(game_functions)
    pointer = controller_pointer(1280 * game_1.ratio, 1290 * game_1.ratio, 12)
    

    controls_button = CircleButton(1070, 1290, 50, 50, "Controls", 40, lambda: Controls().main(game_functions), game_1.images[8])
    score_button = CircleButton(1210, 1290, 50, 50, "Score Board", 40, lambda: scoreboard().main(game_functions), game_1.images[15])
    settings_button = CircleButton(1350, 1290, 50, 50, "Settings", 40, lambda: setattr(game_1, 'settings_open', True), game_1.images[7])
    quit_button = CircleButton(1490, 1290, 50, 50, "Quit Game", 40, lambda: (pygame.quit(), sys.exit(0)), game_1.images[9])

    waves_button = RectButton(800, 950, 400, 100,  "Ranked  ", 40, lambda: setattr(game_1, 'state', 'waves'))
    level_button = RectButton(1360, 950, 400, 100, " Practice", 40, lambda: setattr(game_1, 'state', 'level'))

    level_select_button = RectButton(780, 950, 1000, 100, "", 50, lambda: game_1.start_lvl())
    level_back_button = RectButton(1130, 1075, 300, 60, "Back", 40, lambda: setattr(game_1, 'state', 'home'))

    game_1.level_buttons = [level_select_button, level_back_button]
    game_1.home_buttons = [settings_button, controls_button, quit_button, score_button]
    game_1.state_buttons = [waves_button, level_button]

    music_switch = SwitchButton(1270, 600, 100, 40, "Music", 25, lambda: game_functions.mute_sound_toggle("Music"))
    sfx_switch = SwitchButton(1270, 650, 100, 40, "SFX", 25, lambda: game_functions.mute_sound_toggle("SFX"))
    settings_back_button = RectButton(1130, 820, 300, 60, "Back", 40, lambda: setattr(game_1, 'settings_open', False))
    game_1.settings_buttons = [settings_back_button, sfx_switch, music_switch]

    #Show amount of levels
    files = os.listdir("levels/")
    game_1.lvl_count = len(files)
        
    while True:
        # Check for controller reconnection
        if pygame.joystick.get_count() > 0:
            if game_1.controller is None:
                game_1.controller = pygame.joystick.Joystick(0)
                game_1.controller.init()
        else:
            game_1.controller = None
        
        #select active buttons
        if game_1.settings_open: game_1.active_buttons = game_1.settings_buttons
        elif game_1.state == 'home': game_1.active_buttons = game_1.home_buttons + game_1.state_buttons
        elif game_1.state == 'level': game_1.active_buttons = game_1.level_buttons + game_1.home_buttons

        if pygame.joystick.get_count() > 0:
            button_0_up = game_1.controller.get_button(0) == 0
            if button_0_up == True: game_1.returned = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            for button in game_1.active_buttons:
                button.handle_event(event)
            pointer.move_pointer(game_1.active_buttons)

            if game_1.state == 'level':
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
                    elif event.key == pygame.K_RETURN and game_1.entered_number != 0:
                        file_path = "levels/lvl_" + str(game_1.entered_number) + ".csv"
                        if os.path.exists(file_path):
                            obj = level()
                            obj.main(game_functions, "Level " + str(game_1.entered_number), file_path, game_1.state)
                            game_1.returned = False
                            game_1.state = 'home'
                        else:
                            print("Error: File not found:", file_path)

                elif event.type == pygame.JOYBUTTONDOWN:
                    if game_1.controller.get_button(9) and game_1.entered_number > 0: 
                        game_1.entered_number -= 1
                    elif game_1.controller.get_button(10): game_1.entered_number += 1
                    
                if event.type == pygame.JOYBUTTONUP:
                    game_1.returned = True

            elif game_1.state == 'waves':
                file_path = "levels/lvl_1.csv"
                if os.path.exists(file_path):
                    obj = level()
                    obj.main(game_functions, "Wave 1", file_path, game_1.state)
                    game_1.returned = False
                    game_1.state = 'home'
                else:
                    print("Error: File not found:", file_path)
                        
            if pygame.joystick.get_count() > 0 and game_1.controller != None:  
                if game_1.controller.get_button(6):
                    game_1.settings_open = True

                if game_1.returned == True: 
                    pointer.handle_event(game_1.active_buttons)

        
        pygame.display.update()
        game_1.update_screen(game_functions, pointer)
