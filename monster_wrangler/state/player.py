from typing import NamedTuple


class Player(NamedTuple):
    score: int
    lives: int
    warps: int
    x: int
    y: int
    velocity: int