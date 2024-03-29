import pygame
import sys
import os
pygame.init()




def restart():
	win = pygame.display.set_mode((1000,800))
	pygame.display.set_caption("Space Invaders")

	ship = pygame.image.load('ship.png')
	shipleft = pygame.image.load('shipleft.png')
	shipright = pygame.image.load('shipright.png')
	bg = pygame.image.load('bg.jpg')
	walk = pygame.image.load('alien.png')
	walkA = pygame.image.load('alienA.png')
	walkB = pygame.image.load('shooter.png')
	walkC = pygame.image.load('alienB.png')
	gameover = pygame.image.load('gameover.jpg')
	winner = pygame.image.load('win.jpg')
	rstart = pygame.image.load('restart.jpg')
	quit = pygame.image.load('quit.jpg')
	menu = pygame.image.load('menu.jpg')
	die =  pygame.image.load('explo.png')
	upgrade = pygame.image.load('upgrade.png')

	lazer = pygame.mixer.Sound('laser.wav')
	oversound = pygame.mixer.Sound('gameover.wav')
	alienkill = pygame.mixer.Sound('invaderkilled.wav')

	joysticks = []
	clock = pygame.time.Clock()

	for i in range(0, pygame.joystick.get_count()):
	    # create an Joystick object in our list
	    joysticks.append(pygame.joystick.Joystick(i))
	    # initialize them all (-1 means loop forever)
	    joysticks[-1].init()
	    # print a statement telling what the name of the controller is
	    print ("Detected joystick '"),joysticks[-1].get_name(),"'"

	j = pygame.joystick.Joystick(0) # create a joystick instance
	t = pygame.joystick.Joystick(0) # create a joystick instance


	DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

	Score = 0
	pause = False
	Movetrigger = 0

	MoveDown = False
	MoveDownCounter = 0
	MoveDownA = False
	MoveDownCounterA = 0

	speedup = False
	loopbreak = False
	loopbreak2 = False

	overy = 300
	overx = 350

	winny = 355
	winnx = 375

	alienyA = 100
	alienyB = 150
	alienyC = 200
	alienyD = 50

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


		def draw(self, win):
			if self.left:
				win.blit(shipleft, (self.x,self.y))
			elif self.right:
				win.blit(shipright, (self.x,self.y))
			else:
				win.blit(ship, (self.x,self.y))

			self.hitbox = (self.x + 5, self.y, 35, 45)
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
				alienkill.play()
				print('hit')

	class enemyF(object):
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
				alienkill.play()
				print('hit')

	class enemyJ(object):
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
				alienkill.play()
				print('hit')


#mainloop
	def rewindow():

		win.blit(bg, (0,0))
		text00 = font00.render('Score: ' + str(Score), 1, (124,252,0))
		win.blit(text00, (873, 10))
		man.draw(win)
		alienA.draw(win)
		alienB.draw(win)
		alienC.draw(win)
		alienD.draw(win)
		alienE.draw(win)
		alienF.draw(win)
		alienG.draw(win)
		alienH.draw(win)
		alienI.draw(win)
		alienJ.draw(win)
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
		if not alienP.visible:
			for bulletH in bulletsH:
				bulletH.draw(win)







	font00 = pygame.font.SysFont('comicsans', 30, True)
	man = player(500, 700, 35, 45)
	alienA = enemyA(50, alienyA, 34, 27, 550)
	alienB = enemyB(150, alienyA, 34, 27, 650)
	alienC = enemyC(250, alienyA, 34, 27, 750)
	alienD = enemyD(350, alienyA, 34, 27, 850)
	alienE = enemyE(450, alienyA, 34, 27, 950)
	alienF = enemyF(50, alienyC, 34, 27, 550)
	alienG = enemyG(150, alienyC, 34, 27, 650)
	alienH = enemyH(250, alienyC, 34, 27, 750)
	alienI = enemyI(350, alienyC, 34, 27, 850)
	alienJ = enemyJ(450, alienyC, 34, 27, 950)
	alienK = enemyK(50, alienyB, 34, 27, 550)
	alienL = enemyL(150, alienyB, 34, 27, 650)
	alienM = enemyM(250, alienyB, 34, 27, 750)
	alienN = enemyN(350, alienyB, 34, 27, 850)
	alienO = enemyO(450, alienyB, 34, 27, 950)
	alienQ = enemyQ(100, alienyD, 25, 25, 600)
	alienR = enemyR(200, alienyD, 25, 25, 700)
	alienS = enemyS(300, alienyD, 25, 25, 800)
	alienT = enemyT(400, alienyD, 25, 25, 900)
	alienP = enemyP(100, 30, 34, 27)
	shootloop = 0
	shootloopA = 0
	shootloopB = 0
	shootloopC = 0
	shootloopD = 0
	shootloopE = 0
	shootloopF = 0
	shootloopG = 0
	shootloopH = 0
	bullets = []
	bulletsA = []
	bulletsB = []
	bulletsC = []
	bulletsD = []
	bulletsE = []
	bulletsF = []
	bulletsG = []
	bulletsH = []
	while True:
		clock.tick(60)

		if alienB.y < 150:
			speedup = True
		if (alienB.y > 150) and speedup:
			alienL.vel = 4
			alienM.vel = 4
			alienN.vel = 4

			speedup = False

		if Movetrigger == 1:
			if alienP.visible:
				from random import randint
				R = (randint(1, 8))
				if R == 1:
					alienP.x = 100
				if R == 2:
					alienP.x = 200
				if R == 3:
					alienP.x = 300
				if R == 4:
					alienP.x = 400
				if R == 5:
					alienP.x = 600
				if R == 6:
					alienP.x = 700
				if R == 7:
					alienP.x = 800
				if R == 8:
					alienP.x = 900
				Movetrigger -= 1



		if alienB.x < 600:
			MoveDown = True
		if (alienB.x > 600) and MoveDown:
			MoveDownCounter += 1
			MoveDown = False
			Movetrigger += 1
		alienA.y = alienyA + (MoveDownCounter * 50)
		alienB.y = alienyA + (MoveDownCounter * 50)
		alienC.y = alienyA + (MoveDownCounter * 50)
		alienD.y = alienyA + (MoveDownCounter * 50)
		alienE.y = alienyA + (MoveDownCounter * 50)

		alienF.y = alienyC + (MoveDownCounter * 50)
		alienG.y = alienyC + (MoveDownCounter * 50)
		alienH.y = alienyC + (MoveDownCounter * 50)
		alienI.y = alienyC + (MoveDownCounter * 50)
		alienJ.y = alienyC + (MoveDownCounter * 50)

		alienK.y = alienyB + (MoveDownCounter * 50)
		alienO.y = alienyB + (MoveDownCounter * 50)

		alienQ.y = alienyD + (MoveDownCounter * 50)
		alienR.y = alienyD + (MoveDownCounter * 50)
		alienS.y = alienyD + (MoveDownCounter * 50)
		alienT.y = alienyD + (MoveDownCounter * 50)

		if alienL.x < 600:
			MoveDownA = True
		if (alienL.x > 600) and MoveDownA:
			MoveDownCounterA += 1
			MoveDownA = False
		alienL.y = alienyB + (MoveDownCounterA * 50)
		alienM.y = alienyB + (MoveDownCounterA * 50)
		alienN.y = alienyB + (MoveDownCounterA * 50)


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

		if alienF.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienF.hitbox[1] + alienF.hitbox[3] and bullet.y + bullet.radius > alienF.hitbox[1]:
					if bullet.x + bullet.radius > alienF.hitbox[0] and bullet.x - bullet.radius < alienF.hitbox[0] + alienF.hitbox[2]:
						alienF.hit()
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

		if alienJ.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienJ.hitbox[1] + alienJ.hitbox[3] and bullet.y + bullet.radius > alienJ.hitbox[1]:
					if bullet.x + bullet.radius > alienJ.hitbox[0] and bullet.x - bullet.radius < alienJ.hitbox[0] + alienJ.hitbox[2]:
						alienJ.hit()
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





		if alienA.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienA.hitbox[1] + alienA.hitbox[3] and bulletH.y + bulletH.radius > alienA.hitbox[1]:
					if bulletH.x + bulletH.radius > alienA.hitbox[0] and bulletH.x - bulletH.radius < alienA.hitbox[0] + alienA.hitbox[2]:
						alienA.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienB.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienB.hitbox[1] + alienB.hitbox[3] and bulletH.y + bulletH.radius > alienB.hitbox[1]:
					if bullet.x + bulletH.radius > alienB.hitbox[0] and bullet.x - bulletH.radius < alienB.hitbox[0] + alienB.hitbox[2]:
						alienB.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienC.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienC.hitbox[1] + alienC.hitbox[3] and bulletH.y + bulletH.radius > alienC.hitbox[1]:
					if bulletH.x + bulletH.radius > alienC.hitbox[0] and bulletH.x - bulletH.radius < alienC.hitbox[0] + alienC.hitbox[2]:
						alienC.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienD.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienD.hitbox[1] + alienD.hitbox[3] and bulletH.y + bulletH.radius > alienD.hitbox[1]:
					if bulletH.x + bulletH.radius > alienD.hitbox[0] and bulletH.x - bulletH.radius < alienD.hitbox[0] + alienD.hitbox[2]:
						alienD.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienE.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienE.hitbox[1] + alienE.hitbox[3] and bulletH.y + bulletH.radius > alienE.hitbox[1]:
					if bulletH.x + bulletH.radius > alienE.hitbox[0] and bulletH.x - bulletH.radius < alienE.hitbox[0] + alienE.hitbox[2]:
						alienE.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienF.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienF.hitbox[1] + alienF.hitbox[3] and bulletH.y + bulletH.radius > alienF.hitbox[1]:
					if bulletH.x + bulletH.radius > alienF.hitbox[0] and bulletH.x - bulletH.radius < alienF.hitbox[0] + alienF.hitbox[2]:
						alienF.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienG.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienG.hitbox[1] + alienG.hitbox[3] and bulletH.y + bulletH.radius > alienG.hitbox[1]:
					if bulletH.x + bulletH.radius > alienG.hitbox[0] and bulletH.x - bulletH.radius < alienG.hitbox[0] + alienG.hitbox[2]:
						alienG.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienH.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienH.hitbox[1] + alienH.hitbox[3] and bulletH.y + bulletH.radius > alienH.hitbox[1]:
					if bulletH.x + bulletH.radius > alienH.hitbox[0] and bulletH.x - bulletH.radius < alienH.hitbox[0] + alienH.hitbox[2]:
						alienH.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienI.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienI.hitbox[1] + alienI.hitbox[3] and bulletH.y + bulletH.radius > alienI.hitbox[1]:
					if bulletH.x + bulletH.radius > alienI.hitbox[0] and bullet.x - bulletH.radius < alienI.hitbox[0] + alienI.hitbox[2]:
						alienI.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienJ.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienJ.hitbox[1] + alienJ.hitbox[3] and bulletH.y + bullet.radius > alienJ.hitbox[1]:
					if bulletH.x + bulletH.radius > alienJ.hitbox[0] and bulletH.x - bulletH.radius < alienJ.hitbox[0] + alienJ.hitbox[2]:
						alienJ.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienK.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienK.hitbox[1] + alienK.hitbox[3] and bulletH.y + bulletH.radius > alienK.hitbox[1]:
					if bulletH.x + bulletH.radius > alienK.hitbox[0] and bulletH.x - bulletH.radius < alienK.hitbox[0] + alienK.hitbox[2]:
						alienK.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienL.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienL.hitbox[1] + alienL.hitbox[3] and bulletH.y + bulletH.radius > alienL.hitbox[1]:
					if bulletH.x + bulletH.radius > alienL.hitbox[0] and bulletH.x - bulletH.radius < alienL.hitbox[0] + alienL.hitbox[2]:
						alienL.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienM.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienM.hitbox[1] + alienM.hitbox[3] and bulletH.y + bulletH.radius > alienM.hitbox[1]:
					if bulletH.x + bulletH.radius > alienM.hitbox[0] and bulletH.x - bulletH.radius < alienM.hitbox[0] + alienM.hitbox[2]:
						alienM.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienN.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienN.hitbox[1] + alienN.hitbox[3] and bulletH.y + bulletH.radius > alienN.hitbox[1]:
					if bulletH.x + bulletH.radius > alienN.hitbox[0] and bulletH.x - bulletH.radius < alienN.hitbox[0] + alienN.hitbox[2]:
						alienN.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienO.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienO.hitbox[1] + alienO.hitbox[3] and bulletH.y + bulletH.radius > alienO.hitbox[1]:
					if bulletH.x + bulletH.radius > alienO.hitbox[0] and bulletH.x - bulletH.radius < alienO.hitbox[0] + alienO.hitbox[2]:
						alienO.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienP.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienP.hitbox[1] + alienP.hitbox[3] and bulletH.y + bulletH.radius > alienP.hitbox[1]:
					if bulletH.x + bulletH.radius > alienP.hitbox[0] and bulletH.x - bulletH.radius < alienP.hitbox[0] + alienP.hitbox[2]:
						alienP.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienQ.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienQ.hitbox[1] + alienQ.hitbox[3] and bulletH.y + bulletH.radius > alienQ.hitbox[1]:
					if bulletH.x + bulletH.radius > alienQ.hitbox[0] and bulletH.x - bulletH.radius < alienQ.hitbox[0] + alienQ.hitbox[2]:
						alienQ.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienR.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienR.hitbox[1] + alienR.hitbox[3] and bulletH.y + bulletH.radius > alienR.hitbox[1]:
					if bulletH.x + bulletH.radius > alienR.hitbox[0] and bulletH.x - bulletH.radius < alienR.hitbox[0] + alienR.hitbox[2]:
						alienR.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienS.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienS.hitbox[1] + alienS.hitbox[3] and bulletH.y + bulletH.radius > alienS.hitbox[1]:
					if bulletH.x + bulletH.radius > alienS.hitbox[0] and bulletH.x - bulletH.radius < alienS.hitbox[0] + alienS.hitbox[2]:
						alienS.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))

		if alienT.visible:
			for bulletH in bulletsH:
				if bulletH.y - bulletH.radius < alienT.hitbox[1] + alienT.hitbox[3] and bulletH.y + bulletH.radius > alienT.hitbox[1]:
					if bulletH.x + bulletH.radius > alienT.hitbox[0] and bulletH.x - bulletH.radius < alienT.hitbox[0] + alienT.hitbox[2]:
						alienR.hit()
						Score += 1
						bulletsH.pop(bulletsH.index(bulletH))


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




		if alienP.visible:
			if not loopbreak:
				if not pause:
					for bullet in bullets:
						if bullet.y < 800 and bullet.y > 0:
							bullet.y -= bullet.vel
						else:
							bullets.pop(bullets.index(bullet))

		if not alienP.visible:
			if not loopbreak:
				if not pause:
					for bullet in bullets:
						if bullet.y < 800 and bullet.y > 0:
							bullet.y -= bullet.vel
							bullet.x -= 1
						else:
							bullets.pop(bullets.index(bullet))

		if not alienP.visible:
			if not loopbreak:
				if not pause:
					for bulletH in bulletsH:
						if bulletH.y < 800 and bulletH.y > 0:
							bulletH.y -= bulletH.vel
							bulletH.x += 1
						else:
							bulletsH.pop(bulletsH.index(bulletH))



		keys = pygame.key.get_pressed()


		if not loopbreak:
			if not pause:
				if event.type == pygame.JOYAXISMOTION:
					if t.get_axis(2) <= -0.2 and shootloop == 0:
						if len(bullets) < 1:
							bullets.append(projectileA(round(man.x + man.width //2), round(man.y + man.height//2), 6, (255,140,0)))
							lazer.play()
							if not alienP.visible:
								if shootloopH == 0:
									if len(bulletsH) < 1:
										bulletsH.append(projectileI(round(man.x + man.width //2), round(man.y + man.height//2), 6, (255,140,0)))


		if alienP.visible:
			if not loopbreak:
				if not pause:
					for bulletA in bulletsA:
						if bulletA.y < 800 and bulletA.y > 0:
								bulletA.y += bulletA.vel
						else:
							bulletsA.pop(bulletsA.index(bulletA))

		if alienP.visible:
			if not loopbreak:
				if not pause:
					for bulletB in bulletsB:
						if bulletB.y < 800 and bulletB.y > 0:
							bulletB.y += bulletB.vel
							bulletB.x += 3
						else:
							bulletsB.pop(bulletsB.index(bulletB))

		if alienP.visible:
			if not loopbreak:
				if not pause:
					for bulletC in bulletsC:
						if bulletC.y < 800 and bulletC.y > 0:
							bulletC.y += bulletC.vel
							bulletC.x -= 3
						else:
							bulletsC.pop(bulletsC.index(bulletC))

				if shootloopA == 0:
					if len(bulletsA) < 1:
						bulletsA.append(projectileB(round(alienP.x + alienP.width //2), round(alienP.y + alienP.height//2), 6, (186,85,211)))
				if shootloopB == 0:
					if len(bulletsB) < 1:
						bulletsB.append(projectileC(round(alienP.x + alienP.width //2 - 15), round(alienP.y + alienP.height//2), 6, (186,85,211)))
				if shootloopC == 0:
					if len(bulletsC) < 1:
						bulletsC.append(projectileD(round(alienP.x + alienP.width //2 + 15), round(alienP.y + alienP.height//2), 6, (186,85,211)))
						lazer.play()


		if alienQ.visible:
			if not loopbreak:
				if not pause:
					for bulletD in bulletsD:
						if bulletD.y < 800 and bulletD.y > 0:
								bulletD.y += bulletD.vel

						else:
							bulletsD.pop(bulletsD.index(bulletD))

				if shootloopD == 0:
					if len(bulletsD) < 1:
						bulletsD.append(projectileE(round(alienQ.x + alienQ.width //2), round(alienQ.y + alienQ.height//2), 6, (238,130,238)))
						lazer.play()


		if alienR.visible:
			if not loopbreak:
				if not pause:
					for bulletE in bulletsE:
						if bulletE.y < 800 and bulletE.y > 0:
								bulletE.y += bulletE.vel

						else:
							bulletsE.pop(bulletsE.index(bulletE))

				if shootloopE == 0:
					if len(bulletsE) < 1:
						bulletsE.append(projectileF(round(alienR.x + alienR.width //2), round(alienR.y + alienR.height//2), 6, (238,130,238)))
						lazer.play()

		if alienS.visible:
			if not loopbreak:
				if not pause:
					for bulletF in bulletsF:
						if bulletF.y < 800 and bulletF.y > 0:
								bulletF.y += bulletF.vel

						else:
							bulletsF.pop(bulletsF.index(bulletF))

				if shootloopF == 0:
					if len(bulletsF) < 1:
						bulletsF.append(projectileG(round(alienS.x + alienS.width //2), round(alienS.y + alienS.height//2), 6, (238,130,238)))
						lazer.play()

		if alienT.visible:
			if not loopbreak:
				if not pause:
					for bulletG in bulletsG:
						if bulletG.y < 800 and bulletG.y > 0:
								bulletG.y += bulletG.vel

						else:
							bulletsG.pop(bulletsG.index(bulletG))

				if shootloopG == 0:
					if len(bulletsG) < 1:
						bulletsG.append(projectileH(round(alienT.x + alienT.width //2), round(alienT.y + alienT.height//2), 6, (238,130,238)))
						lazer.play()

		if not loopbreak:
			if event.type == pygame.JOYAXISMOTION and man.x > man.vel:
				if j.get_axis(0) <= -0.2:
						man.x -= man.vel
						man.left = True
						man.right = False


			if event.type == pygame.JOYAXISMOTION and man.x < 1000 - man.vel - man.width:
				if j.get_axis(0) >= 0.2:
					man.x += man.vel
					man.left = False
					man.right = True
			if event.type == pygame.JOYAXISMOTION:
				if j.get_axis(0) <= 0.2:
					if j.get_axis(0) >= -0.2:
						man.left = False
						man.right = False

		if alienA.visible and alienA.y > 690:
			loopbreak = True
		elif alienB.visible and alienB.y > 690:
			loopbreak = True
		elif alienC.visible and alienC.y > 690:
			loopbreak = True
		elif alienD.visible and alienD.y > 690:
			loopbreak = True
		elif alienE.visible and alienE.y > 690:
			loopbreak = True
		elif alienF.visible and alienF.y > 690:
			loopbreak = True
		elif alienG.visible and alienG.y > 690:
			loopbreak = True
		elif alienH.visible and alienH.y > 690:
			loopbreak = True
		elif alienI.visible and alienI.y > 690:
			loopbreak = True
		elif alienJ.visible and alienJ.y > 690:
			loopbreak = True
		elif alienK.visible and alienK.y > 690:
			loopbreak = True
		elif alienL.visible and alienL.y > 690:
			loopbreak = True
		elif alienM.visible and alienM.y > 690:
			loopbreak = True
		elif alienN.visible and alienN.y > 690:
			loopbreak = True
		elif alienO.visible and alienO.y > 690:
			loopbreak = True
		elif alienQ.visible and alienQ.y > 690:
			loopbreak = True
		elif alienR.visible and alienR.y > 690:
			loopbreak = True
		elif alienS.visible and alienS.y > 690:
			loopbreak = True
		elif alienT.visible and alienT.y > 690:
			loopbreak = True

		if not alienA.visible and not alienB.visible and not alienC.visible and not alienD.visible and not alienE.visible and not alienF.visible and not alienG.visible and not alienH.visible and not alienI.visible and not alienJ.visible and not alienK.visible and not alienL.visible and not alienM.visible and not alienN.visible and not alienO.visible and not alienP.visible and not alienQ.visible and not alienR.visible and not alienS.visible and not alienT.visible:
			loopbreak2 = True
			loopbreak = True

		if not alienP.visible:
			win.blit(upgrade, (50, 50))


		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			pause = True

		if pause:
			alienA.vel = 0
			alienB.vel = 0
			alienC.vel = 0
			alienD.vel = 0
			alienE.vel = 0

			alienF.vel = 0
			alienG.vel = 0
			alienH.vel = 0
			alienI.vel = 0
			alienJ.vel = 0

			alienK.vel = 0
			alienL.vel = 0
			alienM.vel = 0
			alienN.vel = 0
			alienO.vel = 0

			alienR.vel = 0
			alienQ.vel = 0
			alienS.vel = 0
			alienT.vel = 0
			win.blit(rstart, (50, 700))
			win.blit(quit, (650, 700))
			win.blit(menu, (50, 750))
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

			alienF.vel = 0
			alienG.vel = 0
			alienH.vel = 0
			alienI.vel = 0
			alienJ.vel = 0

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
					oversound.play()
			if loopbreak2:
				win.blit(winner, (winnx, winny))
			win.blit(rstart, (50, 700))
			win.blit(quit, (650, 700))
			win.blit(menu, (50, 750))
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
