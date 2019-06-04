###############################################################################
# Step 7
###############################################################################
# Move and rotate pieces
###############################################################################

import pygame
from pygame.locals import *
import sys
import functions
from gamedata import GameData
from graphics import *
from sounds import *

pygame.mixer.pre_init(22050, -16, 2, 256)
pygame.init()
pygame.mixer.init()

# Game Setup
g = functions.GameFunctions()

# Setup for the screen.
screen_size = (640, 480) 
screen = pygame.display.set_mode([screen_size[0], screen_size[1]])
pygame.display.set_caption("Tetris")
img_background_scaled = pygame.transform.scale(img_background, screen_size)

# Load sounds
game_sounds = GameSounds()

# Decide which piece we will use first.
this_piece = g.new_piece()

# Create an empty well.
well_matrix = g.new_well()

# Timing
difficulty = 1.0
last_descent_ticks = pygame.time.get_ticks()
hover_duration = int(1000 / difficulty)

# This is the main game loop.  Everything below here repeats forever.
while True:
	pygame.time.Clock().tick(1000/30)

	for event in pygame.event.get():
		# Pay attention if the user clicks the X to quit.
		if event.type == pygame.QUIT:
			sys.exit()

		# Check the keyboard for keypresses. (These buttons must be pressed repeatedly.)
		if event.type == pygame.KEYDOWN:
			if (event.key == K_ESCAPE):
				sys.exit()
			if (event.key == K_LEFT):
				this_piece.move_left(well_matrix)
			if (event.key == K_RIGHT):
				this_piece.move_right(well_matrix)
			if (event.key == K_SPACE):
				this_piece.rotate(well_matrix)

	# If DOWN is held, drop it faster
	keys = pygame.key.get_pressed()
	if (keys[K_DOWN]):
		dropping_speed = int(hover_duration / 10 * 95)
	else:
		dropping_speed = 0

	# If it's time to move the piece down, check to see if it will be set.
	if (last_descent_ticks + hover_duration - dropping_speed <= pygame.time.get_ticks()):
		
		# To determine if the piece will set, we look to see if there are any well bricks
		# directly underneath any piece bricks.  We do that by merging the two matrices
		# and adding the values of the cells at the piece's next location to the same cells in the well.
		# If any cells have a value of 2 then both matrices have a cell in the same position.
		# That's a collision.  Therefore, we can't move the piece down to the next position.

		# If the piece hits the bottom of the well, it sets.
		will_set = g.piece_will_set(this_piece, well_matrix)
		
		if (will_set):
			# Set the piece by drawing its matrix onto the well matrix and starting a new piece.
			g.impose_matrix(this_piece.matrix, well_matrix, this_piece.position)

			game_sounds.thud.play()
			
			# Start the next piece.
			this_piece = g.new_piece()
		else:
			this_piece.move_down()

		last_descent_ticks = pygame.time.get_ticks()

	# Draw the background
	screen.blit(img_background_scaled, (0, 0))

	# Draw the well
	g.draw_well(screen, screen_size)

	# Draw the well grid (if turned on)
	g.draw_well_grid(screen, screen_size)
	
	# Draw the bricks in the well matrix
	g.draw_well_matrix(screen, screen_size, well_matrix)

	# Draw the piece matrix
	g.draw_piece_matrix(screen, screen_size, this_piece)

	# Put the scene on the monitor.
	pygame.display.update()

# End of game loop.
