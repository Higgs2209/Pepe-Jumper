import pygame
from utils import resource_path
from spritesheet import SpriteSheet
import random

class Apple(pygame.sprite.Sprite):
    def __init__(self, screen_width, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)
        # Animation variables
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        animation_steps = 8
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)

        # Select starting image and create retangle from it
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        location_x = random.randint(5, screen_width - 50)
        location_y = random.randint(0, 400)

        self.rect.x = location_x

        self.rect.y = location_y
    def update(self, scroll, screen_width, screen_height):
        # Update animation
        ANIMATION_COOLDOWN = 50
        # Update image depending on current frame
        self.image = self.animation_list[self.frame_index]
        # Check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # If animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        self.rect.y += scroll

        # Check if off the screen
        if self.rect.top > screen_height:
            print("Kill Appple")
            self.kill()