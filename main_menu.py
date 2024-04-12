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
    ratio = 0
    buttons = []

    entered_number = 0
    first_order_entered = False
    second_order_entered = False

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

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Main Menu")

        images = [
            "bgB.png",
            "mainmenu.png",
            "selected_lvl.png",
            "alien_A.png",
            "mute.png",
            "button.png",
        ]
        loaded_images = game_functions.load_images(images)
        self.set_ratio(loaded_images, game_functions)
        self.images = game_functions.scale_images(loaded_images)

        # load mixer with music
        pygame.mixer.music.load('sounds/spaceinvaders1.mp3')
        pygame.mixer.music.play(-1)

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

        game_functions.display_text(50, 'Select a Level'              , 0, 760 * self.ratio, self.win)
        game_functions.display_text(50, 'Press [ENTER] to start'      , 0, 800 * self.ratio, self.win)
        game_functions.display_text(50, 'Selected Level = ' + str(game_1.entered_number), 0, 995 * self.ratio, self.win)
        
        game_functions.display_image(self.images[3], 400 * self.ratio, 1000 * self.ratio, self.win)
        game_functions.display_image(self.images[3], -400 * self.ratio, 1000 * self.ratio, self.win)

        for button in self.buttons: button.draw(self.win, self.images[5])

        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["music"] == "false": game_functions.display_image(self.images[4], -720 * self.ratio, 100 * self.ratio, self.win)

    
#MAIN LOOP
while True:
    game_1 = Game()
    game_functions = global_game_functions()
    game_1.init_game(game_functions)

    quit_button = Button(1625, 1200, 300, 60, "Quit", 40, lambda: (pygame.quit(), sys.exit(0)))
    controls_button = Button(635, 1200, 300, 60, "Controls", 40, lambda: Controls().main(game_functions))
    game_1.buttons = [quit_button, controls_button]
    
    with open("settings.json", 'r') as file: data = json.load(file)
    data["music"] = "true"
    with open("settings.json", 'w') as file: json.dump(data, file, indent=4)
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            quit_button.handle_event(event)
            controls_button.handle_event(event)
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
                    
                elif event.key == pygame.K_s: game_functions.mute_sound_toggle()

                elif event.key == pygame.K_RETURN:
                    obj = level(); obj.main(game_functions, "Level " + str(game_1.entered_number), "levels/lvl_" + str(game_1.entered_number) + ".csv")
                
                


               
        pygame.display.update()
        game_1.update_screen(game_functions)
