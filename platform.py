import pygame
from utils import resource_path
import random

# initialize pygame
pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLATFORM_RESOURCE_PATH = resource_path("assets/wood.png")
platform_image = pygame.image.load(PLATFORM_RESOURCE_PATH).convert_alpha()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 10))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(1, 3)

    def update(self, scroll):
        # Move platforms side to side if moving platform
        if self.moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        # Change platform direction
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        # Update platforms vertically
        self.rect.y += scroll

        # Check if platform is off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
