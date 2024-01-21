import pygame

# Define Font
font_small = pygame.font.SysFont("Lucida Sans", 20)
font_small_bold = pygame.font.SysFont("Lucida Sans", 20, 3)
font_big = pygame.font.SysFont("Lucida Sans", 24)

# Drawing text
def draw_text(screen, text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))