import pygame
import random

#define fps
clock = pygame.time.Clock()
fps = 60

# Create Window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ) )
pygame.display.set_caption( "Space Invaders" )

# Init Stuff
pygame.mixer.init()
pygame.font.init()

# Define Game Variables
alien_rows = 5
alien_cols = 5
alien_width = 50
alien_height = 50
alien_drop = False
alien_speed = 1
alien_move_delay = 2
level = 1
score = 0
invader_font = pygame.font.Font( "img/invaders.ttf", 40 )
game_over = False
game_over_time = 0

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
		global alien_group, bullet_group, explosion_group
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
			bullet = Bullets( self.rect.centerx, self.rect.top, -5, alien_group )
			bullet_group.add( bullet )
			self.last_shot = time_now
		
		# Check if hit alien ship
		if pygame.sprite.spritecollide( self, alien_group, False ):
			self.health_remaining = 0

		# Draw Health Bar
		pygame.draw.rect( screen, red, ( self.rect.x, self.rect.bottom + 10, self.rect.width, 15 ) )
		if self.health_remaining > 0:
			pygame.draw.rect(
				screen, green, (
					self.rect.x,
					self.rect.bottom + 10,
					int( self.rect.width * ( self.health_remaining / self.health_start ) ),
					15
				)
			)
		
		# If hit, create explosion
		if self.health_remaining == 0:
			explosion = Explosion( self.rect.centerx, self.rect.centery )
			explosion_group.add( explosion )
			self.kill()

# Create Bullets
class Bullets( pygame.sprite.Sprite ):
	def __init__( self, x, y, y_dir, hit_group ):
		pygame.sprite.Sprite.__init__( self )
		self.image = pygame.image.load( "img/bullet.png" )
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.hit_group = hit_group
		self.y_dir = y_dir
		sound = pygame.mixer.Sound( "img/laser.wav" )
		sound.set_volume( 0.1 )
		pygame.mixer.Sound.play( sound )
	
	def update( self ):
		is_hit = False
		self.rect.y += self.y_dir
		for hit_item in self.hit_group:
			if pygame.sprite.collide_rect( self, hit_item ):
				hit_item.health_remaining -= 1
				if hit_item.health_remaining == 0:
					global score
					if isinstance( hit_item, Aliens ):
						score += level * 10
					self.hit_group.remove( hit_item )
				explosion = Explosion( hit_item.rect.centerx, hit_item.rect.centery )
				explosion_group.add( explosion )
				is_hit = True
		if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or is_hit:
			self.kill()


# Create Aliens
class Aliens( pygame.sprite.Sprite ):
	def __init__( self, x, y ):
		global alien_move_delay
		pygame.sprite.Sprite.__init__( self )
		id = random.randint( 1, 5 )
		self.frames = [ pygame.image.load( f"img/alien{id}a.png" ), pygame.image.load( f"img/alien{id}b.png" ) ]
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.image = self.frames[0]
		self.rect = self.image.get_rect()
		self.rect.center = [ x, y ]
		self.move_direction = 1
		self.move_delay = alien_move_delay
		self.health_remaining = 1
	
	def update( self ):
		global alien_drop, alien_move_delay, spaceship_group, alien_speed

		# Animate Aliens
		if pygame.time.get_ticks() - self.last_update > 300:
			self.frame = random.randint( 0, 1 )
			self.image = self.frames[ self.frame ]
			self.last_update = pygame.time.get_ticks()
		
		# Move Aliens
		self.move_delay -= 1
		if self.move_delay == 0:
			self.move_delay = alien_move_delay
			self.rect.x += self.move_direction * alien_speed
			if self.rect.x + alien_width > SCREEN_WIDTH or self.rect.left < 0:
				alien_drop = True
		
		# Fire Bullets
		if random.randint( 1, 2000 ) < level * 2:
			bullet = Bullets( self.rect.centerx, self.rect.bottom, 5, spaceship_group )
			bullet_group.add( bullet )
		
		# Check if Alien Reach Bottom
		if self.rect.bottom > SCREEN_HEIGHT:
			for item in spaceship_group:
				item.health_remaining = 0
			
			# Create Explosion on spaceship
			explosion = Explosion(
				spaceship_group.sprites()[0].rect.centerx,
				spaceship_group.sprites()[0].rect.centery
			)
			explosion_group.add( explosion )




# Create Explosion
class Explosion( pygame.sprite.Sprite ):
	def __init__( self, x, y ):
		pygame.sprite.Sprite.__init__( self )
		self.frame = 0
		self.frames = []
		for i in range( 1, 6 ):
			self.frames.append( pygame.image.load( f"img/exp{i}.png" ) )
		self.image = self.frames[ 0 ]
		self.rect = self.image.get_rect()
		self.rect.center = [ x, y ]
		self.last_update = pygame.time.get_ticks()
		sound = pygame.mixer.Sound( "img/explosion.wav" )
		sound.set_volume( 0.25 )
		pygame.mixer.Sound.play( sound )
	
	def update( self ):
		if pygame.time.get_ticks() - self.last_update > 50:
			self.frame += 1
			if self.frame == len( self.frames ):
				self.kill()
			else:
				self.image = self.frames[ self.frame ]
				self.last_update = pygame.time.get_ticks()



# Create Sprite Groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# Create Aliens
def create_aliens():
	buffer = 100
	for row in range( alien_rows ):
		for col in range( alien_cols ):
			alien = Aliens( buffer + col * alien_width * 2, buffer + row * alien_height )
			alien_group.add( alien )

create_aliens()

# Create Player
spaceship = Spaceship( int( SCREEN_WIDTH / 2 ), int( SCREEN_HEIGHT - 100 ), 3 )
spaceship_group.add( spaceship )

run = True
while run:
	clock.tick( fps )
	draw_bg()

	# Check Number of Aliens
	aliens = len( alien_group )
	if aliens == 0:
		create_aliens()
		level += 1
		if level > 5:
			alien_move_delay = 0
	elif not game_over:
		base_speed = 1 + ( level - 1 )
		if aliens == 1:
			alien_speed = base_speed + 10
		elif aliens < 4:
			alien_speed = base_speed + 3
		elif aliens < 8:
			alien_speed = base_speed + 2
		elif aliens < 16:
			alien_speed = base_speed + 1
		else:
			alien_speed = base_speed
	


	# Display Level
	level_label = invader_font.render( f"{level}", 1, green )
	screen.blit( level_label, ( 10, 10 ) )

	# Display Score
	score_text = f"{score}"
	score_label = invader_font.render( f"{score}", 1, green )
	screen.blit( score_label, ( SCREEN_WIDTH - ( len( score_text ) * 40 + 10 ), 10 ) )
	
	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	
	alien_drop = False

	# Update Sprite Groups
	if not game_over:
		spaceship.update()
	
	bullet_group.update()
	alien_group.update()
	explosion_group.update()

	# Check if Aliens Reach Edge of Screen
	if not game_over and alien_drop:
		for alien in alien_group:
			alien.move_direction *= -1
			alien.rect.y += 50

	# Draw Sprite Groups
	spaceship_group.draw( screen )
	bullet_group.draw( screen )
	alien_group.draw( screen )
	explosion_group.draw( screen )

	if not game_over and spaceship.health_remaining == 0:
		alien_speed = 0
		game_over = True
		game_over_time = pygame.time.get_ticks() + 5000
	
	if game_over:
		game_over_text = "Game Over!"
		level_label = invader_font.render( f"Game Over!", 1, green )
		screen.blit(
			level_label,
			( int( SCREEN_WIDTH / 2 ) - len( game_over_text ) * 20,
			int( SCREEN_HEIGHT / 2 ) - 25 )
		)
		if pygame.time.get_ticks() > game_over_time:
			run = False
	
	# Update The Display
	pygame.display.update()

pygame.quit()
