import pygame
#from pygame.locals import *
import random

#define fps
clock = pygame.time.Clock()
fps = 60

# Create Window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
pygame.display.set_caption( "Space Invaders" )


# Define Game Variables
alien_rows = 5
alien_cols = 5

# Define Colors
red = ( 255, 0, 0 )
green = ( 0, 255, 0 )

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
		self.last_shot = pygame.time.get_ticks()
	

	def update( self ):
		# Set Movement Speed
		speed = 8
		cooldown = 500 # milliseconds

		# Get Keypress
		key = pygame.key.get_pressed()
		
		# Movement
		if key[ pygame.K_LEFT ] and self.rect.x > 0:
			self.rect.x -= speed
		if key[ pygame.K_RIGHT ] and self.rect.x < SCREEN_WIDTH - 50:
			self.rect.x += speed
		
		# Record Current Time
		time_now = pygame.time.get_ticks()

		# Shooting
		if key[ pygame.K_SPACE ] and time_now - self.last_shot > cooldown:
			bullet = Bullets( self.rect.centerx, self.rect.top )
			bullet_group.add( bullet )
			self.last_shot = time_now
		
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
	
	def update( self ):
		self.rect.y -= 5
		if self.rect.bottom < 0:
			self.kill()



# Create Aliens
class Aliens( pygame.sprite.Sprite ):
	def __init__( self, x, y ):
		pygame.sprite.Sprite.__init__( self )
		id = random.randint( 1, 5 )
		self.image = pygame.image.load( f"img/alien{id}.png" )
		self.rect = self.image.get_rect()
		self.rect.center = [ x, y ]
		self.move_counter = 0
		self.move_direction = 1
	
	def update( self ):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs( self.move_counter ) > 75:
			self.move_direction *= -1
			self.move_counter *= self.move_direction


# Create Sprite Groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

def create_aliens():
	for row in range( alien_rows ):
		for col in range( alien_cols ):
			alien = Aliens( 100 + col * 100, 100 + row * 70 )
			alien_group.add( alien )

create_aliens()

# Create Player
spaceship = Spaceship( int( SCREEN_WIDTH / 2 ), int( SCREEN_HEIGHT - 100 ), 3 )
spaceship_group.add( spaceship )


run = True
while run:
	clock.tick( fps )
	draw_bg()

	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	# Update Spaceship
	spaceship.update()

	# Update Sprite Groups
	bullet_group.update()
	alien_group.update()

	# Draw Sprite Groups
	spaceship_group.draw( screen )
	bullet_group.draw( screen )
	alien_group.draw( screen )

	# Update The Display
	pygame.display.update()


pygame.quit()