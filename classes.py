import pygame
import os
import sys

class global_game_functions:
	ratio = 0

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
		self.loaded_sounds = loaded_sounds
    
	def scale_images(self, loaded_images):
		scaled_images = []
		for x in loaded_images:
			image_width, image_height = x.get_size()
			scaled_images.append(pygame.transform.scale(x, (image_width * self.ratio, image_height * self.ratio)))
		return scaled_images
	
	def display_text(self, size, text, width, height, win):
		font_size = int(size * min(self.ratio, self.ratio))
		font = pygame.font.SysFont('couriernew', font_size, True)
		renderd_text = font.render(text, 1, (4, 245, 4))
		win.blit(renderd_text, (self.ratio * width, self.ratio * height))


class alien_1(object):
		def __init__(self,x,y, width, height, end, ratio):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 1 * ratio
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 0
			self.visible = True
			self.bullets = []
			self.shootloop = 0
			self.loopbreak = False
		
		def set_loopbreak(self, val):
			self.loopbreak = val

		def draw(self, win, image):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(image, (self.x,self.y))
				else:
					win.blit(image, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x - 2, self.y - 1, 35, 27)
				#pygame.draw.rect(win, (255,0,0), self.hitbox,2)

		def move(self):
			if not self.loopbreak and self.vel > 0:
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
				win.blit(image, (self.x,self.y))
				sound.play()
				print('hit')

class projectile(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class player(object):
		def __init__(self,x,y,width,height):
			self.x = x
			self.y = y
			self.height = height
			self.width = width
			self.vel = 5
			self.left = False
			self.right = False
			self.hitbox = (self.x, self.y, 35, 45)
			self.visible = True

		def draw(self, win, images):
			if self.left:
				win.blit(images[2], (self.x,self.y))
			elif self.right:
				win.blit(images[1], (self.x,self.y))
			else:
				win.blit(images[0], (self.x,self.y))

			self.hitbox = (self.x, self.y, 35, 45)
			#pygame.draw.rect(win, (255,0,0), self.hitbox,2)