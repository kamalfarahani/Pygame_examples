from typing import NamedTuple
from enum import Enum


class Color(Enum):
    GREEN = 0
    BLUE = 1
    YELLOW = 2
    PURPLE = 3


class Monster(NamedTuple):
    color: Color
    x: int
    y: int
    velocity_x: int
    velocity_y: int