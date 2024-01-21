import pygame
from draw_text import draw_text


def draw_panel(screen, score, font_size, colour, panel_colour):
    pygame.draw.rect(screen, panel_colour, (0, 0, 400, 30))
    pygame.draw.line(screen, colour, (0, 30), (400, 30), 2)
    draw_text(screen, f'SCORE: {score}', font_size, colour, 0, 0)
