import pygame
import sys
import os
pygame.init()




def restart():
	win = pygame.display.set_mode((1600,900))
	pygame.display.set_caption("Space Invaders")

	ship = pygame.image.load('ship.png').convert_alpha()
	shipleft = pygame.image.load('shipleft.png').convert_alpha()
	shipright = pygame.image.load('shipright.png').convert_alpha()
	bg = pygame.image.load('bgA.jpg').convert_alpha()
	walk = pygame.image.load('alien.png').convert_alpha()
	walkA = pygame.image.load('alienA.png').convert_alpha()
	walkB = pygame.image.load('shooter.png').convert_alpha()
	gameover = pygame.image.load('gameover.png').convert_alpha()
	winner = pygame.image.load('win.png').convert_alpha()
	rstart = pygame.image.load('restart.png').convert_alpha()
	quit = pygame.image.load('quit.png').convert_alpha()
	menu = pygame.image.load('menu.png').convert_alpha()
	die =  pygame.image.load('explo.png').convert_alpha()
	lvl =  pygame.image.load('lvl2.png').convert_alpha()


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
	mute = False
	mutelock = False

	speedup = False
	loopbreak = False
	loopbreak2 = False

	overy = 350
	overx = 650

	winny = 405
	winnx = 675

	alienyA = 100
	alienyB = 150
	alienyC = 200

	deathsoundcounter = 0

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

	class enemyA(object):
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

	class enemyB(object):
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
			self.move()
			if self.visible:
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

	class enemyC(object):
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

	class enemyD(object):
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

	class enemyE(object):
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

	class enemyF(object):
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

	class enemyG(object):
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

	class enemyH(object):
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

	class enemyI(object):
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

	class enemyJ(object):
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

	class enemyK(object):
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

	class enemyO(object):
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
		alienF.draw(win)
		alienG.draw(win)
		alienH.draw(win)
		alienI.draw(win)
		alienJ.draw(win)
		alienK.draw(win)
		alienO.draw(win)
		for bullet in bullets:
			bullet.draw(win)
		for bulletA in bulletsA:
			bulletA.draw(win)
		for bulletB in bulletsB:
			bulletB.draw(win)
		for bulletC in bulletsC:
			bulletC.draw(win)



	font00 = pygame.font.SysFont('comicsans', 30, True)
	man = player(800, 750, 35, 45)
	alienA = enemyA(350, alienyA, 34, 27, 850)
	alienB = enemyB(450, alienyA, 34, 27, 950)
	alienC = enemyC(550, alienyA, 34, 27, 1050)
	alienD = enemyD(650, alienyA, 34, 27, 1150)
	alienE = enemyE(750, alienyA, 34, 27, 1250)
	alienF = enemyF(350, alienyC, 34, 27, 850)
	alienG = enemyG(450, alienyC, 34, 27, 950)
	alienH = enemyH(550, alienyC, 34, 27, 1050)
	alienI = enemyI(650, alienyC, 34, 27, 1150)
	alienJ = enemyJ(750, alienyC, 34, 27, 1250)
	alienK = enemyK(350, alienyB, 34, 27, 850)
	alienO = enemyO(750, alienyB, 34, 27, 1250)
	shootloop = 0
	shootloopA = 0
	shootloopB = 0
	shootloopC = 0
	bullets = []
	bulletsA = []
	bulletsB = []
	bulletsC = []

	while True:
		pygame.time.delay(11)

		if alienB.x < 900:
			MoveDown = True
		if (alienB.x > 900) and MoveDown:
			MoveDownCounter += 1
			MoveDown = False
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


		if alienO.visible:
			for bullet in bullets:
				if bullet.y - bullet.radius < alienO.hitbox[1] + alienO.hitbox[3] and bullet.y + bullet.radius > alienO.hitbox[1]:
					if bullet.x + bullet.radius > alienO.hitbox[0] and bullet.x - bullet.radius < alienO.hitbox[0] + alienO.hitbox[2]:
						alienO.hit()
						Score += 1
						bullets.pop(bullets.index(bullet))


		if man.visible:
			for bulletA in bulletsA:
				if bulletA.y - bulletA.radius < man.hitbox[1] + man.hitbox[3] and bulletA.y + bulletA.radius > man.hitbox[1]:
					if bulletA.x + bulletA.radius > man.hitbox[0] and bulletA.x - bulletA.radius < man.hitbox[0] + man.hitbox[2]:
						win.blit(gameover, (overx, overy))
						loopbreak = True
						bulletsA.pop(bulletsA.index(bulletA))

		if man.visible:
			for bulletB in bulletsB:
				if bulletB.y - bulletB.radius < man.hitbox[1] + man.hitbox[3] and bulletB.y + bulletB.radius > man.hitbox[1]:
					if bulletB.x + bulletB.radius > man.hitbox[0] and bulletB.x - bulletB.radius < man.hitbox[0] + man.hitbox[2]:
						win.blit(gameover, (overx, overy))
						loopbreak = True
						bulletsB.pop(bulletsB.index(bulletB))


		if man.visible:
			for bulletC in bulletsC:
				if bulletC.y - bulletC.radius < man.hitbox[1] + man.hitbox[3] and bulletC.y + bulletC.radius > man.hitbox[1]:
					if bulletC.x + bulletC.radius > man.hitbox[0] and bulletC.x - bulletC.radius < man.hitbox[0] + man.hitbox[2]:
						win.blit(gameover, (overx, overy))
						loopbreak = True
						bulletsC.pop(bulletsC.index(bulletC))


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
					if len(bullets) < 1:
						bullets.append(projectileA(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,255,255)))
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
		elif alienF.visible and alienF.y > 740:
			loopbreak = True
		elif alienG.visible and alienG.y > 740:
			loopbreak = True
		elif alienH.visible and alienH.y > 740:
			loopbreak = True
		elif alienI.visible and alienI.y > 740:
			loopbreak = True
		elif alienJ.visible and alienJ.y > 740:
			loopbreak = True
		elif alienK.visible and alienK.y > 740:
			loopbreak = True
		elif alienO.visible and alienO.y > 740:
			loopbreak = True

		if not alienA.visible and not alienB.visible and not alienC.visible and not alienD.visible and not alienE.visible and not alienF.visible and not alienG.visible and not alienH.visible and not alienI.visible and not alienJ.visible and not alienK.visible and not alienO.visible:
			loopbreak2 = True
			loopbreak = True

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
			alienO.vel = 0
			win.blit(rstart, (350, 750))
			win.blit(quit, (950, 750))
			win.blit(menu, (350, 800))
			if keys[pygame.K_q]:
				exit()
			if keys[pygame.K_r]:
				restart()
			if keys[pygame.K_m]:
				exit()



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
			alienO.vel = 0
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
				exit()
			if keys[pygame.K_r]:
				restart()
			if keys[pygame.K_m]:
				exit()


		pygame.display.update()
		rewindow()

restart()
