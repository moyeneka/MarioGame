import pygame
import time
import random

from pygame.locals import*
from time import sleep

class Sprite():
# constructor
	def __init__(self, xPos, yPos, width, height):
		self.x = xPos
		self.y = yPos
		self.w = width
		self.h = height

class Tube(Sprite):
	def __init__(self,xPos, yPos, m):
		super(Tube,self).__init__(xPos,yPos,55,400)
		self.x = xPos
		self.y = yPos
		self.isRemove = False
		self.model = m
		self.tube_image = pygame.image.load("tube.png")
		

	def update(self):
		pass

	def drawingImages(self, contextToDraw):
		contextToDraw.blit(self.tube_image, (self.x - self.model.mario.x + self.model.mario.marioOffset, self.y))
			

    
     
     
class Mario(Sprite):
	def __init__(self,xPos, yPos, m):
		super(Mario, self).__init__(xPos,yPos,61,95)
		self.x = xPos
		self.y = yPos
		self.model = m
		self.isRemove = False
		self.px = 0
		self.py = 0	
		self.flip = False
		self.movingMario = 0
		self.marioImageNum = 0
		self.numFramesInAir = 0
		self.marioOffset = 100
		self.vert_velocity = 12.0	
		self.mario_Image_Mario = []
		self.mario_Image_Mario.append(pygame.image.load("mario1.png"))
		self.mario_Image_Mario.append(pygame.image.load("mario2.png"))
		self.mario_Image_Mario.append(pygame.image.load("mario3.png"))
		self.mario_Image_Mario.append(pygame.image.load("mario4.png"))
		self.mario_Image_Mario.append(pygame.image.load("mario4.png"))

	def drawingImages(self, contextToDraw):
			#if self.flip:
			#contextToDraw.blit(self.mario_Image_Mario[self.movingMario],(self.marioOffset, self.y, self.w, self.h))
			#else:
			#	contextToDraw.blit(self.mario_Image_Mario[self.movingMario], (self.marioOffset, self.y, self.w, self.h))
			contextToDraw.blit(pygame.transform.flip(self.mario_Image_Mario[self.movingMario], self.flip, False), (self.marioOffset, self.y, self.w, self.h))


 # making mario jump
	def jump(self):
			if self.numFramesInAir < 5:
				self.vert_velocity +=  -20
    
	def savePreviousPosition(self):
			self.px = self.x
			self.py = self.y
    
 # making mario get out of tube 
	def getOutOfTube(self,t): 
			if self.x + self.w >= t.x and self.px + self.w <= t.x:
				self.x = t.x - self.w

			if self.x <= t.x + t.w and self.px >= t.x + t.w:
				self.x = t.x + t.w
    
			if self.y + self.h >= t.y and self.py + self.h <= t.y: 
				self.y = t.y - self.h
				self.vert_velocity = 0
				self.numFramesInAir = 0
			if self.y <= t.y + t.h and self.py >= t.y + t.h:
				self.y = t.y + t.h
			

	def update(self): 
			self.vert_velocity += 3.0
			self.y += self.vert_velocity
			self.numFramesInAir += 1
			if self.y > 400 - self.h:
				self.vert_velocity = 0
				self.y = 400 - self.h
				self.numFramesInAir = 0
			if self.y < 0:
				self.y = 0
				self.vert_velocity = 0
			for i in self.model.sprites:
				if isinstance(i, Tube):
					if self.model.collision(self,i):
						self.getOutOfTube(i)

			

	def move(self): 
				self.movingMario += 1
				if self.movingMario > 4:
					self.movingMario = 0

class Goomba(Sprite):
	def __init__(self, xPos, yPos, m):
		super(Goomba, self).__init__(xPos,yPos,100,118)
		self.x = xPos
		self.y = yPos
		self.model = m
		self.px = 0
		self.py = 0
		self.speed = 7
		self.direction = 1
		self.isOnFire = False
		self.isRemove = False
		self.health = 30
		self.goomba_image = pygame.image.load("goomba.png")
		self.goomba_fire_image = pygame.image.load("goomba_fire.png")

	def savePreviousPosition(self):
		self.px = self.x



   
	def goombaDead(self):
		if self.health <= 0:
			return True
		else:
			return False
   
	def goombaOutOfTube(self, t): 
		if self.x + self.w >= t.x and self.px + self.w <= t.x:
			self.x = t.x - self.w
			self.direction = -1
		if self.x <= t.x + t.w and self.px >= t.x + t.w:
			self.x = t.x + t.w
			self.direction = 1
   
	def setOnFire(self):
		self.isOnFire = True
  
	def update(self):
		self.y = 400 - self.h
		self.savePreviousPosition()
		self.x += self.speed * self.direction

		for i in self.model.sprites:
			if  isinstance(i, Tube):
				if self.model.collision(self, i):
					self.goombaOutOfTube(i)
			if  isinstance(i, Goomba): 
				if self.goombaDead():
					self.isRemove = True
					
		if (self.isOnFire): 
				self.goomba_image = self.goomba_fire_image
				self.health -= 1
     
	def drawingImages(self, contextToDraw):
		contextToDraw.blit(self.goomba_image, (self.x - self.model.mario.x + self.model.mario.marioOffset, self.y))


class Fireball (Sprite):
	def __init__(self,xPos, yPos, f, m):
		super(Fireball, self).__init__(xPos, yPos, 59, 59)
		self.x = xPos
		self.y = yPos
		self.isRemove = False
		self.px = 0
		self.py = 0
		self.moving = 20
		self.model = m
		self.vert_velocity = 12.0
		self.flip = f
		self.fireball = pygame.image.load("fireball.png")

	def update(self):
		self.vert_velocity += 4.7
		self.y += self.vert_velocity
		if self.flip:
			self.x -= self.moving
		else:
			self.x += self.moving
		if self.y > 400 - self.h:
			self.vert_velocity = -30
			self.y = 400 - self.h
		if self.y < 0: 
			self.y = 0
   
		for i in self.model.sprites:
			if isinstance(i, Goomba):
				if self.model.collision(self, i):
					i.setOnFire()
					self.isRemove =True
			if isinstance(i, Fireball): 
				if i.x >= 3000:
					self.isRemove =True
				if i.x <= -500:
					self.isRemove = True

	def drawingImages(self,contextToDraw):
		contextToDraw.blit(self.fireball, (self.x - self.model.mario.x + self.model.mario.marioOffset, self.y))



class Model():
	def __init__(self):
		#	Constructor that initializes an arrayList of mario.
		self.sprites = []
		self.mario = Mario(100,100,self)
		self.sprites.append(self.mario)
		self.sprites.append(Tube(345,180,self))
		self.sprites.append(Tube(620,170,self))
		self.sprites.append(Goomba(430,200,self))
  
	def collision(self, a, b): 
		self.spriteARight = a.x + a.w
		self.spriteALeft = a.x
		self.spriteATop = a.y
		self.spriteABottom = a.y + a.h
		self.spriteBRight = b.x + b.w
		self.spriteBLeft = b.x
		self.spriteBTop = b.y
		self.spriteBBottom = b.y + b.h

		if self.spriteARight <= self.spriteBLeft:
			return False
		if self.spriteALeft >= self.spriteBRight: 
			return False
		if self.spriteABottom <= self.spriteBTop:
			return False
		if self.spriteATop >= self.spriteBBottom:
			return False
		return True
	


	def addFireball(self):
		if(self.mario.flip):
			self.sprites.append(Fireball(self.mario.x, self.mario.y, self.mario.flip, self))
		else:
			self.sprites.append(Fireball(self.mario.x + self.mario.w, self.mario.y, self.mario.flip, self))

	#	Method that calls the update method from the 
	#	Mario class. This ensures the desired outcome and check if goomba is removed or not
	// implemented in the Mario class is achieved.
	def update(self):
		for i in self.sprites:
			i.update()
			if i.isRemove == True:
				self.sprites.remove(i)

     
class View():
	def __init__(self, model):
			screen_size = (800,600)
			self.screen = pygame.display.set_mode(screen_size, 28)
			self.tube_image = pygame.image.load("tube.png")
			self.model = model

	def update(self):
			self.screen.fill([0,200,100])
			for i in self.model.sprites:
				i.drawingImages(self.screen)
			pygame.draw.rect(self.screen, (255,191,0), pygame.Rect(0, 400, 800, 200)) 
			pygame.display.flip()
	



class Controller():
	#Constructor for the Controller class. 
	#It initializes the model. 
	def __init__(self, model, view):
		# Declaring the member variables.
		self.view = view
		self.model = model
		self.keep_going = True
		self.key_right = False
		self.key_left = False
		self.key_up = False
		self.key_down = False
		self.control = False
		self.space = False



	#	Method that updates the view when the left 
	#	and right arrow keys are pressed. This method
	#	also determines the scrolling speed. 
	def update(self):
			for event in pygame.event.get():
				if event.type == QUIT:
					self.keep_going = False
				elif event.type == KEYUP:
					if event.key == K_RIGHT:
						self.key_right = False
					if event.key == K_LEFT:
						self.key_left =	False
					if event.key == K_UP:
						self.key_up = False
					if event.key == K_DOWN: 
						self.key_down = False
					if event.key == K_LCTRL or event.key == K_RCTRL: 
						self.control = False
					if event.key == K_SPACE:
						self.space = False
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.keep_going = False
					if event.key == K_RIGHT:
						self.key_right = True
					if event.key == K_LEFT:
						self.key_left =	True
					if event.key == K_UP:
						self.key_up = True
					if event.key == K_DOWN: 
						self.key_down = True
					if event.key == K_LCTRL or event.key == K_RCTRL : 
						self.control = True
					if event.key == K_SPACE:
						self.space = True
			self.model.mario.savePreviousPosition()
			if self.key_right:
				self.model.mario.flip = False
				self.model.mario.x +=5
				self.model.mario.move()
			if self.key_left:
				self.model.mario.flip = True
				self.model.mario.x -=5
				self.model.mario.move()

			#Making mario jump
			if self.key_up or self.space:
				self.model.mario.jump()
			# make mario shoot fire ball
			if self.control :
				self.model.addFireball()






print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m,v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")