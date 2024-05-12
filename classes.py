import pygame
import os
import sys
import json
import math
from pygame import gfxdraw

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
		renderd_text = font.render(text, 1, (112, 228, 209))
  
		screen_center  = (pygame.display.get_surface().get_size()[0])/2
		image_width = 0
		if width == 0:
			image_width = screen_center - (font.size(text)[0] / 2)
		elif width < 0:
			image_width = screen_center - font.size(text)[0] + width 
		else:
			image_width = screen_center + width
  
		win.blit(renderd_text, (image_width, height))
	
	def object_hit(self, obj, bullets, image, sound, win):
		if obj.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < obj.hitbox[1] + obj.hitbox[3] and bullet.y + bullet.radius > obj.hitbox[1]:
					if bullet.x + bullet.radius > obj.hitbox[0] and bullet.x - bullet.radius < obj.hitbox[0] + obj.hitbox[2]:
						bullets.pop(bullets.index(bullet))
						return True
		return False
	

class alien(object):
	def __init__(self, x, y, alien_image, ratio, direction, hp, type):
		self.x = x * ratio
		self.y = y * ratio
		if direction == ">": 
			self.end = self.x + (800 * ratio)
			self.path = [self.x , self.end]
		else: 
			self.end = self.x - (800 * ratio)
			self.path = [self.end , self.x]

		self.type = type
		self.image = alien_image
		self.ratio = ratio
		self.direction = direction
		self.hp = hp
		self.bullets = []
		self.shootloop = 0
  
		if type == 0:   self.vel = 1 * self.ratio; self.width = 60 * self.ratio; self.height = 45 * self.ratio; self.shooting = False
		elif type == 1: self.vel = 3 * self.ratio; self.width = 60 * self.ratio; self.height = 45 * self.ratio; self.shooting = False
		elif type == 2: self.vel = 6 * self.ratio; self.width = 60 * self.ratio; self.height = 45 * self.ratio; self.shooting = False
		elif type == 3:	self.vel = 3 * self.ratio; self.width = 45 * self.ratio; self.height = 45 * self.ratio; self.shooting = True
  
		self.start_hp = hp
		self.start_x = x
		self.start_y = y
		self.hitbox = (self.x, self.y, self.width, self.height)
		self.visible = True
		self.move_down = False
		self.shoot_delay = 0

	def draw(self, win):
		self.hitbox = (self.x - 2, self.y - 1, self.width, self.height)
		# pygame.draw.rect(win, (255,0,0), self.hitbox,2)

		if self.direction == ">" and self.vel > 1: correction = +5 
		elif self.direction == "<" and self.vel > 1: correction = -5 
		else: correction = 0

		
		if self.visible == True:
			self.move()
			
			win.blit(self.image, (self.x,self.y))
			pygame.draw.rect(win, (255,0,0), ((correction + self.hitbox[0] + ((self.hitbox[2] / 2) - (55 / 2))) * self.ratio, self.hitbox[1] - 8 * self.ratio , 55 * self.ratio, 5))
			pygame.draw.rect(win, (0,128,0), ((correction + self.hitbox[0] + ((self.hitbox[2] / 2) - (55 / 2))) * self.ratio , self.hitbox[1] - 8 * self.ratio , ((55 / self.start_hp) * self.hp) * self.ratio, 5))
	
	def shoot(self, win):
		if self.type == 3: bullet_color = (255,4,252)
		else: bullet_color = (255,255,255)	

		if self.visible:
			if self.shoot_delay <= 0:
				self.bullets.append(projectile(
					round(self.x + self.width // 2),
					round(self.y + self.height // 2), 10, bullet_color, self.ratio))
				self.shoot_delay = 100  
			else:
				self.shoot_delay -= 1

		for bullet in self.bullets:
			if bullet.y < 1360 * self.ratio and bullet.y > 80 * self.ratio:
				bullet.y += bullet.vel
			else:
				self.bullets.pop(self.bullets.index(bullet))
	
	def move(self):
		if self.direction == ">":
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.direction = "<"
		elif self.direction == "<":
			if self.x - self.vel > self.path[0]:
				self.x -= self.vel
			else:
				self.direction = ">"

		if self.start_x < 1200:
			if self.x < ((755 + self.start_x) * self.ratio):
				self.move_down = True
			if (self.x > (755 + self.start_x) * self.ratio) and self.move_down:
				self.y += (55 * self.ratio)
				self.move_down = False
		elif self.start_x > 1200:
			if self.x > ((self.start_x - 755) * self.ratio):
				self.move_down = True
			if (self.x < (self.start_x - 755) * self.ratio) and self.move_down:
				self.y += (55 * self.ratio)
				self.move_down = False

	def hit(self, win, image, sound):
		if self.hp > 1:
			self.hp -= 1
		else:
			self.visible = False
			win.blit(image, (self.x,self.y))
			with open("settings.json", 'r') as file:
				data = json.load(file)
				if data["SFX"] == "true": sound.play()
				

class projectile(object):
	def __init__(self,x,y,radius,color, ratio):
		self.x = x
		self.y = y
		self.radius = radius * ratio 
		self.color = color
		self.vel = 15 * ratio

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
		self.ratio = ratio

	def draw(self, win, images):
		if self.left:
			win.blit(images[2], (self.x,self.y))
		elif self.right:
			win.blit(images[1], (self.x,self.y))
		else:
			win.blit(images[0], (self.x,self.y))

		self.hitbox = (self.x, self.y, self.width, self.height)
		# pygame.draw.rect(win, (255,0,0), self.hitbox,2)
  
	def shoot(self):
		if self.shootloop > 0: self.shootloop += 1
		if self.shootloop > 3: self.shootloop = 0

		for bullet in self.bullets:
			if bullet.y < 1360 * self.ratio and bullet.y > 80 * self.ratio:
					bullet.y -= bullet.vel
			else:
				self.bullets.pop(self.bullets.index(bullet))