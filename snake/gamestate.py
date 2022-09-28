from dataclasses import dataclass
from snake import Snake, Position


@dataclass
class GameState:
    score: int
    snake: Snake
    apple_position: Position