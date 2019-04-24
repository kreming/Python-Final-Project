# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# game settings (64 x 48)
WIDTH = 1024   # 64
HEIGHT = 768  # 48
FPS = 60
TITLE = "Pathfinder®"
BGCOLOR = DARKGREY

TILESIZE = 32
COMPUTER_PLAY_RATE = 20  # 50 is good, 10 for testing quickly
PLAYER_MOVE_RATE = 5 # How many frames between player movements

# Screen IDs
TITLESCREEN = 0
PLAYSCREEN = 1

# Levels
LEVELPATHS = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'mapTest.txt']