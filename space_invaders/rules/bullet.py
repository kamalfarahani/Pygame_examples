import pygame
import constants

from typing import List, Tuple
from rules import GameRule
from state.gamestate import GameState
from state.bullet import Bullet


class PlayerBulletMoveRule(GameRule):
    def __init__(self, min_height: int, max_height: int) -> None:
        self.min_height = min_height
        self.max_height = max_height

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player_bullets = state.player.bullets
        velocity = constants.PLAYER_BULLET_VELOCITY
        
        new_bullets = list(filter(
            lambda b: self.min_height < b.y < self.max_height,
            map(
                lambda b: b._replace(y=b.y - velocity),
                player_bullets
            )
        ))

        return state._replace(
            player=state.player._replace(
                bullets=new_bullets
            )
        )