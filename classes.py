import pygame
import os
import sys

class global_game_functions:
	def mute_sound_toggle(self):
		with open('mute.txt', 'r') as file:
			content = file.read()
			if content.strip() == "false":
				with open('mute.txt', 'w') as file:
					file.write("true")
				pygame.mixer.music.unpause()
			elif content.strip() == "true":
				with open('mute.txt', 'w') as file:
					file.write("false")
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

	def display_image(self, image, width, height, win):
		screen_center  = ((pygame.display.get_surface().get_size()[0])/2)
		image_width = 0
		if width == 0:
			image_width = screen_center - ((image.get_size()[0]) / 2)	
		elif width < 0:
			image_width = screen_center - image.get_size()[0] + width
		else:
			image_width = screen_center + width

		win.blit(image, (image_width, height))
	
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
	

class alien_1(object):
	def __init__(self,x,y, ratio, vel):
		self.x = x
		self.y = y
		self.width = 34 * ratio
		self.height = 27 * ratio
		self.end = self.x + (500 * ratio)
		self.path = [self.x , self.end]
		self.vel = vel * ratio
		self.hitbox = (self.x, self.y, 34 * ratio, 27 * ratio)
		self.health = 0
		self.visible = True
		self.shootloop = 0
		self.ratio = ratio

	def draw(self, win, image):
		if self.y < (1080 * self.ratio):
			self.move()
			if self.visible == True:
				win.blit(image, (self.x,self.y))
				pygame.draw.rect(win, (255,0,0), (self.hitbox[0] * self.ratio, (self.hitbox[1] - 5) * self.ratio, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0] * self.ratio, (self.hitbox[1] - 5) * self.ratio, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x - 2, self.y - 1, self.width, self.height)
				# pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	def move(self):
		if self.vel > 0:
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1
		else:
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel = self.vel * -1

	def hit(self, win, image, sound):
		if self.health > 0:
			self.health -= 1
		else:
			self.visible = False
			self.vel = 0
			win.blit(image, (self.x,self.y))
			with open('mute.txt', 'r') as file:
				content = file.read()
				if content.strip() == "true": sound.play()
			print('hit')

class projectile(object):
	def __init__(self,x,y,radius,color, ratio):
		self.x = x
		self.y = y
		self.radius = radius * ratio 
		self.color = color
		self.vel = 8 * ratio

	def draw(self,win):
		pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class player(object):
	def __init__(self,x,y, ratio):
		self.x = x
		self.y = y
		self.height = 45 * ratio
		self.width = 35 * ratio
		self.vel = 5 * ratio
		self.left = False
		self.right = False
		self.hitbox = (self.x, self.y, 35, 45)
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