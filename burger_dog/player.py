from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    RIGHT = 1
    LEFT = 2


@dataclass
class Player:
    x: int
    y: int
    direction: Direction
    score: int = 0
    burger_points: int = 0
    burgers_eaten: int = 0
    velocity: int = 0
    boost_level: int = 0
    lives: int = 0