import pygame
from utils import resource_path

# initialize pygame
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



PLATFORM_RESOURCE_PATH = resource_path("assets/wood.png")
platform_image = pygame.image.load(PLATFORM_RESOURCE_PATH).convert_alpha()


# Max Platforms


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
