import pygame
import os
import sys


from classes import global_game_functions
from lvl_01 import level_1


class Game:
    images = []
    win = None
    ratio = 0

    entered_number = 0
    first_order_entered = False
    second_order_entered = False

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
            "bgA.jpg",
            "mainmenu.png",
            "selected_lvl.png",
            "alien_a.png",
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
        game_functions.display_image(self.images[1], 0 , 150, self.win)
        game_functions.display_image(self.images[2], 0 , 610, self.win)

        game_functions.display_text(30, 'Select a Level'              , 0, 475, self.win)
        game_functions.display_text(30, 'Press [SPACE] to start'      , 0, 505, self.win)
        game_functions.display_text(25, '[C] - Controls '             , -150, 750, self.win)
        game_functions.display_text(25, '[I] - Game Info'             , -150, 775, self.win)
        game_functions.display_text(25, '[Q] - Quit     '             , 200, 750, self.win)
        game_functions.display_text(30, 'Selected Level = ' + str(game_1.entered_number), 0, 625, self.win)
        
        game_functions.display_image(self.images[3], 250 , 630, self.win)
        game_functions.display_image(self.images[3], -250 , 630, self.win)
        


#MAIN LOOP
while True:
    game_1 = Game()
    game_functions = global_game_functions()
    game_1.init_game(game_functions)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)

                elif event.key == pygame.K_SPACE:
                    if game_1.entered_number == 1: obj = level_1(); obj.start_level()
                        
               
        pygame.display.update()
        game_1.update_screen(game_functions)
