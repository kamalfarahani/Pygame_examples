from dataclasses import dataclass

from clown import Clown
from player import Player


@dataclass
class GameState:
    clown: Clown
    player: Player