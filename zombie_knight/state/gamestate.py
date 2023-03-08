from typing import NamedTuple, List

from state.player import Player
from state.zombie import Zombie
from state.tilemap import TileMap
from state.rubymaker import RubyMaker
from state.portal import BasePortal
from state.bullet import Bullet


class GameState(NamedTuple):
    player: Player
    ruby_maker: RubyMaker
    bullets: List[Bullet]
    #zombies: List[Zombie]
    tile_map: TileMap
    portals: List[BasePortal]
    gameover: bool = False