from copyreg import dispatch_table
from lib2to3 import pygram
import pygame
import time

from collections import namedtuple

RGB = namedtuple('RGB', ['r', 'g', 'b'], defaults=[0, 0, 0])

BLACK = RGB(0,0,0)
WHITE = RGB(255, 255, 255)
RED = RGB(255, 0, 0)
GREEN = RGB(0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = RGB(255, 255, 0)
CYAN = RGB(0, 255, 255)
MAGENTA = RGB(255, 0, 255)



pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display_surface.fill(WHITE)
pygame.display.set_caption('Hello World')

pygame.draw.line(display_surface, RED, (0,0), (100, 100), 5)
pygame.draw.line(display_surface, GREEN, (100, 100), (200, 150), 2)
pygame.draw.circle(
    surface=display_surface,
    color=BLACK,
    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
    radius=200,
    width=2,
)


pygame.draw.circle(
    surface=display_surface,
    color=YELLOW,
    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
    radius=100,
    width=0,
)

pygame.draw.rect(
    surface=display_surface,
    color=CYAN,
    rect=(500, 10, 50, 50)
)


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()