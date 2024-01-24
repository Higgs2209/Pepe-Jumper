import pygame
from utils import resource_path

# initialize pygame
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BROKEN_PLATFORM_RESOURCE_PATH = resource_path("assets/broken platform.png")

