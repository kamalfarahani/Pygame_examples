import pygame
from typing import NamedTuple
from state.general import Direction

class Bullet(NamedTuple):
    position: pygame.math.Vector2
    start_position: pygame.math.Vector2
    velocity: pygame.math.Vector2
    direction: Direction
    range: float