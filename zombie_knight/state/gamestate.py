from typing import NamedTuple, List

from state.player import Player
from state.zombie import Zombie
from state.tilemap import TileMap
from state.rubymaker import RubyMaker


class GameState(NamedTuple):
    player: Player
    ruby_maker: RubyMaker
    #zombies: List[Zombie]
    tile_map: TileMap
    gameover: bool = False