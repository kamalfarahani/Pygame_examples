from dataclasses import dataclass


@dataclass
class Player:
    score: int = 0
    lives: int = 0