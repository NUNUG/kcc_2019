import os
import os.path
import pygame
from gamedata import *

#filename = "../assets/sounds/thud.wav"
#filename = GameData.SOUND_THUD_FILENAME
#exists = os.path.isfile(filename)
#print (exists)
#print (os.getcwd())
# cpath = os.path.join(os.getcwd(), GameData.SOUND_THUD_FILENAME)
# print ("CPath: ")
# print (cpath)
# cpathexists = os.path.isfile(cpath)
# print (cpathexists)
# abspath = os.path.abspath(cpath)
# print("AbsPath: ")
# print(abspath)
# abspathexists = os.path.isfile(abspath)
# print(abspathexists)

class GameSounds:
	def __init__(self):
		self.thud = pygame.mixer.Sound(GameData.SOUND_THUD_FILENAME)
		self.line_clear = pygame.mixer.Sound(GameData.SOUND_LINE_CLEAR_FILENAME)
		self.crunch = pygame.mixer.Sound(GameData.SOUND_CRUNCH_FILENAME)
		self.game_over = pygame.mixer.Sound(GameData.SOUND_GAMEOVER_FILENAME)
