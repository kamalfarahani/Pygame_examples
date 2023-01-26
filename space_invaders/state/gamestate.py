from typing import NamedTuple, List

from state.bullet import Bullet
from state.player import Player
from state.alien import Alien

class GameState(NamedTuple):
    player: Player
    aliens: List[Alien]
    aliens_bullets: List[Bullet]
    aliens_velocity: int
    round: int
    gameover: bool = False