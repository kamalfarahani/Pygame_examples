from typing import NamedTuple, List

from state.bullet import Bullet


class Player(NamedTuple):
    x: int
    y: int
    velocity: int
    score: int
    lives: int
    bullets: List[Bullet]