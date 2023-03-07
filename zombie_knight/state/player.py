import pygame
from typing import NamedTuple
from enum import Enum
from state.general import Direction


class AnimationState:
    IDLE = 1
    RUNNING = 2
    JUMPING = 3
    ATTACKING = 4


class Player(NamedTuple):
    lives: int
    score: int
    animation_index: int
    animation_state: AnimationState
    direction: Direction
    position: pygame.math.Vector2
    velocity: pygame.math.Vector2
    acceleration: pygame.math.Vector2