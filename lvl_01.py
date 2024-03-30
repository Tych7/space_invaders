import pygame
import sys
import os

from classes import global_game_functions,alien_1, projectile, player

class level_1:

    #global static data
    images = []
    loaded_sounds = []
    win = None
    player_objects = [] 
    alien_1_objects = []
    ratio = 0

    #global variable data
    score = 0
    pauze = False

    def set_ratio(self, loaded_images, game_functions):
        bg_width, bg_height = loaded_images[0].get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()

        self.ratio = screen_width / bg_width

    def init_lvl(self, game_functions):
        pygame.init()

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("level 1")

        images = [
            "bgA.jpg",
            "lvl_select.png",
            "ship.png",
            "shipleft.png",
            "shipright.png",
            "gameover.png",
            "win.png",
            "restart.png",
            "quit.png",
            "menu.png",
            "explo.png",
            "alien_A.png",
        ]
        loaded_images = game_functions.load_images(self, images)
        self.set_ratio(loaded_images, game_functions)
        self.images = game_functions.scale_images(self, loaded_images)
        
        sounds = [
            "laser.wav",
            "gameover.wav",
            "invaderkilled.wav",
        ]
        game_functions.load_sounds(self, sounds)


    def update_screen(self, game_functions):
        self.win.blit(self.images[0], (0, 0 ))
        self.win.blit(self.images[1], (self.ratio * 200, self.ratio * 825))

        for x in self.alien_1_objects: x.draw(self.win, self.images[11])

        player_images = [self.images[2], self.images[3], self.images[4]]
        for x in self.player_objects: x.draw(self.win, player_images)

        game_functions.display_text(30,'Score: ' + str(self.score), 1150, 60, self.win)



    def start_level(self):
        game_functions = global_game_functions()
        self.init_lvl(global_game_functions)

        self.player_objects.clear()
        self.alien_1_objects.clear()

        alien_level_a = 100 * self.ratio
        alien_level_b = 150 * self.ratio
        alien_level_c = 200 * self.ratio

        player_1 = player(self.ratio * 800, self.ratio * 750, 35, 45); self.player_objects.append(player_1)
        alienA = alien_1(self.ratio * 350, alien_level_a, 34, 27, self.ratio * 850, self.ratio); self.alien_1_objects.append(alienA)
        alienB = alien_1(self.ratio * 450, alien_level_a, 34, 27, self.ratio * 950, self.ratio); self.alien_1_objects.append(alienB)
        alienC = alien_1(self.ratio * 550, alien_level_a, 34, 27, self.ratio * 1050, self.ratio); self.alien_1_objects.append(alienC)
        alienD = alien_1(self.ratio * 650, alien_level_a, 34, 27, self.ratio * 1150, self.ratio); self.alien_1_objects.append(alienD)
        alienE = alien_1(self.ratio * 750, alien_level_a, 34, 27, self.ratio * 1250, self.ratio); self.alien_1_objects.append(alienE)

        running = True
        #Start Main Loop
        while running:
            pygame.time.delay(11)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.pauze = True

            if self.pauze:
                alienA.vel = 0
                alienB.vel = 0
                alienC.vel = 0
                alienD.vel = 0
                alienE.vel = 0
                self.win.blit(self.images[7], (self.ratio * 350, self.ratio * 750))
                self.win.blit(self.images[8], (self.ratio * 950, self.ratio * 750))
                self.win.blit(self.images[9], (self.ratio * 350, self.ratio * 800))
                if keys[pygame.K_q]:
                    pygame.quit()
                    sys.exit(0)
                # if keys[pygame.K_r]:
                #     restart()
                if keys[pygame.K_m]:
                    running = False
        
            pygame.display.update()
            self.update_screen(game_functions)
