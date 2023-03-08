import pygame
import constants
import render.tile
from typing import List, Callable
from rules import GameRule
from state.gamestate import GameState



class PlatformCollideRule(GameRule):
    def __init__(self, get_collided_tiles: Callable[[GameState], List[render.tile.BaseTile]]) -> None:
        self.get_colidded_tiles = get_collided_tiles
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player 
        tile_sprits = self.get_colidded_tiles(state)
        if len(tile_sprits)  == 0:
            return state
        
        tile_sprite = tile_sprits[0]
        y_top = tile_sprite.rect.top
        y_bottom = tile_sprite.rect.bottom
        if player.velocity.y > 0 and abs(player.position.y - y_top) < 50:
            new_player = player._replace(
                position=pygame.math.Vector2(player.position.x, y_top + 3),
                velocity=pygame.math.Vector2(player.velocity.x, 0)
            )

            return state._replace(
                player=new_player
            )
        elif player.velocity.y < 0:
            return state._replace(
                player=player._replace(
                    position=pygame.math.Vector2(player.position.x, y_bottom + constants.PLAYER_SIZE + 3),
                    velocity=pygame.math.Vector2(player.velocity.x, 0)
                )
            )

        return state