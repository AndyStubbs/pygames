import random

print("Welcome to the guessing game!")
print("I'm thinking of a number between 1 and 100")

answer = random.randint(1, 100)
while True:
	guess = int(input("Make a guess: "))
	print( f"You guessed {guess}" )
	if guess < answer:
		print("Too Low!")
	elif guess > answer:
		print("Too High!")
	else:
		print("Correct!")
		break

print("Thanks for playing!")
input("Press Enter to exit...")
