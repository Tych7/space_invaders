import pygame
import os
import sys
import json
import math


class Button:
    ratio = 0
    controller = None

    def set_ratio(self):
        with open("settings.json", 'r') as file: 
            data = json.load(file)
            self.ratio = data["ratio"]
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
			
    def __init__(self, x, y, width, height, text, font_size, action, image=None):
        self.set_ratio()
        self.text = text
        self.action = action
        self.x = x * self.ratio
        self.y = y * self.ratio
        self.width = width * self.ratio
        self.height = height * self.ratio
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font_size = font_size
        self.image = image
	
    def draw_pushbutton_rect(self, win):
        pygame.draw.rect(win, (0, 0, 0), self.rect, 0, border_radius=int(22 * self.ratio))
        mouse_pos = pygame.mouse.get_pos()
        mouse_over = self.rect.collidepoint(mouse_pos)
        
        if mouse_over: pygame.draw.rect(win, (4, 245, 4), self.rect, int(6 * self.ratio), border_radius=int(22 * self.ratio))
        else: pygame.draw.rect(win, (195, 195, 195), self.rect, int(6 * self.ratio), border_radius=int(22 * self.ratio))

        font_size = int(self.font_size * min(self.ratio, self.ratio))
        font = pygame.font.SysFont('couriernew', font_size, True)

        renderd_text = font.render(self.text, 1, (4, 245, 4))
        text_x = (self.width / 2) - (font.size(self.text)[0] / 2)
        text_y = (self.height / 2) - (font.size(self.text)[1] / 2)
        win.blit(renderd_text, (self.x + text_x, self.y + text_y))

    def draw_pushbutton_circle(self, win):
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.width)
        image_width, image_height = self.image.get_size()
        centered_x = self.x - (image_width / 2)
        centered_y = self.y - (image_height / 2)
        win.blit(self.image, (centered_x, centered_y))

        mouse_pos = pygame.mouse.get_pos()
        distance = math.sqrt((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)
        mouse_over = distance <= self.width
        if mouse_over: pygame.draw.circle(win, (4, 245, 4), (self.x, self.y), self.width, int(6 * self.ratio))
        else: pygame.draw.circle(win, (195, 195, 195), (self.x, self.y), self.width, int(6 * self.ratio))

    def draw_switch(self, win):
        pygame.draw.rect(win, (0, 0, 0), self.rect, 0, border_radius=int(22 * self.ratio))
        pygame.draw.rect(win, (195, 195, 195), self.rect, int(5 * self.ratio), border_radius=int(22 * self.ratio))
        font_size = int(self.font_size * min(self.ratio, self.ratio))
        font = pygame.font.SysFont('couriernew', font_size, True)
        text = ""
        text_y = (self.height / 2) - (font.size(self.text)[1] / 2)

        lable_text = font.render(self.text + ":", 1, (4, 245, 4))
        win.blit(lable_text, (self.x - (100 * self.ratio), self.y + text_y))

        with open("settings.json", 'r') as file:
            data = json.load(file)
            if data[self.text] == "true": 
                text = "ON"
                renderd_text = font.render(text, 1, (4, 245, 4))
                pygame.draw.circle(win, (195, 195, 195), (self.x + (20 * self.ratio), self.y + self.height/2), (12 * self.ratio))
                win.blit(renderd_text, (self.x + (50 * self.ratio), self.y + text_y))
            else: 
                text = "OFF"
                renderd_text = font.render(text, 1, (255, 0, 0))
                pygame.draw.circle(win, (195, 195, 195), (self.x + (80 * self.ratio), self.y + self.height/2), (12 * self.ratio))
                win.blit(renderd_text, (self.x + (10 * self.ratio), self.y + text_y + (3 * self.ratio)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.image != None:
                mouse_pos = pygame.mouse.get_pos()
                distance = math.sqrt((mouse_pos[0] - self.x)**2 + (mouse_pos[1] - self.y)**2)
                if distance <= self.width:	
                    self.action()
            else:
               if self.rect.collidepoint(event.pos):
                    self.action()
        elif event.type == pygame.JOYBUTTONDOWN:
            if self.controller.get_button(0): self.action()

class global_game_functions:
	ratio = 0
 
	def set_ratio(self):
		with open("settings.json", 'r') as file: 
			data = json.load(file)
			self.ratio = data["ratio"]
    
	def mute_sound_toggle(self, setting):
		with open("settings.json", 'r') as file: 
			data = json.load(file)

			if data[setting] == "false":
				with open("settings.json", 'w') as file:
					data[setting] = "true"
					json.dump(data, file, indent=4)
				if setting == "Music":
					pygame.mixer.music.unpause()
			else:
				with open("settings.json", 'w') as file:
					data[setting] = "false"
					json.dump(data, file, indent=4)
				if setting == "Music":
					pygame.mixer.music.pause()

	def load_images(self, unloaded_images):
		loaded_images = []
		directory = "images/"
		for x in unloaded_images:
			loaded_images.append(pygame.image.load(directory + x).convert_alpha())
		return loaded_images

	def load_sounds(self, unloaded_sounds):
		loaded_sounds = []
		directory = "sounds/"
		for x in unloaded_sounds:
			loaded_sounds.append(pygame.mixer.Sound(directory + x))
		self.sounds = loaded_sounds

	def scale_images(self, loaded_images):
		scaled_images = []
		for x in loaded_images:
			image_width, image_height = x.get_size()
			scaled_images.append(pygame.transform.scale(x, (image_width * self.ratio, image_height * self.ratio)))
		return scaled_images

	def display_image(self, image, x, y, win):
		screen_center  = ((pygame.display.get_surface().get_size()[0])/2)
		image_width = 0
		if x == 0:
			image_width = screen_center - ((image.get_size()[0]) / 2)	
		elif x < 0:
			image_width = screen_center - image.get_size()[0] + x
		else:
			image_width = screen_center + x

		win.blit(image, (image_width, y))
  
	def display_text(self, size, text, width, height, win):
		font_size = int(size * min(self.ratio, self.ratio))
		font = pygame.font.SysFont('couriernew', font_size, True)
		renderd_text = font.render(text, 1, (4, 245, 4))
  
		screen_center  = (pygame.display.get_surface().get_size()[0])/2
		image_width = 0
		if width == 0:
			image_width = screen_center - (font.size(text)[0] / 2)
		elif width < 0:
			image_width = screen_center - font.size(text)[0] + width 
		else:
			image_width = screen_center + width
  
		win.blit(renderd_text, (image_width, height))
	
	def alien_hit(self, alien, bullets, image, sound, win):
		if alien.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alien.hitbox[1] + alien.hitbox[3] and bullet.y + bullet.radius > alien.hitbox[1]:
					if bullet.x + bullet.radius > alien.hitbox[0] and bullet.x - bullet.radius < alien.hitbox[0] + alien.hitbox[2]:
						alien.hit(win, image, sound)
						bullets.pop(bullets.index(bullet))
						return True
		return False
	

class alien(object):
	def __init__(self, x, y, width, height, vel, alien_image, ratio, type):
		self.x = x
		self.y = y
		self.width = width * ratio
		self.height = height * ratio
		self.end = self.x + (800 * ratio)
		self.path = [self.x , self.end]
		self.vel = vel * ratio
		self.hitbox = (self.x, self.y, width * ratio, height * ratio)
		self.health = 0
		self.visible = True
		self.shootloop = 0
		self.ratio = ratio
		self.image = alien_image
		self.type = type
		self.direction = ""

	def draw(self, win):
		self.move()
		if self.visible == True:
			win.blit(self.image, (self.x,self.y))
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0] + 5 * self.ratio, (self.hitbox[1] - 8 * self.ratio) , 55 * self.ratio, 5))
			pygame.draw.rect(win, (0,128,0), (self.hitbox[0] + 5 * self.ratio , (self.hitbox[1] - 8 * self.ratio) , (55 * self.ratio) - (55 * (0 - self.health)), 5))
			self.hitbox = (self.x - 2, self.y - 1, self.width, self.height)
			# pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	def move(self):
		if self.visible == True:
			if self.direction == 'right':
				if self.x + self.vel < self.path[1]:
					self.x += self.vel
				else:
					self.direction = 'left'
			else:
				if self.x - self.vel > self.path[0]:
					self.x -= self.vel
				else:
					self.direction = 'right'

	def hit(self, win, image, sound):
		if self.health > 0:
			self.health -= 1
		else:
			self.visible = False
			win.blit(image, (self.x,self.y))
			with open("settings.json", 'r') as file:
				data = json.load(file)
				if data["SFX"] == "true": sound.play()
			print('hit')

class projectile(object):
	def __init__(self,x,y,radius,color, ratio):
		self.x = x
		self.y = y
		self.radius = radius * ratio 
		self.color = color
		self.vel = 12 * ratio

	def draw(self,win):
		pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class player(object):
	def __init__(self,x,y, ratio):
		self.x = x
		self.y = y
		self.height = 80 * ratio
		self.width = 58 * ratio
		self.vel = 8 * ratio
		self.left = False
		self.right = False
		self.hitbox = (self.x, self.y, 58, 80)
		self.visible = True
		self.bullets = []
		self.shootloop = 0

	def draw(self, win, images):
		if self.left:
			win.blit(images[2], (self.x,self.y))
		elif self.right:
			win.blit(images[1], (self.x,self.y))
		else:
			win.blit(images[0], (self.x,self.y))

		self.hitbox = (self.x, self.y, self.width, self.height)
		# pygame.draw.rect(win, (255,0,0), self.hitbox,2)