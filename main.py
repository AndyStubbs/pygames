import pygame

pygame.init()

# Setup the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup the player
player = pygame.Rect((300, 250, 50, 50))

run = True
while run:
	screen.fill((0, 0, 0))
	pygame.draw.rect(screen, (255, 0, 0), player)

	key = pygame.key.get_pressed()
	if key[pygame.K_LEFT]:
		player.move_ip(-1, 0)
	if key[pygame.K_RIGHT]:
		player.move_ip(1, 0)
	if key[pygame.K_UP]:
		player.move_ip(0, -1)
	if key[pygame.K_DOWN]:
		player.move_ip(0, 1)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	pygame.display.update()

pygame.quit()