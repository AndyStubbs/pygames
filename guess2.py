import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32
FONT = pygame.font.SysFont("Arial", FONT_SIZE)

screen = pygame.display.set_mode( ( WIDTH, HEIGHT ) )
pygame.display.set_caption( "Space Invaders" )

def guessing_game():
	# Set the range for the random number
	min_num = 1
	max_num = 100

	# Generate a random number within the range
	secret_number = random.randint(min_num, max_num)

	# Initialize the number of attempts
	attempts = 0

	# Create the game window
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Guessing Game")

	clock = pygame.time.Clock()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				# Ask the user for their guess
				try:
					guess = int(input("Enter your guess: "))
				except ValueError:
					print("That's not a valid number!")
					continue

				# Check if the guess is within the range
				if guess < min_num or guess > max_num:
					print(f"Please enter a number between {min_num} and {max_num}.")
					continue

				# Increment the number of attempts
				attempts += 1

				# Check if the guess is correct
				if guess == secret_number:
					print(f" Congratulations! You found the number in {attempts} attempts.")
					running = False
				elif guess < secret_number:
					screen.fill(WHITE)
					text = FONT.render("Too low!", True, BLACK)
					screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
					pygame.display.update()
					pygame.time.wait(500)  # Wait for 0.5 seconds
				else:
					screen.fill(WHITE)
					text = FONT.render("Too high!", True, BLACK)
					screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
					pygame.display.update()
					pygame.time.wait(500)  # Wait for 0.5 seconds

		# Check if the user pressed a key without closing the window
		keys = pygame.key.get_pressed()
		if not (keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]):
			running = False
	
	print( "Thanks for playing!" )
	pygame.quit()

print("Welcome to the Guessing Game!")
guessing_game()
