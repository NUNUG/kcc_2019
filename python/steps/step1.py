###############################################################################
# Final Game
###############################################################################
# This is the finished game
# Instructions:
# 	Left or right to move the piece.
#	Space-bar to rotate
#	Down to drop the piece
#	Fill all the blocks in a line to clear the line.  
#	Clear multiple lines at once for more points!
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

# Setup for the screen.
screen_size = (640, 480) 
screen = pygame.display.set_mode([screen_size[0], screen_size[1]])
pygame.display.set_caption("Tetris")
img_background_scaled = pygame.transform.scale(img_background, screen_size)

# Load sounds
game_sounds = GameSounds()

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

# End of game loop.
