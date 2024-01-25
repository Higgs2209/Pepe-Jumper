import time
from utils import resource_path
import pygame
from platform import Platform
import random
from draw_text import draw_text, font_big, font_small, font_small_bold
from info_panel import draw_panel
import os
from spritesheet import SpriteSheet
from enemy import Enemy
from pygame import mixer
from apple import Apple
from collisions import Collide

# initialize pygame
mixer.init()
pygame.init()

# Game window dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Define Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL = (153, 217, 234)

# Game Variables
GRAVITY = 1
MAX_PLATFORMS = 15
SCROLL_THRESHOLD = 150

bg_scroll = 0

game_over = False

score = 0

fade_counter = 0

apple_generation = 0

apple_event = pygame.USEREVENT + 0
pygame.time.set_timer(apple_event, 25000)

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

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

# Bird Sprite Sheet
BIRD_SHEET_PATH = resource_path("assets/bird.png")
bird_sheet_img = pygame.image.load(BIRD_SHEET_PATH).convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)

# music
DEATH_MUSIC_RESOURCE_PATH = resource_path("assets/death.mp3")
JUMP_MUSIC_RESOURCE_PATH = resource_path("assets/jump.mp3")
MUSIC_RESOURCE_PATH = resource_path("assets/music.mp3")

# Background Music
pygame.mixer.music.load(MUSIC_RESOURCE_PATH)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1, 0.0)

# Sound Effects
jump_fx = pygame.mixer.Sound(JUMP_MUSIC_RESOURCE_PATH)
jump_fx.set_volume(0.7)
death_fx = pygame.mixer.Sound(DEATH_MUSIC_RESOURCE_PATH)
death_fx.set_volume(0.5)

# Apple Sprite Sheet import
APPLE_RESOURCE_PATH = resource_path("assets/Apple.png")
apple_sheet_img = pygame.image.load(APPLE_RESOURCE_PATH).convert_alpha()
apple_sheet = SpriteSheet(apple_sheet_img)


# Function to draw the background
def draw_background(bg_scroll):
    # Draw Background
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, -600 + bg_scroll))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.pepe_mask = None
        self.image = pygame.transform.scale(pepe_image, (45, 45))

        # Create the player rectangle
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

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

        # Create a mask
        self.pepe_mask = pygame.mask.from_surface(self.image)
        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))
        # pygame.draw.rect(screen, WHITE, self.rect, 2)

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


# Platform group
platform_group = pygame.sprite.Group()
# Enemy Group
enemy_group = pygame.sprite.Group()
# enemy = Enemy()

# Apple Group
apple_group = pygame.sprite.Group()

# create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
platform_group.add(platform)

# Initialize collision class
collision = Collide(pepe)




def apple_gen():
    if len(apple_group) == 0:
        apple = Apple(SCREEN_WIDTH, apple_sheet, 1.8)
        apple_group.add(apple)


while run:

    # Set Frame Rate
    clock.tick(FPS)

    if not game_over:

        platform_generation(platform)

        # Run move method
        scroll = pepe.move()

        # draw background
        bg_scroll += scroll
        if bg_scroll >= 600:
            bg_scroll = 0
        draw_background(bg_scroll)

        # pygame.draw.line(screen, WHITE, (0, SCROLL_THRESHOLD), (SCREEN_WIDTH, SCROLL_THRESHOLD))

        # Generate Platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            print(p_x)
            p_y = platform.rect.y - random.randint(50, 100)
            p_type = random.randint(1, 2)
            if p_type == 1 and score >= 150:
                p_moving = True
            else:
                p_moving = False

            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)

        # Generate Enemy's
        if len(enemy_group) == 0 and score >= 700:
            enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
            enemy_group.add(enemy)

        # update enemy
        enemy_group.update(scroll, SCREEN_WIDTH)

        # Draw Sprites
        platform_group.draw(screen)
        pepe.draw()
        enemy_group.draw(screen)
        apple_group.update(scroll, SCREEN_WIDTH, SCREEN_HEIGHT)
        apple_group.draw(screen)

        # Draw Panel
        draw_panel(screen, score, font_small, WHITE, PANEL)

        # update platforms
        platform_group.update(scroll)

        # Score
        if scroll > 0:
            score += scroll

        # draw line and High Score text at prior old score
        draw_text(screen, "HIGH SCORE", font_small_bold, BLACK, 0, score - high_score + SCROLL_THRESHOLD)
        pygame.draw.line(screen, BLACK, (0, score - high_score + SCROLL_THRESHOLD),
                         (SCREEN_WIDTH, score - high_score + SCROLL_THRESHOLD), 3)

        # Check for collisions
        collision.platform_collide(platform_group, platform, jump_fx)

        # Check game over
        if pepe.rect.top > SCREEN_HEIGHT:
            game_over = True
            death_fx.play()
        # Check collision with enemies
        enemy_bird_collision = collision.enemy_collide(enemy_group)
        if enemy_bird_collision:
            game_over = True
            death_fx.play()
            print("Test")

        # Apple Collision Detection
        apple_collision = collision.apple_collision(apple_group)
        if apple_collision:
            pepe.vel_y = -50


        # for event in pygame.event.get():


    else:
        # Fade effect
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y * 100, fade_counter, SCREEN_HEIGHT / 6))
                pygame.draw.rect(screen, BLACK,
                                 (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, SCREEN_HEIGHT / 6))
        else:
            draw_text(screen, 'Game Over', font_big, WHITE, 130, 200)
            draw_text(screen, f'SCORE:{score} ', font_big, WHITE, 130, 250)
            draw_text(screen, 'Press space to play again', font_big, WHITE, 40, 300)
            # Update high score
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # Reset Varibales
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0

                # Reset enemy
                enemy_group.empty()
                # Reposition Pepe
                pepe.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

                # Rest Platforms
                platform_group.empty()
                # create starting platform
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                platform_group.add(platform)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == apple_event:
            apple_gen()

    # Update Display
    pygame.display.update()

pygame.quit()
