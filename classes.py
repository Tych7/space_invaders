import pygame
import os
import sys

class alien_1(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 1
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 0
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walk, (self.x,self.y))
				else:
					win.blit(walk, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x - 2, self.y - 1, 35, 27)
				#pygame.draw.rect(win, (255,0,0), self.hitbox,2)

		def move(self):
			if not loopbreak and self.vel > 0:
				if self.x + self.vel < self.path[1]:
					self.x += self.vel
				else:
					self.vel = self.vel * -1
			else:
				if self.x - self.vel > self.path[0]:
					self.x += self.vel
				else:
					self.vel = self.vel * -1


		def hit(self):
			if self.health > 0:
				self.health -= 1
			else:
				self.visible = False
				win.blit(die, (self.x,self.y))
				if not mute:
					alienkill.play()
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

		def draw(self, win):
			if self.left:
				win.blit(shipleft, (self.x,self.y))
			elif self.right:
				win.blit(shipright, (self.x,self.y))
			else:
				win.blit(ship, (self.x,self.y))

			self.hitbox = (self.x, self.y, 35, 45)
			#pygame.draw.rect(win, (255,0,0), self.hitbox,2)