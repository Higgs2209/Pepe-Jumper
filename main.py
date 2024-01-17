from utils import resource_path
import pygame
from platform import Platform
import random


# initialize pygame
pygame.init()

# Game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Define Colours
WHITE = (255, 255, 255)

# Game Variables
GRAVITY = 1
MAX_PLATFORMS = 10

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pepe Jumper")

# Asset Loading
PEPE_RESOURCE_PATH = resource_path('assets/pepe.png')
pepe_image = pygame.image.load(PEPE_RESOURCE_PATH).convert_alpha()
BG_RESOURCE_PATH = resource_path("assets/bg.png")
bg_image = pygame.image.load(BG_RESOURCE_PATH).convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pepe_image, (45, 45))

        # Create the player rectangle
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        # Create a mask
        self.pepe_mask = pygame.mask.from_surface(self.image)

        # Create momentum and direction
        self.momentum = 0
        self.direction = 0
        self.movement_speed = 0
        self.flip = False

        # Y Velocity
        self.vel_y = 0

    def move(self):

        # reset the variables
        dx = 0
        dy = 0

        # Process Keyboard events
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.direction = -1
            self.flip = True
            dx -= self.movement_speed + self.momentum

            if self.momentum < 5:
                self.momentum += 0.5

        elif key[pygame.K_d]:
            self.direction = 1
            self.flip = False
            dx += self.movement_speed + self.momentum

            if self.momentum < 5:
                self.momentum += 0.5

        else:
            # if no keys are pressed, gradually lower the momentum
            if self.momentum > 0:
                dx += (self.movement_speed * self.direction) + (self.momentum * self.direction)
                self.momentum -= 0.5

        # Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Ensure player stays within the screen
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right



        # Check collision with platforms
        #for platform in platform_group:
        #if platform.mask.overlap(self.pepe_mask, (self.rect.x, self.rect.y)):
      #      print("Collide")




        # Check if the player goes of the bottom of the screen
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0
            self.vel_y = -20

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

       # if self.pepe_mask.overlap(platform.mask, (self.rect.x, self.rect.y)):
        #    print("Collide")

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Draw Mask
        # olist = self.pepe_mask.outline()
        # pygame.draw.lines(screen, (255, 0, 0), 1, olist)


# Game Loop
run = True

# call player class

pepe = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
pepe_group = pygame.sprite.Group()
pepe_group.add(pepe)

# Platform Instance
platform_group = pygame.sprite.Group()

# Create temporary platform
for p in range(MAX_PLATFORMS):
    p_w = random.randint(40, 60)
    p_x = random.randint(0, SCREEN_WIDTH - p_w)
    p_y = p * random.randint(80, 120)
    platform = Platform(p_x, p_y, p_w)

    platform_group.add(platform)


def collide():
    if pygame.sprite.spritecollide(pepe, platform_group, False, pygame.sprite.collide_mask):
        print('collide')
    else:
        print("No Collide")



while run:

    # Set Frame Rate
    clock.tick(FPS)

    # Run move method
    pepe.move()

    # Draw Background
    screen.blit(bg_image, (0, 0))

    # Draw Sprites
    platform_group.draw(screen)
    pepe.draw()

    # Check for collisions
    collide()



    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update Display
    pygame.display.update()

pygame.quit()
