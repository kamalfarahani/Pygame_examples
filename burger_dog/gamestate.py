from dataclasses import dataclass

from player import Player
from burger import Burger


@dataclass
class GameState:
    player: Player
    burger: Burger
