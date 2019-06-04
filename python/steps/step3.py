###############################################################################
# Step 3
###############################################################################
# Create and draw the well.
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

# Create an empty well.
well_matrix = g.new_well()

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

	# Draw the background
	screen.blit(img_background_scaled, (0, 0))

	# Draw the well
	g.draw_well(screen, screen_size)

	# Draw the well grid (if turned on)
	g.draw_well_grid(screen, screen_size)

	# Put the scene on the monitor.
	pygame.display.update()

# End of game loop.
