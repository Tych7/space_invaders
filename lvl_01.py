import pygame
import sys
import os

from classes import alien_1, projectile, player

class level_1:

    #global static data
    images = []
    sounds = []
    win = None
    width_max = 0
    height_max = 0
    player_objects = [] 
    alien_1_objects = []

    #global variable data
    score = 0
    pauze = False
	
    def init_lvl(self):
        pygame.init()

        # set window label
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("level 1")


        # load all images
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
        self.load_images(images)

        # load & start music
        sounds = [
            "laser.wav",
            "gameover.wav",
            "invaderkilled.wav",
        ]
        self.load_sounds(sounds)

        bg_width, bg_height = self.loaimagesed_images[0].get_size()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.width_max = (screen_width - bg_width) / 2
        self.height_max = (screen_height - bg_height) / 2
    
    def load_images(self, unloaded_images):
        loaded_images = []
        directory = "images/"
        for x in unloaded_images:
            loaded_images.append(pygame.image.load(directory + x).convert_alpha())
        self.images = loaded_images

    def load_sounds(self, unloaded_sounds):
        loaded_sounds = []
        directory = "sounds/"
        for x in unloaded_sounds:
            loaded_sounds.append(pygame.mixer.Sound(directory + x))
        self.sounds = loaded_sounds

    def update_screen(self):
        self.win.blit(self.images[0], (self.width_max , self.height_max ))
        self.win.blit(self.images[1], (self.width_max + 200, self.height_max + 825))

        font00 = pygame.font.SysFont('couriernew', 30, True)
        text00 = font00.render('Score: ' + str(self.score), 1, (124,252,0))
        self.win.blit(text00, (self.width_max + 1150, self.height_max +  60))

        for x in self.alien_1_objects: x.draw(self.win, self.images[11])

        player_images = [self.images[2], self.images[3], self.images[4]]
        for x in self.player_objects: x.draw(self.win, player_images)



    def start_level(self):
        self.init_lvl()

        self.player_objects.clear()
        self.alien_1_objects.clear()

        alien_level_a = 100 + self.height_max
        alien_level_b = 150 + self.height_max
        alien_level_c = 200 + self.height_max

        player_1 = player(self.width_max + 800, self.height_max + 750, 35, 45); self.player_objects.append(player_1)
        alienA = alien_1(self.width_max + 350, alien_level_a, 34, 27, self.height_max + 850); self.alien_1_objects.append(alienA)
        alienB = alien_1(self.width_max + 450, alien_level_a, 34, 27, self.height_max + 950); self.alien_1_objects.append(alienB)
        alienC = alien_1(self.width_max + 550, alien_level_a, 34, 27, self.height_max + 1050); self.alien_1_objects.append(alienC)
        alienD = alien_1(self.width_max + 650, alien_level_a, 34, 27, self.height_max + 1150); self.alien_1_objects.append(alienD)
        alienE = alien_1(self.width_max + 750, alien_level_a, 34, 27, self.height_max + 1250); self.alien_1_objects.append(alienE)

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
                self.win.blit(self.images[7], (self.width_max + 350, self.height_max + 750))
                self.win.blit(self.images[8], (self.width_max + 950, self.height_max + 750))
                self.win.blit(self.images[9], (self.width_max + 350, self.height_max + 800))
                if keys[pygame.K_q]:
                    pygame.quit()
                    sys.exit(0)
                # if keys[pygame.K_r]:
                #     restart()
                if keys[pygame.K_m]:
                    running = False
        
            pygame.display.update()
            self.update_screen()
