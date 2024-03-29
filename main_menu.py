import pygame
import os
import sys

from lvl_01 import level_1


class Game:
    loaded_estatic_images = []
    win = None
    width_max = 0
    height_max = 0

    entered_number = 0
    first_order_entered = False
    second_order_entered = False

    def init_game(self):
        pygame.init()

        # Set screen & label
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Main Menu")

        # Load all images
        estatic_images = [
            "bgA.jpg",
            "quit.png",
            "level.png",
            "mainmenu.png",
            "info.png",
            "info2.png",
            "start.png",
            "lvl_select.png",
        ]
        self.loaded_estatic_images = self.load_images(estatic_images)

        # Start music
        pygame.mixer.music.load('sounds/spaceinvaders1.mp3')
        pygame.mixer.music.play(-1)

        # Center screen
        bg_width, bg_height = self.loaded_estatic_images[0].get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()

        self.width_max = (screen_width - bg_width) / 2
        self.height_max = (screen_height - bg_height) / 2

    def load_images(self, unloaded_images):
        loaded_images = {}
        directory = "images/"
        counter = 0
        for x in unloaded_images:
            loaded_images[counter] = pygame.image.load(directory + x).convert_alpha()
            counter += 1

        return loaded_images

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

    def update_screen(self):
        self.win.blit(self.loaded_estatic_images[0], (self.width_max , self.height_max))
        self.win.blit(self.loaded_estatic_images[1], (self.width_max + 950, self.height_max + 775))
        self.win.blit(self.loaded_estatic_images[2], (self.width_max + 400, self.height_max + 425))
        self.win.blit(self.loaded_estatic_images[3], (self.width_max + 400, self.height_max + 50))
        self.win.blit(self.loaded_estatic_images[4], (self.width_max + 400, self.height_max + 770))
        self.win.blit(self.loaded_estatic_images[5], (self.width_max + 400, self.height_max + 800))
        self.win.blit(self.loaded_estatic_images[6], (self.width_max + 600, self.height_max + 650))
        self.win.blit(self.loaded_estatic_images[7], (self.width_max + 1000, self.height_max + 350))


#MAIN LOOP
while True:
    game_1 = Game()

    game_1.init_game()

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

                elif event.key == pygame.K_SPACE:
                    if game_1.entered_number == 1:
                        obj = level_1()
                        obj.start_lvl_1()

        font = pygame.font.SysFont('couriernew', 30, True)
        level_select = font.render('Level:' + str(game_1.entered_number), 1, (4, 245, 4))
        game_1.win.blit(level_select, (game_1.width_max + 1030, game_1.height_max +  365))

        pygame.display.update()
        game_1.update_screen()
