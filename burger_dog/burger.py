from dataclasses import dataclass


@dataclass
class Burger:
    x: int
    y: int
    velocity: int
    acceleration: int
    points: int = 0