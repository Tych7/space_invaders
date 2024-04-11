import pygame
import sys
import os
import json

from classes import global_game_functions,alien_1, projectile, player

class level_1:

    #global static data
    images = []
    sounds = []
    win = None
    player_objects = [] 
    alien_1_objects = []
    ratio = 0
    level_string = "level 1"
    alien_rows = []
    alien_collums = []

    #global variable data
    score = 0
    pauze = False
    winner = False
    lose = False
    running = True

    def set_ratio(self, loaded_images, game_functions):
        bg_width = loaded_images[0].get_size()[0]
        screen_width = pygame.display.get_surface().get_size()[0]

        self.ratio = screen_width / bg_width
        game_functions.ratio = self.ratio

    def init_lvl(self, game_functions):
        pygame.init()

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(self.level_string)

        images = [
            "bgA.jpg",
            "lvl_select.png",
            "ship.png",
            "shipright.png",
            "shipleft.png",
            "gameover.png",
            "win.png",
            "explo.png",
            "mute.png",
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
        
        #display static images
        game_functions.display_image(self.images[0], 0 , 0, self.win)
        game_functions.display_image(self.images[1], -640 * self.ratio, 1300 * self.ratio, self.win)

        #display aliens type 1
        for x in self.alien_1_objects: x.draw(self.win, self.images[9])

        #display player
        player_images = [self.images[2], self.images[3], self.images[4]]
        for x in self.player_objects: x.draw(self.win, player_images)

        #display text
        game_functions.display_text(50,'Score: ' + str(self.score), 520 * self.ratio, 100 * self.ratio, self.win)
        game_functions.display_text(50,self.level_string, -700 * self.ratio, 1325 * self.ratio, self.win)
        
        if self.pauze:
            game_functions.display_text(40, '[M] - Main Menu '             , -240 * self.ratio, 1200 * self.ratio, self.win)
            game_functions.display_text(40, '[R] - Restart   '             , -240 * self.ratio, 1240 * self.ratio, self.win)
            game_functions.display_text(40, '[Q] - Quit      '             , 320 * self.ratio, 1200 * self.ratio, self.win)
            
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

        #display mute icon
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["music"] == "false": game_functions.display_image(self.images[8], -720 * self.ratio, 90 * self.ratio, self.win)
            
        #display projectiles
        for bullet in self.player_objects[0].bullets: bullet.draw(self.win)

    def init_objects(self):
        self.player_objects.clear()
        self.alien_1_objects.clear()
        self.winner = False
        self.lose = False
        self.pauze = False
        self.score = 0
        
        index = 0
        while index < 5: self.alien_rows.append(160 + (index * 50)); index += 1
        index = 0
        while index < 5: self.alien_collums.append(525 + (index * 160)); index += 1
        
        player_1 = player(self.ratio * 1280, self.ratio * 1200, self.ratio); self.player_objects.append(player_1)

        self.alien_1_objects.append(alien_1(self.ratio * self.alien_collums[0],self.ratio * self.alien_rows[0], self.ratio, 2))
        self.alien_1_objects.append(alien_1(self.ratio * self.alien_collums[1],self.ratio * self.alien_rows[0], self.ratio, 2))
        self.alien_1_objects.append(alien_1(self.ratio * self.alien_collums[2],self.ratio * self.alien_rows[0], self.ratio, 2))
        self.alien_1_objects.append(alien_1(self.ratio * self.alien_collums[3],self.ratio * self.alien_rows[0], self.ratio, 2))
        self.alien_1_objects.append(alien_1(self.ratio * self.alien_collums[4],self.ratio * self.alien_rows[0], self.ratio, 2))
        
        
    def keyboard_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit(0)
        elif keys[pygame.K_r]:
            self.init_objects()
        elif keys[pygame.K_m]:
            self.running = False


    def main(self):
        game_functions = global_game_functions()
        self.init_lvl(global_game_functions)
        self.init_objects()

        move_down = False
        self.running = True

        #Start Main Loop
        while self.running:
            pygame.time.delay(11)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s: game_functions.mute_sound_toggle()
            
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
                            if data["music"] == "true": self.sounds[0].play()
                    
                        
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
                self.keyboard_inputs()
                    
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
                    if data["music"] == "true": self.sounds[1].play()
                for obj in self.alien_1_objects: obj.vel = 0                
                self.lose = True
                self.keyboard_inputs()

        #Refresh screen
            pygame.display.update()
            self.update_screen(game_functions)
