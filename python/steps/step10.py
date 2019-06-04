###############################################################################
# Step 10
###############################################################################
# Score board.  Scoring works like this:
#	Every piece that sets is worth 5.
#	When clearing lines:
# 		The first line scores 50
# 		The second line scores 100
# 		The third line scores 150
# 		The fourth line scores 200
#
#	This means that 1 line totals 50, 2 lines totals 150, 
# 	3 lines totals 300 and 4 lines totals 500.
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

# Start the score at 0
score = 0

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
			# If the piece is set too high, it will stack above the "kill" line at the top.
			# If this happened, it's game over.  We know that it happened if the part is 
			# going to be set and its row  index is less than 0.
			(x, y) = this_piece.position
			if (y < 0):
				game_sounds.game_over.play()
				g.show_game_over(screen, screen_size)
				sys.exit()

			# Set the piece by drawing its matrix onto the well matrix and starting a new piece.
			g.impose_matrix(this_piece.matrix, well_matrix, this_piece.position)

			if g.has_lines_to_clear(well_matrix):
				clear_count = len(g.get_lines_to_clear(well_matrix))
				for multiplier in range(clear_count):
					score = score + 50 * (multiplier + 1)
				g.draw_clearings(screen, screen_size, well_matrix, game_sounds.crunch)
				g.compact_well(well_matrix)
				game_sounds.line_clear.play()
			else:
				score = score + 5
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

	# Draw the score box
	g.draw_scoreboard(screen, screen_size, score)

	# Put the scene on the monitor.
	pygame.display.update()

# End of game loop.
