import pygame
from pygame.locals import *

#define fps
clock = pygame.time.Clock()
fps = 60

# Create Window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
pygame.display.set_caption( "Space Invaders" )

# Define Colors
red = (255, 0, 0)
green = (0, 255, 0)

# Background Image
bg = pygame.image.load( "img/bg.png" )
def draw_bg():
	screen.blit( bg, ( 0, 0 ) )


# Create Spaceship
class Spaceship( pygame.sprite.Sprite ):
	def __init__( self, x, y, health ):
		pygame.sprite.Sprite.__init__( self )
		self.image = pygame.image.load( "img/spaceship.png" )
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.health_start = health
		self.health_remaining = health
	def update( self ):
		# Set Movement Speed
		speed = 8

		# Get Keypress
		key = pygame.key.get_pressed()
		if key[ pygame.K_LEFT ] and self.rect.x > 0:
			self.rect.x -= speed
		if key[ pygame.K_RIGHT ] and self.rect.x < SCREEN_WIDTH - 50:
			self.rect.x += speed
		
		# Draw Health Bar
		pygame.draw.rect( screen, red, ( self.rect.x, self.rect.bottom + 10, self.rect.width, 15 ) )
		if self.health_remaining > 0:
			pygame.draw.rect(
				screen, green, (
					self.rect.x, self.rect.bottom + 10, int( self.rect.width * ( self.health_remaining / self.health_start ) ), 15 
				)
			)

# Create Bullets
class Bullets( pygame.sprite.Sprite ):
	def __init__( self, x, y ):
		pygame.sprite.Sprite.__init__( self )
		self.image = pygame.image.load( "img/bullet.png" )
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]


# Create Sprite Groups
spaceship_group = pygame.sprite.Group()


# Create Player
spaceship = Spaceship( int( SCREEN_WIDTH / 2 ), int( SCREEN_HEIGHT - 100 ), 3 )
spaceship_group.add(spaceship)

run = True
while run:
	clock.tick(fps)
	draw_bg()

	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	# Update Spaceship
	spaceship.update()

	# Draw Sprite Groups
	spaceship_group.draw(screen)

	pygame.display.update()


pygame.quit()