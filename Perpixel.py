import pygame
from pygame.locals import *

MAP_SIZE = (100, 60) #size in tiles
CAMERA_SIZE = (640, 480) #size in pixels

class ImageManager:
	def __init__(self):
		self.images = {}

	def use(self, filename): #just in time image loader
		if not (filename in self.images.keys()):
			self.images[filename] = pygame.image.load(filename)
		return self.images[filename]

class Tile:
	def __init__(self, pos, filename = "tile.png"):
		self.x = pos[0]*32
		self.y = pos[1]*32
		self.sprite = filename

class Map:
	def __init__(self):
		self.width = MAP_SIZE[0]
		self.height = MAP_SIZE[1]
		self.map = []
		
		for x in range(self.width):
			self.map.append([])
			for y in range(self.height):
				self.map[x].append(Tile((x, y)))

class Camera:
	def __init__(self):
		self.velX = 0.0
		self.velY = 0.0
		self.maxVel = 20
		self.x = 0
		self.y = 0
		self.scroll_speed = 1
		self.friction = 0.5

	def addVelX(self, right = True):
		if right and not (self.velX >= self.maxVel):
			self.velX += 1
		else:
			if not (self.velX <= ((-1)*self.maxVel)):
				self.velX -= 1
	
	def addVelY(self, down = True):
		if down and not (self.velY >= self.maxVel):
			self.velY += 1
		else:
			if not (self.velY <= ((-1)*self.maxVel)):
				self.velY -= 1
	
	def tick(self, pressed):
		self.changeX(int(self.velX))
		self.changeY(int(self.velY))
		if not pressed:
			if self.velX > 0:
				self.velX -= self.friction
			elif self.velX < 0:
				self.velX += self.friction
			if self.velY > 0:
				self.velY -= self.friction
			elif self.velY < 0:
				self.velY += self.friction

	def changeX(self, x):
		self.x += x
		if self.x < 0:
			self.x = 0
		if self.x > (((MAP_SIZE[0]-1)*32)-CAMERA_SIZE[0]):
			self.x = ((MAP_SIZE[0]-1)*32)-CAMERA_SIZE[0]

	def changeY(self, y):
		self.y += y
		if self.y < 0:
			self.y = 0
		if self.y > (((MAP_SIZE[1]-1)*32)-CAMERA_SIZE[1]):
			self.y = ((MAP_SIZE[1]-1)*32)-CAMERA_SIZE[1]

def main():
	print "initializing pygame"
	pygame.init()
	print "initializing display"
	screen = pygame.display.set_mode(CAMERA_SIZE, DOUBLEBUF)
	manager = ImageManager()
	print "initializing clock"
	clock = pygame.time.Clock()

	print "creating map"
	map = Map()

	print "initializing camera"
	camera = Camera()

	keys = []
	running = True
	while running:
		clock.tick(60)

		#process events
		running = processEvents(keys, camera)

		#render
		render(manager, screen, map, camera)

	pygame.quit()

def processEvents(keys, camera):
	mouseRel = pygame.mouse.get_rel()
	pressed = False
	if pygame.mouse.get_pressed()[2]:
		pressed = True
	running = True
	for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if event.type == KEYDOWN:
				keys.append(event.key)
			if event.type == KEYUP:
				keys.remove(event.key)
			if event.type == MOUSEBUTTONUP:
				if event.button == 2:
					camera.setVel(0, 0)

	for key in keys:
		if key == K_ESCAPE:
			running = Fals

	if pressed:
		if mouseRel[0] > 0:
			camera.addVelX()
		elif mouseRel[0] < 0:
			camera.addVelX(False)
		if mouseRel[1] > 0:
			camera.addVelY()
		elif mouseRel[1] < 0:
			camera.addVelY(False)

	camera.tick(pressed)


	return running

def render(manager, screen, map, camera):
	range_x = CAMERA_SIZE[0]/32
	if camera.x % 32 != 0:
		range_x += 1
	range_y = CAMERA_SIZE[1]/32
	if camera.y % 32 != 0:
		range_y += 1

	screen.fill((0,0,0))
	for x in range(range_x):
		for y in range(range_y):
			tile = map.map[((camera.x/32)+x)][((camera.y/32)+y)]
			screen.blit(manager.use(tile.sprite), ((tile.x-camera.x), (tile.y-camera.y)))
	caption = "[" + str(camera.x)+","+str(camera.y)+"], ("+str(camera.velX)+","+str(camera.velY)+")"
	pygame.display.set_caption(caption)
	pygame.display.update()

main()
