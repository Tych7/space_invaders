import pygame
import sys
import os
pygame.init()




def restart():
	win = pygame.display.set_mode((1600,900))
	pygame.display.set_caption("Space Invaders")

	ship = pygame.image.load('ship.png').convert()
	shipleft = pygame.image.load('shipleft.png').convert()
	shipright = pygame.image.load('shipright.png').convert()

	shipupgrade = pygame.image.load('shipupgrade.png').convert()
	shipupgradeleft = pygame.image.load('shipupgradeleft.png').convert()
	shipupgraderight = pygame.image.load('shipupgraderight.png').convert()

	bg = pygame.image.load('bgA.jpg').convert()
	walk = pygame.image.load('alien.png').convert()
	walkA = pygame.image.load('alienA.png').convert()
	walkB = pygame.image.load('shooterA.png').convert()
	walkC = pygame.image.load('alienB.png').convert()
	tank = pygame.image.load('tank.png').convert()
	gameover = pygame.image.load('gameover.jpg').convert()
	winner = pygame.image.load('win.jpg').convert()
	rstart = pygame.image.load('restart.jpg').convert()
	quit = pygame.image.load('quit.jpg').convert()
	menu = pygame.image.load('menu.jpg').convert()
	die =  pygame.image.load('explo.png').convert()
	upgrade = pygame.image.load('upgrade.png').convert()
	lvl =  pygame.image.load('lvl9.png').convert()

	lazer = pygame.mixer.Sound('laser.wav')
	oversound = pygame.mixer.Sound('gameover.wav')
	alienkill = pygame.mixer.Sound('invaderkilled.wav')


	DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

	Score = 0
	pause = False
	Movetrigger = 0

	MoveDown = False
	MoveDownCounter = 0
	MoveDownA = False
	MoveDownCounterA = 0
	upgradecounter = 0
	mute = False
	mutelock = False
	MoveDownlock = False

	speedup = False
	loopbreak = False
	loopbreak2 = False

	overy = 350
	overx = 650

	winny = 405
	winnx = 675

	alienyA = 150
	alienyB = 200
	alienyC = 250
	alienyD = 100

	deathsoundcounter = 0

	apear = False
	apearcounter = 0


	class player(object):
		def __init__(self,x,y,width,height):
			self.x = x
			self.y = y
			self.height = height
			self.width = width
			self.vel = 5
			self.left = False
			self.right = False
			self.hitbox = (self.x + 5, self.y, 35, 45)
			self.visible = True
			self.upgrade = False


		def draw(self, win):
			if not self.upgrade:
				if self.left:
					win.blit(shipleft, (self.x,self.y))
				elif self.right:
					win.blit(shipright, (self.x,self.y))
				else:
					win.blit(ship, (self.x,self.y))

			if self.upgrade:
				if self.left:
					win.blit(shipupgradeleft, (self.x,self.y))
				elif self.right:
					win.blit(shipupgraderight, (self.x,self.y))
				else:
					win.blit(shipupgrade, (self.x,self.y))

			self.hitbox = (self.x, self.y, 35, 45)
			#pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	class projectileA(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileB(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileC(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileD(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileE(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileF(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileG(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileH(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileI(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			if self.y < 850 and self.y > 50:
				pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

	class projectileJ(object):
		def __init__(self,x,y,radius,color):
			self.x = x
			self.y = y
			self.radius = radius
			self.color = color
			self.vel = 8

		def draw(self,win):
			if self.y < 850 and self.y > 50:
				pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


	class enemyA(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 0
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walkA, (self.x,self.y))
				else:
					win.blit(walkA, (self.x,self.y))

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

	class enemyB(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 2
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walk, (self.x,self.y))
				else:
					win.blit(walk, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (13 * (2 - self.health)), 5))
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

	class enemyC(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 0
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walkA, (self.x,self.y))
				else:
					win.blit(walkA, (self.x,self.y))

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

	class enemyD(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 2
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walk, (self.x,self.y))
				else:
					win.blit(walk, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (13 * (2 - self.health)), 5))
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

	class enemyE(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 0
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walkA, (self.x,self.y))
				else:
					win.blit(walkA, (self.x,self.y))

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

	class enemyG(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 134, 40)
			self.health = 5
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(tank, (self.x,self.y))
				else:
					win.blit(tank, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0] + 45, self.hitbox[1] - 10, 50, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0] + 45, self.hitbox[1] - 10, 50 - (8.5 * (5 - self.health)), 5))
				self.hitbox = (self.x - 2, self.y - 1, 134, 40)
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

	class enemyH(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 35, 27)
			self.health = 2
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walk, (self.x,self.y))
				else:
					win.blit(walk, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (13 * (2 - self.health)), 5))
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

	class enemyI(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 134, 40)
			self.health = 5
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(tank, (self.x,self.y))
				else:
					win.blit(tank, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0] + 45, self.hitbox[1] - 10, 50, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0] + 45, self.hitbox[1] - 10, 50 - (8.5 * (5 - self.health)), 5))
				self.hitbox = (self.x - 2, self.y - 1, 134, 40)
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


		def hit(self):
			if self.health > 0:
				self.health -= 1
			else:
				self.visible = False
				win.blit(die, (self.x,self.y))
				if not mute:
					alienkill.play()
				print('hit')

	class enemyK(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 25, 25)
			self.health = 0
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walkC, (self.x,self.y))
				else:
					win.blit(walkC, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x, self.y, 25, 25)
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

	class enemyL(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 2
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walk, (self.x,self.y))
				else:
					win.blit(walk, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (13 * (2 - self.health)), 5))
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

	class enemyM(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 2
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walk, (self.x,self.y))
				else:
					win.blit(walk, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (13 * (2 - self.health)), 5))
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

	class enemyN(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 34, 27)
			self.health = 2
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walk, (self.x,self.y))
				else:
					win.blit(walk, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (13 * (2 - self.health)), 5))
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

	class enemyO(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 25, 25)
			self.health = 0
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walkC, (self.x,self.y))
				else:
					win.blit(walkC, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x, self.y, 25, 25)
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

	class enemyP(object):
		def __init__(self,x,y, width, height):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.health = 2
			self.hitbox = (self.x, self.y - 1, 40, 26)
			self.visible = True

		def draw(self, win):
			if self.visible:
				win.blit(walkB, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (13 * (2 - self.health)), 5))
				self.hitbox = (self.x, self.y - 1, 40, 26)
				#pygame.draw.rect(win, (255,0,0), self.hitbox,2)

		def hit(self):
			if self.health > 0:
				self.health -= 1
			else:
				self.visible = False
				win.blit(die, (self.x,self.y))
				if not mute:
					alienkill.play()
				print('hit')

	class enemyQ(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 25, 25)
			self.health = 0
			self.visible = True

		def draw(self, win):
			if self.visible:
				self.move()
				if self.vel > 0:
					win.blit(walkC, (self.x,self.y))
				else:
					win.blit(walkC, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x, self.y, 25, 25)
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

	class enemyR(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 25, 25)
			self.health = 0
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walkC, (self.x,self.y))
				else:
					win.blit(walkC, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x, self.y, 25, 25)
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

	class enemyS(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 25, 25)
			self.health = 0
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walkC, (self.x,self.y))
				else:
					win.blit(walkC, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x, self.y, 25, 25)
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

	class enemyT(object):
		def __init__(self,x,y, width, height, end):
			self.x = x
			self.y = y
			self.width = width
			self.height = height
			self.end = end
			self.path = [self.x , self.end]
			self.vel = 2
			self.hitbox = (self.x, self.y, 25, 25)
			self.health = 0
			self.visible = True

		def draw(self, win):
			self.move()
			if self.visible:
				if self.vel > 0:
					win.blit(walkC, (self.x,self.y))
				else:
					win.blit(walkC, (self.x,self.y))

				pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 5, 38, 5))
				pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 5, 38 - (50 * (0 - self.health)), 5))
				self.hitbox = (self.x, self.y, 25, 25)
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


#mainloop
	def rewindow():

		win.blit(bg, (0,0))
		win.blit(lvl, (200,825))
		text00 = font00.render('Score: ' + str(Score), 1, (124,252,0))
		win.blit(text00, (1175, 60))
		man.draw(win)
		alienA.draw(win)
		alienB.draw(win)
		alienC.draw(win)
		alienD.draw(win)
		alienE.draw(win)
		alienG.draw(win)
		alienH.draw(win)
		alienI.draw(win)
		alienK.draw(win)
		alienL.draw(win)
		alienM.draw(win)
		alienN.draw(win)
		alienO.draw(win)
		alienP.draw(win)
		alienQ.draw(win)
		alienR.draw(win)
		alienS.draw(win)
		alienT.draw(win)
		for bullet in bullets:
			bullet.draw(win)
		if alienP.visible:
			for bulletA in bulletsA:
				bulletA.draw(win)
			for bulletB in bulletsB:
				bulletB.draw(win)
			for bulletC in bulletsC:
				bulletC.draw(win)
		if alienQ.visible:
			for bulletD in bulletsD:
				bulletD.draw(win)
		if alienR.visible:
			for bulletE in bulletsE:
				bulletE.draw(win)
		if alienS.visible:
			for bulletF in bulletsF:
				bulletF.draw(win)
		if alienT.visible:
			for bulletG in bulletsG:
				bulletG.draw(win)
		if alienK.visible:
			for bulletH in bulletsH:
				bulletH.draw(win)
		if alienO.visible:
			for bulletI in bulletsI:
				bulletI.draw(win)






	font00 = pygame.font.SysFont('comicsans', 30, True)
	man = player(800, 750, 50, 45)
	alienA = enemyA(350, alienyA, 34, 27, 850)
	alienB = enemyB(450, alienyA, 34, 27, 950)
	alienC = enemyC(550, alienyA, 34, 27, 1050)
	alienD = enemyD(650, alienyA, 34, 27, 1150)
	alienE = enemyE(750, alienyA, 34, 27, 1250)
	alienG = enemyG(350, alienyC, 134, 58, 850)
	alienH = enemyH(550, alienyC, 34, 27, 1050)
	alienI = enemyI(650, alienyC, 34, 27, 1150)
	alienK = enemyK(350, alienyB, 34, 27, 850)
	alienL = enemyL(450, alienyB, 34, 27, 950)
	alienM = enemyM(550, alienyB, 34, 27, 1050)
	alienN = enemyN(650, alienyB, 34, 27, 1150)
	alienO = enemyO(750, alienyB, 34, 27, 1250)
	alienP = enemyP(400, 80, 34, 27)
	alienQ = enemyQ(700, alienyD, 25, 25, 1200)
	alienR = enemyR(400, alienyD, 25, 25, 900)
	alienS = enemyS(500, alienyD, 25, 25, 1000)
	alienT = enemyT(600, alienyD, 25, 25, 1100)

	shootloop = 0
	shootloopA = 0
	shootloopB = 0
	shootloopC = 0
	shootloopD = 0
	shootloopE = 0
	shootloopF = 0
	shootloopG = 0
	shootloopH = 0
	shootloopI = 0
	bullets = []
	bulletsA = []
	bulletsB = []
	bulletsC = []
	bulletsD = []
	bulletsE = []
	bulletsF = []
	bulletsG = []
	bulletsH = []
	bulletsI = []
	while True:
		pygame.time.delay(12)

		if alienA.y < 200:
			speedup = True
		if (alienA.y > 200) and speedup:
			alienA.vel = 6
			alienC.vel = 6
			alienE.vel = 6

			speedup = False

		if Movetrigger == 1:
			from random import randint
			R = (randint(1, 8))
			if R == 1:
				alienP.x = 400
			if R == 2:
				alienP.x = 500
			if R == 3:
				alienP.x = 600
			if R == 4:
				alienP.x = 700
			if R == 5:
				alienP.x = 800
			if R == 6:
				alienP.x = 900
			if R == 7:
				alienP.x = 1000
			if R == 8:
				alienP.x = 1100
			Movetrigger -= 1



		if alienB.x < 900:
			MoveDown = True
		if (alienB.x > 900) and MoveDown:
			MoveDownCounter += 1
			MoveDown = False
			Movetrigger += 1

		if alienB.x > 500:
			MoveDownlock = True
		if (alienB.x < 500) and MoveDownlock:
			Movetrigger += 1
			MoveDownlock = False

		alienB.y = alienyA + (MoveDownCounter * 50)
		alienD.y = alienyA + (MoveDownCounter * 50)


		alienG.y = alienyC + (MoveDownCounter * 50)
		alienH.y = alienyC + (MoveDownCounter * 50)
		alienI.y = alienyC + (MoveDownCounter * 50)

		alienK.y = alienyB + (MoveDownCounter * 50)
		alienL.y = alienyB + (MoveDownCounter * 50)
		alienM.y = alienyB + (MoveDownCounter * 50)
		alienN.y = alienyB + (MoveDownCounter * 50)
		alienO.y = alienyB + (MoveDownCounter * 50)


		alienQ.y = alienyD + (MoveDownCounter * 50)
		alienR.y = alienyD + (MoveDownCounter * 50)
		alienS.y = alienyD + (MoveDownCounter * 50)
		alienT.y = alienyD + (MoveDownCounter * 50)

		if alienA.x < 800:
			MoveDownA = True
		if (alienA.x > 800) and MoveDownA:
			MoveDownCounterA += 1
			MoveDownA = False
		alienA.y = alienyA + (MoveDownCounterA * 50)
		alienC.y = alienyA + (MoveDownCounterA * 50)
		alienE.y = alienyA + (MoveDownCounterA * 50)



		if shootloop > 0:
			shootloop += 1
		if shootloop > 3:
			shootloop = 0

		if shootloopA > 0:
			shootloopA += 1
		if shootloopA > 3:
			shootloopA = 0

		if shootloopB > 0:
			shootloopB += 1
		if shootloopB > 3:
			shootloopB = 0

		if shootloopC > 0:
			shootloopC += 1
		if shootloopC > 3:
			shootloopC = 0

		if shootloopD > 0:
			shootloopD += 1
		if shootloopD > 3:
			shootloopD = 0

		if shootloopE > 0:
			shootloopE += 1
		if shootloopE > 3:
			shootloopE = 0

		if shootloopF > 0:
			shootloopF += 1
		if shootloopF > 3:
			shootloopF = 0

		if shootloopG > 0:
			shootloopG += 1
		if shootloopG > 3:
			shootloopG = 0

		if shootloopH > 0:
			shootloopH += 1
		if shootloopH > 3:
			shootloopH = 0

		if shootloopI > 0:
			shootloopI += 1
		if shootloopI > 3:
			shootloopI = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)

		if alienA.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienA.hitbox[1] + alienA.hitbox[3] and bullet.y + bullet.radius > alienA.hitbox[1]:
					if bullet.x + bullet.radius > alienA.hitbox[0] and bullet.x - bullet.radius < alienA.hitbox[0] + alienA.hitbox[2]:
						alienA.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienB.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienB.hitbox[1] + alienB.hitbox[3] and bullet.y + bullet.radius > alienB.hitbox[1]:
					if bullet.x + bullet.radius > alienB.hitbox[0] and bullet.x - bullet.radius < alienB.hitbox[0] + alienB.hitbox[2]:
						alienB.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienC.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienC.hitbox[1] + alienC.hitbox[3] and bullet.y + bullet.radius > alienC.hitbox[1]:
					if bullet.x + bullet.radius > alienC.hitbox[0] and bullet.x - bullet.radius < alienC.hitbox[0] + alienC.hitbox[2]:
						alienC.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienD.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienD.hitbox[1] + alienD.hitbox[3] and bullet.y + bullet.radius > alienD.hitbox[1]:
					if bullet.x + bullet.radius > alienD.hitbox[0] and bullet.x - bullet.radius < alienD.hitbox[0] + alienD.hitbox[2]:
						alienD.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienE.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienE.hitbox[1] + alienE.hitbox[3] and bullet.y + bullet.radius > alienE.hitbox[1]:
					if bullet.x + bullet.radius > alienE.hitbox[0] and bullet.x - bullet.radius < alienE.hitbox[0] + alienE.hitbox[2]:
						alienE.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienG.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienG.hitbox[1] + alienG.hitbox[3] and bullet.y + bullet.radius > alienG.hitbox[1]:
					if bullet.x + bullet.radius > alienG.hitbox[0] and bullet.x - bullet.radius < alienG.hitbox[0] + alienG.hitbox[2]:
						alienG.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienH.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienH.hitbox[1] + alienH.hitbox[3] and bullet.y + bullet.radius > alienH.hitbox[1]:
					if bullet.x + bullet.radius > alienH.hitbox[0] and bullet.x - bullet.radius < alienH.hitbox[0] + alienH.hitbox[2]:
						alienH.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienI.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienI.hitbox[1] + alienI.hitbox[3] and bullet.y + bullet.radius > alienI.hitbox[1]:
					if bullet.x + bullet.radius > alienI.hitbox[0] and bullet.x - bullet.radius < alienI.hitbox[0] + alienI.hitbox[2]:
						alienI.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienK.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienK.hitbox[1] + alienK.hitbox[3] and bullet.y + bullet.radius > alienK.hitbox[1]:
					if bullet.x + bullet.radius > alienK.hitbox[0] and bullet.x - bullet.radius < alienK.hitbox[0] + alienK.hitbox[2]:
						alienK.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienL.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienL.hitbox[1] + alienL.hitbox[3] and bullet.y + bullet.radius > alienL.hitbox[1]:
					if bullet.x + bullet.radius > alienL.hitbox[0] and bullet.x - bullet.radius < alienL.hitbox[0] + alienL.hitbox[2]:
						alienL.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienM.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienM.hitbox[1] + alienM.hitbox[3] and bullet.y + bullet.radius > alienM.hitbox[1]:
					if bullet.x + bullet.radius > alienM.hitbox[0] and bullet.x - bullet.radius < alienM.hitbox[0] + alienM.hitbox[2]:
						alienM.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienN.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienN.hitbox[1] + alienN.hitbox[3] and bullet.y + bullet.radius > alienN.hitbox[1]:
					if bullet.x + bullet.radius > alienN.hitbox[0] and bullet.x - bullet.radius < alienN.hitbox[0] + alienN.hitbox[2]:
						alienN.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienO.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienO.hitbox[1] + alienO.hitbox[3] and bullet.y + bullet.radius > alienO.hitbox[1]:
					if bullet.x + bullet.radius > alienO.hitbox[0] and bullet.x - bullet.radius < alienO.hitbox[0] + alienO.hitbox[2]:
						alienO.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienP.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienP.hitbox[1] + alienP.hitbox[3] and bullet.y + bullet.radius > alienP.hitbox[1]:
					if bullet.x + bullet.radius > alienP.hitbox[0] and bullet.x - bullet.radius < alienP.hitbox[0] + alienP.hitbox[2]:
						alienP.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienQ.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienQ.hitbox[1] + alienQ.hitbox[3] and bullet.y + bullet.radius > alienQ.hitbox[1]:
					if bullet.x + bullet.radius > alienQ.hitbox[0] and bullet.x - bullet.radius < alienQ.hitbox[0] + alienQ.hitbox[2]:
						alienQ.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienR.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienR.hitbox[1] + alienR.hitbox[3] and bullet.y + bullet.radius > alienR.hitbox[1]:
					if bullet.x + bullet.radius > alienR.hitbox[0] and bullet.x - bullet.radius < alienR.hitbox[0] + alienR.hitbox[2]:
						alienR.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienS.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienS.hitbox[1] + alienS.hitbox[3] and bullet.y + bullet.radius > alienS.hitbox[1]:
					if bullet.x + bullet.radius > alienS.hitbox[0] and bullet.x - bullet.radius < alienS.hitbox[0] + alienS.hitbox[2]:
						alienS.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))

		if alienT.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienT.hitbox[1] + alienT.hitbox[3] and bullet.y + bullet.radius > alienT.hitbox[1]:
					if bullet.x + bullet.radius > alienT.hitbox[0] and bullet.x - bullet.radius < alienT.hitbox[0] + alienT.hitbox[2]:
						alienT.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))


		if man.visible:
			if alienP.visible:
				for bulletA in bulletsA:
					if bulletA.y - bulletA.radius < man.hitbox[1] + man.hitbox[3] and bulletA.y + bulletA.radius > man.hitbox[1]:
						if bulletA.x + bulletA.radius > man.hitbox[0] and bulletA.x - bulletA.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsA.pop(bulletsA.index(bulletA))

		if man.visible:
			if alienP.visible:
				for bulletB in bulletsB:
					if bulletB.y - bulletB.radius < man.hitbox[1] + man.hitbox[3] and bulletB.y + bulletB.radius > man.hitbox[1]:
						if bulletB.x + bulletB.radius > man.hitbox[0] and bulletB.x - bulletB.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsB.pop(bulletsB.index(bulletB))


		if man.visible:
			if alienP.visible:
				for bulletC in bulletsC:
					if bulletC.y - bulletC.radius < man.hitbox[1] + man.hitbox[3] and bulletC.y + bulletC.radius > man.hitbox[1]:
						if bulletC.x + bulletC.radius > man.hitbox[0] and bulletC.x - bulletC.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsC.pop(bulletsC.index(bulletC))

		if man.visible:
			if alienQ.visible:
				for bulletD in bulletsD:
					if bulletD.y - bulletD.radius < man.hitbox[1] + man.hitbox[3] and bulletD.y + bulletD.radius > man.hitbox[1]:
						if bulletD.x + bulletD.radius > man.hitbox[0] and bulletD.x - bulletD.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsD.pop(bulletsD.index(bulletD))

		if man.visible:
			if alienR.visible:
				for bulletE in bulletsE:
					if bulletE.y - bulletE.radius < man.hitbox[1] + man.hitbox[3] and bulletE.y + bulletE.radius > man.hitbox[1]:
						if bulletE.x + bulletE.radius > man.hitbox[0] and bulletE.x - bulletE.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsE.pop(bulletsE.index(bulletE))

		if man.visible:
			if alienS.visible:
				for bulletF in bulletsF:
					if bulletF.y - bulletF.radius < man.hitbox[1] + man.hitbox[3] and bulletF.y + bulletF.radius > man.hitbox[1]:
						if bulletF.x + bulletF.radius > man.hitbox[0] and bulletF.x - bulletF.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsF.pop(bulletsF.index(bulletF))

		if man.visible:
			if alienT.visible:
				for bulletG in bulletsG:
					if bulletG.y - bulletG.radius < man.hitbox[1] + man.hitbox[3] and bulletG.y + bulletG.radius > man.hitbox[1]:
						if bulletG.x + bulletG.radius > man.hitbox[0] and bulletG.x - bulletG.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsG.pop(bulletsG.index(bulletG))

		if man.visible:
			if alienK.visible:
				for bulletH in bulletsH:
					if bulletH.y - bulletH.radius < man.hitbox[1] + man.hitbox[3] and bulletH.y + bulletH.radius > man.hitbox[1]:
						if bulletH.x + bulletH.radius > man.hitbox[0] and bulletH.x - bulletH.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsH.pop(bulletsH.index(bulletH))

		if man.visible:
			if alienO.visible:
				for bulletI in bulletsI:
					if bulletI.y - bulletI.radius < man.hitbox[1] + man.hitbox[3] and bulletI.y + bulletI.radius > man.hitbox[1]:
						if bulletI.x + bulletI.radius > man.hitbox[0] and bulletI.x - bulletI.radius < man.hitbox[0] + man.hitbox[2]:
							win.blit(gameover, (overx, overy))
							loopbreak = True
							bulletsI.pop(bulletsI.index(bulletI))






		if not loopbreak:
			if not pause:
				for bullet in bullets:
					if bullet.y < 850 and bullet.y > 50:
						bullet.y -= bullet.vel
					else:
						bullets.pop(bullets.index(bullet))



		keys = pygame.key.get_pressed()


		if not loopbreak:
			if not pause:
				if keys[pygame.K_SPACE] and shootloop == 0:
					if alienP.visible:
						if len(bullets) < 1:
							bullets.append(projectileA(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,255,255)))
							if not mute:
								lazer.play()
					if not alienP.visible:
						if shootloop == 0:
							if len(bullets) < 2:
								bullets.append(projectileA(round(man.x + man.width //2 + 20), round(man.y + man.height//2), 6, (0,255,255)))
								bullets.append(projectileA(round(man.x + man.width //2 - 20), round(man.y + man.height//2), 6, (0,255,255)))
								if not mute:
									lazer.play()



		if alienP.visible:
			if not loopbreak:
				if not pause:
					for bulletA in bulletsA:
						if bulletA.y < 850 and bulletA.y > 50:
								bulletA.y += bulletA.vel
						else:
							bulletsA.pop(bulletsA.index(bulletA))

		if alienP.visible:
			if not loopbreak:
				if not pause:
					for bulletB in bulletsB:
						if bulletB.y < 850 and bulletB.y > 50:
							if bulletB.x < 1300 and bulletB.x > 300:
								bulletB.y += bulletB.vel
								bulletB.x += 3
							else:
								bulletsB.pop(bulletsB.index(bulletB))
						else:
							bulletsB.pop(bulletsB.index(bulletB))

		if alienP.visible:
			if not loopbreak:
				if not pause:
					for bulletC in bulletsC:
						if bulletC.y < 850 and bulletC.y > 50:
							if bulletC.x < 1300 and bulletC.x > 300:
								bulletC.y += bulletC.vel
								bulletC.x -= 3
							else:
								bulletsC.pop(bulletsC.index(bulletC))
						else:
							bulletsC.pop(bulletsC.index(bulletC))



				keys = pygame.key.get_pressed()

				if shootloopA == 0:
					if len(bulletsA) < 1:
						bulletsA.append(projectileB(round(alienP.x + alienP.width //2), round(alienP.y + alienP.height//2), 6, (255,0,0)))
						bulletsB.append(projectileC(round(alienP.x + alienP.width //2 - 15), round(alienP.y + alienP.height//2), 6, (255,0,0)))
						bulletsC.append(projectileD(round(alienP.x + alienP.width //2 + 15), round(alienP.y + alienP.height//2), 6, (255,0,0)))
						if not mute:
							lazer.play()


		if alienQ.visible:
			if not loopbreak:
				if not pause:
					for bulletD in bulletsD:
						if bulletD.y < 850 and bulletD.y > 50:
								bulletD.y += bulletD.vel

						else:
							bulletsD.pop(bulletsD.index(bulletD))

				if shootloopD == 0:
					if len(bulletsD) < 1:
						bulletsD.append(projectileE(round(alienQ.x + alienQ.width //2), round(alienQ.y + alienQ.height//2), 6, (238,130,238)))
						if not mute:
							lazer.play()


		if alienR.visible:
			if not loopbreak:
				if not pause:
					for bulletE in bulletsE:
						if bulletE.y < 850 and bulletE.y > 50:
								bulletE.y += bulletE.vel

						else:
							bulletsE.pop(bulletsE.index(bulletE))

				if shootloopE == 0:
					if len(bulletsE) < 1:
						bulletsE.append(projectileF(round(alienR.x + alienR.width //2), round(alienR.y + alienR.height//2), 6, (238,130,238)))
						if not mute:
							lazer.play()

		if alienS.visible:
			if not loopbreak:
				if not pause:
					for bulletF in bulletsF:
						if bulletF.y < 850 and bulletF.y > 50:
								bulletF.y += bulletF.vel

						else:
							bulletsF.pop(bulletsF.index(bulletF))

				if shootloopF == 0:
					if len(bulletsF) < 1:
						bulletsF.append(projectileG(round(alienS.x + alienS.width //2), round(alienS.y + alienS.height//2), 6, (238,130,238)))
						if not mute:
							lazer.play()

		if alienT.visible:
			if not loopbreak:
				if not pause:
					for bulletG in bulletsG:
						if bulletG.y < 850 and bulletG.y > 50:
								bulletG.y += bulletG.vel

						else:
							bulletsG.pop(bulletsG.index(bulletG))

				if shootloopG == 0:
					if len(bulletsG) < 1:
						bulletsG.append(projectileH(round(alienT.x + alienT.width //2), round(alienT.y + alienT.height//2), 6, (238,130,238)))
						if not mute:
							lazer.play()

		if alienK.visible:
			if not loopbreak:
				if not pause:
					for bulletH in bulletsH:
						if bulletH.y < 950 and bulletH.y > 50:
								bulletH.y += bulletH.vel

						else:
							bulletsH.pop(bulletsH.index(bulletH))

				if shootloopH == 0:
					if len(bulletsH) < 1:
						bulletsH.append(projectileI(round(alienK.x + alienK.width //2), round(alienK.y + alienK.height//2), 6, (238,130,238)))


		if alienO.visible:
			if not loopbreak:
				if not pause:
					for bulletI in bulletsI:
						if bulletI.y < 950 and bulletI.y > 50:
								bulletI.y += bulletI.vel

						else:
							bulletsI.pop(bulletsI.index(bulletI))

				if shootloopI == 0:
					if len(bulletsI) < 1:
						bulletsI.append(projectileJ(round(alienO.x + alienO.width //2), round(alienO.y + alienO.height//2), 6, (238,130,238)))
						if not mute:
							lazer.play()


		if keys[pygame.K_KP0]:
			if not mute:
				if not mutelock:
					mute = True
					mutelock = True
			if mute:
				if not mutelock:
					mute = False
					mutelock = True
		if not keys[pygame.K_KP0]:
			mutelock = False

		if not loopbreak:
			if keys[pygame.K_LEFT] and man.x > 300:
				man.x -= man.vel
				man.left = True
				man.right = False
			elif keys[pygame.K_RIGHT] and man.x < 1300 - man.width:
				man.x += man.vel
				man.left = False
				man.right = True
			else:
				man.left = False
				man.right = False

		if alienA.visible and alienA.y > 740:
			loopbreak = True
		elif alienB.visible and alienB.y > 740:
			loopbreak = True
		elif alienC.visible and alienC.y > 740:
			loopbreak = True
		elif alienD.visible and alienD.y > 740:
			loopbreak = True
		elif alienE.visible and alienE.y > 740:
			loopbreak = True
		elif alienG.visible and alienG.y > 740:
			loopbreak = True
		elif alienH.visible and alienH.y > 740:
			loopbreak = True
		elif alienI.visible and alienI.y > 740:
			loopbreak = True
		elif alienK.visible and alienK.y > 740:
			loopbreak = True
		elif alienL.visible and alienL.y > 740:
			loopbreak = True
		elif alienM.visible and alienM.y > 740:
			loopbreak = True
		elif alienN.visible and alienN.y > 740:
			loopbreak = True
		elif alienO.visible and alienO.y > 740:
			loopbreak = True
		elif alienQ.visible and alienQ.y > 740:
			loopbreak = True
		elif alienR.visible and alienR.y > 740:
			loopbreak = True
		elif alienS.visible and alienS.y > 740:
			loopbreak = True
		elif alienT.visible and alienT.y > 740:
			loopbreak = True

		if not alienA.visible and not alienB.visible and not alienC.visible and not alienD.visible and not alienE.visible and not alienG.visible and not alienH.visible and not alienI.visible and not alienK.visible and not alienL.visible and not alienM.visible and not alienN.visible and not alienO.visible and not alienP.visible and not alienQ.visible and not alienR.visible and not alienS.visible and not alienT.visible:
			loopbreak2 = True
			loopbreak = True

		if not alienP.visible:
			man.upgrade = True

		if not alienP.visible:
			upgradecounter += 1
			if not upgradecounter > 50:
				win.blit(upgrade, (350, 100))

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			pause = True

		if pause:
			alienA.vel = 0
			alienB.vel = 0
			alienC.vel = 0
			alienD.vel = 0
			alienE.vel = 0

			alienG.vel = 0
			alienH.vel = 0
			alienI.vel = 0

			alienK.vel = 0
			alienL.vel = 0
			alienM.vel = 0
			alienN.vel = 0
			alienO.vel = 0

			alienR.vel = 0
			alienQ.vel = 0
			alienS.vel = 0
			alienT.vel = 0
			win.blit(rstart, (350, 750))
			win.blit(quit, (950, 750))
			win.blit(menu, (350, 800))
			if keys[pygame.K_q]:
				os.system('TASKKILL /F /IM python.exe')
			if keys[pygame.K_r]:
				restart()
			if keys[pygame.K_m]:
				os.startfile('main_menu.py')
				pygame.quit()

		if loopbreak:
			alienA.vel = 0
			alienB.vel = 0
			alienC.vel = 0
			alienD.vel = 0
			alienE.vel = 0

			alienG.vel = 0
			alienH.vel = 0
			alienI.vel = 0

			alienK.vel = 0
			alienL.vel = 0
			alienM.vel = 0
			alienN.vel = 0
			alienO.vel = 0
			alienR.vel = 0
			alienQ.vel = 0
			alienS.vel = 0
			alienT.vel = 0
			if not loopbreak2:
				win.blit(gameover, (overx, overy))
				deathsoundcounter += 1
				if deathsoundcounter == 1:
					if not mute:
						oversound.play()
			if loopbreak2:
				win.blit(winner, (winnx, winny))
			win.blit(rstart, (350, 750))
			win.blit(quit, (950, 750))
			win.blit(menu, (350, 800))
			if keys[pygame.K_q]:
				os.system('TASKKILL /F /IM python.exe')
			if keys[pygame.K_r]:
				restart()
			if keys[pygame.K_m]:
				os.startfile('main_menu.py')
				pygame.quit()


		pygame.display.update()
		rewindow()

restart()
