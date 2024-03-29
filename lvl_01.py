import pygame
import sys
import os

from classes import alien_1, projectile, player

class level_1(self):

    #global class vars
	loaded_images = []
    loaded_sounds = []


    def load_images(self, unloaded_images):
        loaded_images = []
        directory = "images/"
        counter = 0
        for x in unloaded_images:
            loaded_images[counter] = pygame.image.load(directory + x).convert_alpha()
            counter += 1
        self.load_images = loaded_images

    def load_sounds(self, unloaded_sounds):
        loaded_sounds = []
        directory = "sounds/"
        counter = 0
        for x in unloaded_sounds:
            loaded_sounds[counter] = pygame.mixer.Sound(directory + x)
            counter += 1
        self.loaded_sounds = loaded_sounds
	
	def init_lvl():
		pygame.init()

        # set screen & label
        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Main Menu")

        # load all images
        images = [
            "ship.png",
            "shipleft.png",
            "shipright.png",
            "bgA.jpg",
            "alien_A.png",
            "gameover.png",
            "win.png",
            "restart.png",
            "quit.png",
            "menu.png",
            "explo.png",
            "lvl1.png",
        ]
        self.load_images(images)

        # load & start music
        sounds = [
            "laser.wav",
            "gameover.wav",
            "invaderkilled.wav",
        ]
        self.load_sounds(sounds)

        pygame.mixer.music.load('sounds/spaceinvaders1.mp3')
        pygame.mixer.music.play(-1)


	def start_lvl():

