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
			scaled_images.append(pygame.transform.smoothscale(x, (image_width * self.ratio, image_height * self.ratio)))
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
	def __init__(self, x, y, width, height, vel, alien_image, ratio, direction, hp, type):
		self.x = x * ratio
		self.y = y * ratio
		if direction == "right": 
			self.end = self.x + (800 * ratio)
			self.path = [self.x , self.end]
		else: 
			self.end = self.x - (800 * ratio)
			self.path = [self.end , self.x]

		self.width = width * ratio
		self.height = height * ratio
		self.vel = vel * ratio
		self.image = alien_image
		self.ratio = ratio
		self.direction = direction
		self.hp = hp
		self.type = type

		self.start_hp = hp
		self.start_x = x
		self.start_y = y
		self.hitbox = (self.x, self.y, width * ratio, height * ratio)
		self.visible = True
		self.move_down = False

	def draw(self, win):
		self.hitbox = (self.x - 2, self.y - 1, self.width, self.height)
		# pygame.draw.rect(win, (255,0,0), self.hitbox,2)
		
		if self.visible == True:
			self.move()
			win.blit(self.image, (self.x,self.y))
			pygame.draw.rect(win, (255,0,0), (self.hitbox[0] + 5 * self.ratio, (self.hitbox[1] - 8 * self.ratio) , 55 * self.ratio, 5))
			pygame.draw.rect(win, (0,128,0), (self.hitbox[0] + 5 * self.ratio , (self.hitbox[1] - 8 * self.ratio) , ((55 / self.start_hp) * self.hp) * self.ratio, 5))
			

	def move(self):
		if self.direction == 'right':
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.direction = 'left'
		elif self.direction == 'left':
			if self.x - self.vel > self.path[0]:
				self.x -= self.vel
			else:
				self.direction = 'right'

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