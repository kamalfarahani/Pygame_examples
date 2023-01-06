from typing import NamedTuple, List

from state.player import Player
from state.monster import Monster, Color


class GameState(NamedTuple):
    player: Player
    monsters: List[Monster]
    round: int
    round_time: int
    catch_type: Color