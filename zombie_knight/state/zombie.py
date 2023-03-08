import pygame
from typing import NamedTuple
from enum import Enum
from state.general import Direction


class Gender(Enum):
    MALE = 1
    FEMALE = 2

class Zombie(NamedTuple):
    position: pygame.Vector2
    velocity: pygame.Vector2
    acceleration: pygame.Vector2
    direction: Direction
    animation_index: int
    rise_time: int
    gender: Gender
    dead: bool
    catched: bool