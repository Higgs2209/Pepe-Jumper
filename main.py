from utils import resource_path
import pygame

# initialize pygame
pygame.init()

# Game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Define Colours
WHITE = (255, 255, 255)

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


class Player():
    def __init__(self, x, y):
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
        self.flip = None

    def move(self):

        # reset the variables
        dx = 0
        dy = 0

        # Process Keyboard events
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.direction = -1
            self.flip = False
            dx -= self.movement_speed + self.momentum

            if self.momentum < 5:
                self.momentum += 0.5

        elif key[pygame.K_d]:
            self.direction = 1
            self.flip = True
            dx += self.movement_speed + self.momentum

            if self.momentum < 5:
                self.momentum += 0.5

        else:
            # if no keys are pressed, gradually lower the momentum
            if self.momentum > 0:
                dx += (self.movement_speed * self.direction) + (self.momentum * self.direction)
                self.momentum -= 0.5

        # Ensure player stays within the screen
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(self.image, (self.rect.x - 12, self.rect.y - 5))
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        # Draw Mask
        # olist = self.pepe_mask.outline()
        # pygame.draw.lines(screen, (255, 0, 0), 1, olist)


# Game Loop
run = True

# call player class
pepe = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

while run:

    # Set Frame Rate
    clock.tick(FPS)

    # Run move method
    pepe.move()

    # Draw Background
    screen.blit(bg_image, (0, 0))

    # Draw Sprites
    pepe.draw()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update Display
    pygame.display.update()

pygame.quit()
