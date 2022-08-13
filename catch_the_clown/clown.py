from dataclasses import dataclass


@dataclass
class Clown:
    x: int = 0
    y: int = 0
    velocity: float = 1
    dx: float = 1
    dy: float = 1