from dataclasses import dataclass
from typing import List

@dataclass
class Position:
    x: int
    y: int


@dataclass
class Snake:
    size: int
    head_position: Position
    tail: List[Position]
    dx: int = 0
    dy: int = 0