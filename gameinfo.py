import pygame
import os
import sys
pygame.init()

win = pygame.display.set_mode((1600,900))
pygame.display.set_caption("information")

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


#mainloop
def rewindow():

    quit = pygame.image.load('quit.png').convert_alpha()
    bg = pygame.image.load('bgA.jpg').convert_alpha()
    mm = pygame.image.load('mainmenu.png').convert_alpha()
    menu = pygame.image.load('menu.png').convert_alpha()
    keyboard = pygame.image.load('keyboard.png').convert_alpha()



    win.blit(bg, (0, 0))
    win.blit(quit, (950, 800))
    win.blit(mm, (400, 50))
    win.blit(menu, (350, 800))
    win.blit(keyboard, (500, 350))



while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

    keys = pygame.key.get_pressed()


    if keys[pygame.K_m]:
    	exit()
    if keys[pygame.K_q]:
        exit()

    pygame.display.update()
    rewindow()
