import pygame
import sys
import os
import json
import csv
import time

from entities import global_game_functions,alien, projectile, player
from GUI import Button, RectButton, CircleButton, SwitchButton, controller_pointer

class level:
    #global static data
    images = []
    alien_images = []
    sounds = []
    win = None
    controller = None
    player_objects = [] 
    alien_objects = []
    ratio = 0
    state = None
    level_string = ""
    level_structure = None
    alien_rows = []
    alien_collums = []

    pauze_buttons = []
    settings_buttons = []
    win_buttons = []
    lose_buttons = []    
    active_buttons = []

    #global variable data
    score = 0
    lives = 3
    combo_counter = 0
    multiplier = 1
    pauze = False
    winner = False
    lose = False
    running = True
    settings_open = False
    player_move = True
    block_shoot = False


    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]

    def init_lvl(self, game_functions):
        pygame.init()
        self.set_ratio()
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)

        self.win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(self.level_string)

        images = [
            "bgA.png",              #0
            "lvl_select.png",       #1
            "ship.png",             #2
            "shipright.png",        #3
            "shipleft.png",         #4
            "gameover.png",         #5
            "win.png",              #6
            "explo.png",            #7
            "SFX.png",              #8
            "music.png",            #9
            "pauze_menu.png",       #10
            "icon_home.png",        #11
            "icon_quit.png",        #12
            "icon_settings.png",    #13
            "heart_full.png",       #14
            "heart_empty.png",      #15
        ]
        loaded_images = game_functions.load_images(self, images)
        self.images = game_functions.scale_images(self, loaded_images)

        alien_images = [
            "alien_start.png",      #0
            "alien_A.png",          #1
            "alien_B.png",          #2
            "alien_C.png",          #3        
        ]
        loaded_aliens = game_functions.load_images(self, alien_images)
        self.alien_images = game_functions.scale_images(self, loaded_aliens)

        sounds = [
            "laser.wav",
            "gameover.wav",
            "invaderkilled.wav",
            "get_hit.mp3",
        ]
        game_functions.load_sounds(self, sounds)

    def update_screen(self, game_functions, pointer):
        
        #display static images
        game_functions.display_image(self.images[0], 0 , 0, self.win)
        game_functions.display_image(self.images[1], -640 * self.ratio, 1300 * self.ratio, self.win)

        #display aliens
        for alien in self.alien_objects: alien.draw(self.win)

        #display player
        if self.lose == False: player_images = [self.images[2], self.images[3], self.images[4]]
        else: player_images = [self.images[7], self.images[7], self.images[7]]
        for player in self.player_objects: player.draw(self.win, player_images)

        #display text
        game_functions.display_text(60,'SCORE:', 950 * self.ratio, 675 * self.ratio, self.win)

        digits = len(str(abs(self.score)))
        score_alignment = 1040 - ((digits - 1) * 20)
        game_functions.display_text(60,str(self.score), score_alignment * self.ratio, 750 * self.ratio, self.win)

        game_functions.display_text(50,"Combo X" + str(self.multiplier), 1020 * self.ratio, 600 * self.ratio, self.win)
        
        #display score
        lvl_number = int(self.level_string.split(" ")[1])
        if lvl_number > 9:  lvl_label_x = -675 * self.ratio
        else: lvl_label_x = -700 * self.ratio
        
        game_functions.display_text(50,self.level_string, lvl_label_x , 1325 * self.ratio, self.win)

        if self.state == 'waves':
            hearts = []
            for i in range(self.lives): hearts.append(14)
            for i in range(3 - len(hearts)): hearts.append(15)
            for i in range(len(hearts)): 
                image_x = (675 + (i * 40)) * self.ratio
                game_functions.display_image(self.images[hearts[i]], image_x , 100 * self.ratio, self.win)


        #display projectiles
        for player_bullet in self.player_objects[0].bullets: player_bullet.draw(self.win)
        
        for alien in self.alien_objects:
            for alien_bullet in alien.bullets: alien_bullet.draw(self.win)

        #display sound icons
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["SFX"] == "false": game_functions.display_image(self.images[8], -700 * self.ratio, 90 * self.ratio, self.win)
        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data["Music"] == "false": game_functions.display_image(self.images[9], -750 * self.ratio, 90 * self.ratio, self.win)
        

        if self.pauze or self.winner or self.lose:
            overlay_color = (0, 0, 0, 200) 
            overlay = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
            overlay.fill(overlay_color)
            self.win.blit(overlay, (0, 0))

        if self.pauze:
            game_functions.display_image(self.images[10], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, self.level_string, 0 , 515 * self.ratio, self.win)
            for button in self.pauze_buttons: button.draw(self.win)
            pointer.draw(self.win, self.pauze_buttons)
     
        if self.winner:
            game_functions.display_image(self.images[10], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, self.level_string, 0 , 515 * self.ratio, self.win)
            for button in self.win_buttons: button.draw(self.win)
            game_functions.display_image(self.images[6], 0 , 300 * self.ratio, self.win)#
            pointer.draw(self.win, self.win_buttons)
        
        if self.lose:
            game_functions.display_image(self.images[10], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, self.level_string, 0 , 515 * self.ratio, self.win)
            for button in self.lose_buttons: button.draw(self.win)
            game_functions.display_image(self.images[5], 0 , 300 * self.ratio, self.win)
            pointer.draw(self.win, self.lose_buttons)
            
        if self.settings_open:
            game_functions.display_image(self.images[10], 0 , 500 * self.ratio, self.win)
            game_functions.display_text(35, 'SETTINGS', 0 , 515 * self.ratio, self.win)
            for button in self.settings_buttons: button.draw(self.win)
            pointer.draw(self.win, self.settings_buttons)
            

    def init_objects(self, lvl_lable, lvl_structure, state):
        self.player_objects.clear()
        self.alien_objects.clear()
        self.winner = False
        self.lose = False
        self.pauze = False
        self.player_move = True
        self.level_string = lvl_lable
        self.level_structure = lvl_structure
        self.state = state
        self.block_shoot = False

        if self.state == 'level': 
            self.score = 0
            self.combo_counter = 0
            self.multiplier = 1
        
        # Read the CSV file
        with open(lvl_structure, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row_idx, row in enumerate(reader):
                for col_idx, value in enumerate(row):
                    x = col_idx
                    y = row_idx

                    dir = ""
                    hp = 0
                    alien_type = 0

                    index = 0
                    for char in value:
                        if index == 0: dir = char
                        elif index == 1: alien_type = int(char)
                        elif index == 3: hp = int(char) 
                        index = index + 1

                    if dir == ">":                     #|       x       |        y      |       image                  |  ratio    | dir | hp | type     |
                        self.alien_objects.append(alien((525  + x * 160), (200 + y * 55), self.alien_images[alien_type], self.ratio, ">", hp, alien_type))
                    if dir == "<":
                        self.alien_objects.append(alien((1965 - x * 160), (200 + y * 55), self.alien_images[alien_type], self.ratio, "<", hp, alien_type))


        # Example player object creation
        player_1 = player(self.ratio * 1280, self.ratio * 1200, self.ratio)
        self.player_objects.append(player_1)
            
    def resume_lvl(self):
        self.block_shoot = True
        self.pauze = False
        for obj in self.alien_objects: 
            obj.moving = True
            self.player_move = True

    
    def next_lvl(self):
        self.block_shoot = True
        current_level = int(self.level_string.split(" ")[1])
        next_level = current_level + 1
        file_path = f"levels/lvl_{next_level}.csv"
        
        if os.path.exists(file_path):
            self.init_objects(self.level_string.split(" ")[0] + " " + str(next_level), file_path, self.state)
        else:
            print("Error: File not found:", file_path)
    
    def restart_lvl(self):
        self.block_shoot = True
        if self.state == 'level': 
            self.init_objects(self.level_string, self.level_structure, self.state)
        elif self.state == 'waves': 
            self.init_objects("Wave 1", "levels/lvl_1.csv", self.state)
            self.score = 0
            self.lives = 3

    def shoot_bullet(self, obj):
        if self.player_move == True:          
            if not self.pauze or not self.winner or not self.lose or not self.settings_open:               
                if len(obj.bullets) < 1 and obj.shootloop == 0:
                        obj.bullets.append(projectile(
                            round(obj.x + obj.width //2), 
                            round(obj.y + obj.height//2), 10, (0,255,255), self.ratio))
                        with open("settings.json", 'r') as file:
                            data = json.load(file)
                            if data["SFX"] == "true": self.sounds[0].play()


    def main(self, game_functions, lvl_lable, lvl_structure, state):
        self.init_lvl(global_game_functions)
        self.init_objects(lvl_lable, lvl_structure, state)
        pointer = controller_pointer(1280 * self.ratio, 825 * self.ratio, 12)

        #Pauze buttons
        home_button = CircleButton(1170, 825, 50, 50, "Controls", 40, lambda: setattr(self, 'running', False), self.images[11])
        settings_button = CircleButton(1280, 825, 50, 50, "Settings", 40, lambda: setattr(self, 'settings_open', True), self.images[13])
        quit_button = CircleButton(1390, 825, 50, 50, "Quit Game", 40, lambda: (pygame.quit(), sys.exit(0)), self.images[12])
        resume_button = RectButton(1130, 680, 300, 60, "Resume", 40, lambda: self.resume_lvl())
        restart_button = RectButton(1130, 600, 300, 60, "Restart", 40, lambda: self.restart_lvl())

        #Settings buttons
        music_switch = SwitchButton(1270, 600, 100, 40, "Music", 25, lambda: game_functions.mute_sound_toggle("Music"))
        sfx_switch = SwitchButton(1270, 650, 100, 40, "SFX", 25, lambda: game_functions.mute_sound_toggle("SFX"))
        back_button = RectButton(1130, 820, 300, 60, "Back", 40, lambda: setattr(self, 'settings_open', False))

        #Win/lose buttons
        next_lvl_button = RectButton(1130, 680, 300, 60, "Next Level", 40, lambda: self.next_lvl())
        big_restart_button = RectButton(1130, 600, 300, 120, "Restart", 40, lambda: self.restart_lvl())

        self.pauze_buttons = [resume_button, restart_button, settings_button, home_button, quit_button]
        self.settings_buttons = [back_button, sfx_switch, music_switch]
        self.win_buttons = [settings_button, home_button, quit_button, next_lvl_button, restart_button]
        self.lose_buttons = [settings_button, home_button, quit_button, big_restart_button]

        self.running = True
        
        clock = pygame.time.Clock()

        #Start Main Loop
        while self.running:
            if self.settings_open: self.active_buttons = self.settings_buttons
            elif self.pauze: self.active_buttons = self.pauze_buttons
            elif self.winner: self.active_buttons = self.win_buttons
            elif self.lose: self.active_buttons = self.lose_buttons
            else: self.active_buttons = []

            
            clock.tick(60)
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                for button in self.active_buttons:
                    button.handle_event(event)
                pointer.move_pointer(self.active_buttons)

                if event.type == pygame.JOYBUTTONUP:
                    self.block_shoot = False

                if event.type == pygame.JOYBUTTONDOWN:
                    pointer.handle_event(self.active_buttons)
                    if self.controller is not None and self.controller.get_button(0) and self.block_shoot == False:
                        self.shoot_bullet(self.player_objects[0])
                        self.block_shoot = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.shoot_bullet(self.player_objects[0])
        

        #player move controls
            if self.player_move == True:         
                if (keys[pygame.K_LEFT] or (self.controller is not None and (self.controller.get_axis(0) < -0.5 or self.controller.get_button(13)))) and self.player_objects[0].x > 480 * self.ratio:
                    self.player_objects[0].x -= self.player_objects[0].vel
                    self.player_objects[0].left = True
                    self.player_objects[0].right = False
                elif (keys[pygame.K_RIGHT] or (self.controller is not None and (self.controller.get_axis(0) > 0.5 or self.controller.get_button(14)))) and self.player_objects[0].x < 2080 * self.ratio - self.player_objects[0].width:
                    self.player_objects[0].x += self.player_objects[0].vel
                    self.player_objects[0].left = False
                    self.player_objects[0].right = True
                else:
                    self.player_objects[0].left = False
                    self.player_objects[0].right = False
                    
        #Check if object gets hit
            for alien_obj in self.alien_objects:
                if game_functions.object_hit(alien_obj, self.player_objects[0].bullets) == True:
                    self.score += 1
                    self.combo_counter += 1
                    alien_obj.hit(self.win, self.images[7], self.sounds[2])
                else:
                    self.combo_counter = 0

        #set score multilier
            if self.combo_counter > 2: self.multiplier = 2
            if self.combo_counter > 3: self.multiplier = 3


            for player_obj in self.player_objects:
                for alien_obj in self.alien_objects:
                    if game_functions.object_hit(player_obj, alien_obj.bullets) == True:
                        if self.state == 'level':
                            with open("settings.json", 'r') as file:
                                data = json.load(file)
                                if data["SFX"] == "true": self.sounds[1].play()
                            for obj in self.alien_objects: 
                                obj.vel = 0
                                obj.shooting = False                
                            self.lose = True
                            self.player_move = False
                        elif self.state == 'waves':
                            if self.lives == 1:
                                for obj in self.alien_objects: 
                                    obj.vel = 0
                                    obj.shooting = False                
                                self.lose = True
                                self.player_move = False
                                with open("settings.json", 'r') as file:
                                    data = json.load(file)
                                    if data["SFX"] == "true": self.sounds[1].play()
                            else:
                                with open("settings.json", 'r') as file:
                                    data = json.load(file)
                                    if data["SFX"] == "true": self.sounds[3].play()
                                self.lives -= 1
                    
        #Shoot bullets
            if not self.pauze:
                for player in self.player_objects:
                    player.shoot()
                for alien in self.alien_objects:
                    if alien.shooting == True: 
                        alien.shoot(self.win)
        
        #Pauze game         
            if (keys[pygame.K_ESCAPE] or (self.controller is not None and self.controller.get_button(6))) and not self.winner and not self.lose:
                self.pauze = True
                self.player_move = False
            if self.pauze:
                for obj in self.alien_objects: obj.moving = False
                    
        #Check for win
            all_aliens_invisible = True
            for obj in self.alien_objects:
                if obj.visible == True:
                    all_aliens_invisible = False
            if all_aliens_invisible == True:
                if self.state == 'level':
                    for obj in self.alien_objects: obj.vel = 0
                    self.winner = True
                    self.player_move = False
                elif self.state == 'waves': self.next_lvl()
                    
        #Check for lose
            alien_to_low = False
            for obj in self.alien_objects:
                if obj.y + obj.height > self.player_objects[0].y:
                    alien_to_low = True
            if alien_to_low == True:
                with open("settings.json", 'r') as file:
                    data = json.load(file)
                    if data["SFX"] == "true": self.sounds[1].play()
                if self.state == 'level':
                    for obj in self.alien_objects: obj.vel = 0                
                    self.lose = True
                    self.player_move = False
                elif self.state == 'waves':
                    print("PLACEHOLDER")

        #Refresh screen
            pygame.display.update()
            self.update_screen(game_functions, pointer)
