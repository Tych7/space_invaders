import pygame
import sys
import os
import json
import csv

from classes import global_game_functions,alien, projectile, player, Button

class level:

    #global static data
    images = []
    sounds = []
    win = None
    player_objects = [] 
    alien_1_objects = []
    ratio = 0
    level_string = ""
    alien_rows = []
    alien_collums = []

    pauze_pushbuttons = []
    settings_pushbuttons = []
    settings_switches = []


    #global variable data
    score = 0
    pauze = False
    winner = False
    lose = False
    running = True
    settings_open = False


    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]

    def init_lvl(self, game_functions):
        pygame.init()

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(self.level_string)

        images = [
            "bgA.png",          #0
            "lvl_select.png",   #1
            "ship.png",         #2
            "shipright.png",    #3
            "shipleft.png",     #4
            "gameover.png",     #5
            "win.png",          #6
            "explo.png",        #7
            "SFX.png",          #8
            "music.png",        #9
            "button.png",       #10
            "switch.png",       #11
            "pauze_menu.png",   #12
            "alien_A.png",      #13
        ]
        loaded_images = game_functions.load_images(self, images)
        self.set_ratio()
        self.images = game_functions.scale_images(self, loaded_images)
        
        sounds = [
            "laser.wav",
            "gameover.wav",
            "invaderkilled.wav",
        ]
        game_functions.load_sounds(self, sounds)

    def update_screen(self, game_functions):
        
        #display static images
        game_functions.display_image(self.images[0], 0 , 0, self.win)
        game_functions.display_image(self.images[1], -640 * self.ratio, 1300 * self.ratio, self.win)

        #display aliens type A
        for x in self.alien_1_objects: x.draw(self.win)

        #display player
        player_images = [self.images[2], self.images[3], self.images[4]]
        for x in self.player_objects: x.draw(self.win, player_images)

        #display text
        game_functions.display_text(60,'SCORE:', 950 * self.ratio, 675 * self.ratio, self.win)
        if self.score < 10: score_alignment = 1040
        else: score_alignment = 1020
        game_functions.display_text(60,str(self.score), score_alignment * self.ratio, 750 * self.ratio, self.win)
        
        game_functions.display_text(50,self.level_string, -700 * self.ratio, 1325 * self.ratio, self.win)

        #display projectiles
        for bullet in self.player_objects[0].bullets: bullet.draw(self.win)

        if self.settings_open:
            game_functions.display_image(self.images[12], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, 'SETTINGS', 0 , 515 * self.ratio, self.win)
            for button in self.settings_pushbuttons: button.draw_pushbutton(self.win, self.images[10])
            for switch in self.settings_switches: switch.draw_switch(self.win, self.images[11])

        elif self.pauze:
            game_functions.display_image(self.images[12], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, 'PAUZE MENU', 0 , 515 * self.ratio, self.win)
            for button in self.pauze_pushbuttons: button.draw_pushbutton(self.win, self.images[10])
            
        if self.winner:
            game_functions.display_text(40, '[M] - Main Menu '             , -240 * self.ratio, 1200 * self.ratio, self.win)
            game_functions.display_text(40, '[R] - Restart   '             , -240 * self.ratio, 1240 * self.ratio, self.win)
            game_functions.display_text(40, '[Q] - Quit      '             , 320 * self.ratio, 1200 * self.ratio, self.win)
            game_functions.display_image(self.images[6], 0 , 640 * self.ratio, self.win)
        
        if self.lose:
            game_functions.display_text(40, '[M] - Main Menu '             , -240 * self.ratio, 1200 * self.ratio, self.win)
            game_functions.display_text(40, '[R] - Restart   '             , -240 * self.ratio, 1240 * self.ratio, self.win)
            game_functions.display_text(40, '[Q] - Quit      '             , 320 * self.ratio, 1200 * self.ratio, self.win)
            game_functions.display_image(self.images[5], 0 , 640 * self.ratio, self.win)

        #display icons
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["SFX"] == "false": game_functions.display_image(self.images[8], -700 * self.ratio, 90 * self.ratio, self.win)
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["Music"] == "false": game_functions.display_image(self.images[9], -750 * self.ratio, 90 * self.ratio, self.win)
            

    def init_objects(self, lvl_lable, lvl_structure):
        self.player_objects.clear()
        self.alien_1_objects.clear()
        self.winner = False
        self.lose = False
        self.pauze = False
        self.score = 0
        self.level_string = lvl_lable
        
        # Read the CSV file
        with open(lvl_structure, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row_idx, row in enumerate(reader):
                for col_idx, value in enumerate(row):
                    x = col_idx
                    y = row_idx
                    if value == '1':                     #|            x              |               y            |widht|height|vel|   image      |  ratio    |
                        self.alien_1_objects.append(alien(self.ratio * (525 + x * 160), self.ratio * (200 + y * 50), 60  ,  45  , 2, self.images[13], self.ratio))
                    if value == '2':
                        self.alien_1_objects.append(alien(self.ratio * (525 + x * 160), self.ratio * (200 + y * 50), 60  ,  45  , 4, self.images[13], self.ratio))

        # Example player object creation
        player_1 = player(self.ratio * 1280, self.ratio * 1200, self.ratio)
        self.player_objects.append(player_1)
        
        
    def keyboard_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit(0)
        elif keys[pygame.K_r]:
            self.init_objects()
        elif keys[pygame.K_m]:
            self.running = False
            
    def resume_game(self):
        self.pauze = False
        for obj in self.alien_1_objects: obj.vel = 2


    def main(self, game_functions, lvl_lable, lvl_structure):
        self.init_lvl(global_game_functions)
        self.init_objects(lvl_lable, lvl_structure)

        main_button = Button(1130, 580, 300, 60, "Main Menu", 40, lambda: setattr(self, 'running', False))
        restart_button = Button(1130, 660, 300, 60, "Resume", 40, lambda: self.resume_game())
        settings_button = Button(1130, 740, 300, 60, "Settings", 40, lambda: setattr(self, 'settings_open', True))
        quit_button = Button(1130, 820, 300, 60, "Quit Game", 40, lambda: (pygame.quit(), sys.exit(0)))

        music_switch = Button(1270, 600, 100, 40, "Music", 25, lambda: game_functions.mute_sound_toggle("Music"))
        sfx_switch = Button(1270, 650, 100, 40, "SFX", 25, lambda: game_functions.mute_sound_toggle("SFX"))
        back_button = Button(1130, 820, 300, 60, "Back", 40, lambda: setattr(self, 'settings_open', False))

        self.pauze_pushbuttons = [main_button, restart_button, settings_button, quit_button]
        self.settings_pushbuttons = [back_button]
        self.settings_switches = [sfx_switch, music_switch]


        move_down = False
        self.running = True

        #Start Main Loop
        while self.running:
            pygame.time.delay(11)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if self.settings_open:
                    back_button.handle_event(event)
                    sfx_switch.handle_event(event)
                    music_switch.handle_event(event)
                elif self.pauze:
                    main_button.handle_event(event)
                    restart_button.handle_event(event)
                    settings_button.handle_event(event)
                    quit_button.handle_event(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s: game_functions.mute_sound_toggle("SFX")
            
        #Moving the aliens down
            if self.alien_1_objects[0].x < (1280 * self.ratio):
                 move_down = True
            if (self.alien_1_objects[0].x > 1280 * self.ratio) and move_down:
                for obj in self.alien_1_objects: obj.y += (50 * self.ratio)
                move_down = False
                    
        #Check if aliens get hit
            for obj in self.alien_1_objects:
                if game_functions.alien_hit(obj, self.player_objects[0].bullets, self.images[7], self.sounds[2], self.win) == True:
                    self.score += 1
                    
            if self.player_objects[0].shootloop > 0: self.player_objects[0].shootloop += 1
            if self.player_objects[0].shootloop > 3: self.player_objects[0].shootloop = 0

            if not self.pauze:
                for bullet in self.player_objects[0].bullets:
                    if bullet.y < 1360 * self.ratio and bullet.y > 80 * self.ratio:
                            bullet.y -= bullet.vel
                    else:
                        self.player_objects[0].bullets.pop(self.player_objects[0].bullets.index(bullet))

        #player controls
            keys = pygame.key.get_pressed()
            if not self.pauze:
                if keys[pygame.K_SPACE] and self.player_objects[0].shootloop == 0:
                    if len(self.player_objects[0].bullets) < 1:
                        self.player_objects[0].bullets.append(projectile(
                            round(self.player_objects[0].x + self.player_objects[0].width //2), 
                            round(self.player_objects[0].y + self.player_objects[0].height//2), 10, (0,255,255), self.ratio))
                        with open("settings.json", 'r') as file:
                            data = json.load(file)
                            if data["SFX"] == "true": self.sounds[0].play()
                    
                        
            if keys[pygame.K_LEFT] and self.player_objects[0].x > 480 * self.ratio:
                self.player_objects[0].x -= self.player_objects[0].vel
                self.player_objects[0].left = True
                self.player_objects[0].right = False
            elif keys[pygame.K_RIGHT] and self.player_objects[0].x < 2080 * self.ratio - self.player_objects[0].width:
                self.player_objects[0].x += self.player_objects[0].vel
                self.player_objects[0].left = False
                self.player_objects[0].right = True
            else:
                self.player_objects[0].left = False
                self.player_objects[0].right = False
                                
        
        #Pauze game         
            if keys[pygame.K_ESCAPE] and not self.winner and not self.lose:
                self.pauze = True

            if self.pauze:
                for obj in self.alien_1_objects: obj.vel = 0
                
                    
        #Check for win
            all_aliens_invisible = True
            for obj in self.alien_1_objects:
                if obj.visible == True:
                    all_aliens_invisible = False
            if all_aliens_invisible == True:
                for obj in self.alien_1_objects: obj.vel = 0
                self.winner = True
                self.keyboard_inputs()
        
        #Check for lose
            alien_to_low = False
            for obj in self.alien_1_objects:
                if obj.y + obj.height > self.player_objects[0].y:
                    alien_to_low = True
            if alien_to_low == True:
                with open("settings.json", 'r') as file:
                    data = json.load(file)
                    if data["SFX"] == "true": self.sounds[1].play()
                for obj in self.alien_1_objects: obj.vel = 0                
                self.lose = True
                self.keyboard_inputs()

        #Refresh screen
            pygame.display.update()
            self.update_screen(game_functions)
