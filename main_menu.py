import pygame
import os
import sys

from lvl_01 import level_1


class Game:
    images = []
    win = None
    width_ratio = 0
    height_ratio = 0

    entered_number = 0
    first_order_entered = False
    second_order_entered = False

    def load_images(self, unloaded_images):
        loaded_images = []
        directory = "images/"
        for x in unloaded_images:
            loaded_images.append(pygame.image.load(directory + x).convert_alpha())
        return loaded_images
    
    def scale_images(self, loaded_images):
        scaled_images = []
        bg_width, bg_height = loaded_images[0].get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()

        self.width_ratio = screen_width / bg_width
        self.height_ratio = screen_height / bg_height

        for x in loaded_images:
            image_width, image_height = x.get_size()
            scaled_images.append(pygame.transform.scale(x, (image_width * self.width_ratio, image_height * self.height_ratio)))
        return scaled_images

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
        loaded_images = self.load_images(estatic_images)
        self.images = self.scale_images(loaded_images)

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
    
    def scale_font_size(self, base_size):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        scaled_size = int(base_size * min(self.width_ratio, self.height_ratio))
        return scaled_size

    def update_screen(self):
        self.win.blit(self.images[0], (0 , 0))
        self.win.blit(self.images[1], (self.width_ratio * 950, self.height_ratio * 775))
        self.win.blit(self.images[2], (self.width_ratio * 400, self.height_ratio * 425))
        self.win.blit(self.images[3], (self.width_ratio * 400, self.height_ratio * 50))
        self.win.blit(self.images[4], (self.width_ratio * 400, self.height_ratio * 770))
        self.win.blit(self.images[5], (self.width_ratio * 400, self.height_ratio * 800))
        self.win.blit(self.images[6], (self.width_ratio * 600, self.height_ratio * 650))
        self.win.blit(self.images[7], (self.width_ratio * 1000, self.height_ratio * 350))

        font_size = self.scale_font_size(30)
        font = pygame.font.SysFont('couriernew', font_size, True)
        level_select = font.render('Level:' + str(game_1.entered_number), 1, (4, 245, 4))
        self.win.blit(level_select, (self.width_ratio * 1030, self.height_ratio * 365))



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
                        obj.start_level()
                        
               
        pygame.display.update()
        game_1.update_screen()
