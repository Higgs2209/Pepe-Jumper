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
MAX_PLATFORMS = 20
SCROLL_THRESHOLD = 150

bg_scroll = 0

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


# Function to draw the background
def draw_background(bg_scroll):
    # Draw Background
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


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

        # Velocity and direction
        self.dy = 0
        self.dx = 0

    def move(self):

        # reset the variables
        self.dx = 0
        self.dy = 0
        scroll = 0

        # Process Keyboard events
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.direction = -1
            self.flip = True
            self.dx -= self.movement_speed + self.momentum

            if self.momentum < 5:
                self.momentum += 0.5

        elif key[pygame.K_d]:
            self.direction = 1
            self.flip = False
            self.dx += self.movement_speed + self.momentum

            if self.momentum < 5:
                self.momentum += 0.5

        else:
            # if no keys are pressed, gradually lower the momentum
            if self.momentum > 0:
                self.dx += (self.movement_speed * self.direction) + (self.momentum * self.direction)
                self.momentum -= 0.5

        # Gravity
        self.vel_y += GRAVITY
        self.dy += self.vel_y

        # Allow player to scroll off the screen
        if self.rect.left + self.dx < 0:
            self.rect.right = 400
            print("Hit Screen")

        if self.rect.right + self.dx > SCREEN_WIDTH:
            self.rect.x = 0

        # Check collision with platforms
        # for platform in platform_group:
        # if platform.mask.overlap(self.pepe_mask, (self.rect.x, self.rect.y)):
        #      print("Collide")

        # Check if the player goes of the bottom of the screen
        if self.rect.bottom + self.dy > SCREEN_HEIGHT:
            self.dy = 0
            self.vel_y = -20

        # Check if player has hit the scroll line
        if pepe.rect.top <= SCROLL_THRESHOLD:
            # If player is jumping
            if pepe.vel_y < 0:
                scroll = -pepe.dy
                platform_group.update(scroll)
                # pepe.rect.y += pepe.dy + scroll
        # print(scroll)

        # Update rectangle position
        self.rect.x += self.dx
        self.rect.y += self.dy + scroll

        # print(self.dy)

        # if self.pepe_mask.overlap(platform.mask, (self.rect.x, self.rect.y)):
        #    print("Collide")
        return scroll

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


def platform_generation(platform):
    pass


# Platform Instance
platform_group = pygame.sprite.Group()

# create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100)
platform_group.add(platform)


def collide(platform_group, platform):
    if pygame.sprite.spritecollide(pepe, platform_group, False, pygame.sprite.collide_mask):
        # check if player is above rectangle
        # print(platform.rect.centery)
        if pepe.rect.bottom > platform.rect.centery:
            if pepe.vel_y > 0:
                # I don't think I need the below line

                # Make pepe bounce
                pepe.dy = 0
                pepe.vel_y = -20
            # pepe.rect.bottom = platform.rect.top

            # print('collide')


while run:

    # Set Frame Rate
    clock.tick(FPS)

    platform_generation(platform)

    # Run move method
    scroll = pepe.move()

    # draw background
    bg_scroll += scroll
    if bg_scroll >= 600:
        bg_scroll = 0
    draw_background(bg_scroll)

    pygame.draw.line(screen, WHITE, (0, SCROLL_THRESHOLD), (SCREEN_WIDTH, SCROLL_THRESHOLD))

    if len(platform_group) < MAX_PLATFORMS:
        p_w = random.randint(40, 60)
        p_x = random.randint(0, SCREEN_WIDTH - p_w)
        print(p_x)
        p_y = platform.rect.y - random.randint(50, 100)
        platform = Platform(p_x, p_y, p_w)
        # print(platform.rect.y)
        # print(p_y)
        platform_group.add(platform)

    # print(len(platform_group))

    # Draw Sprites
    platform_group.draw(screen)
    pepe.draw()

    # update platforms
    platform_group.update(scroll)

    # Check for collisions
    collide(platform_group, platform)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update Display
    pygame.display.update()

pygame.quit()
