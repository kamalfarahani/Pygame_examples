import pygame
import constants

from typing import List, Tuple
from rules import GameRule
from state.gamestate import GameState


class AliensMoveRule(GameRule):
    def __init__(self, min_width: int, max_width: int, min_height: int, max_height: int) -> None:
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        aliens = state.aliens
        velocity = state.aliens_velocity
        can_move_horizontally = all(
            map(
                lambda alien: self.min_width < alien.x + velocity < self.max_width,
                aliens
            )
        )

        if not can_move_horizontally:
            new_aliens = list(map(
                lambda alien: alien._replace(y=alien.y + abs(velocity)),
                aliens
            ))

            return state._replace(
                aliens_velocity = -velocity,
                aliens=new_aliens
            )
        else:
            new_aliens = list(map(
                lambda alien: alien._replace(x=alien.x + velocity),
                aliens
            ))

            return state._replace(
                aliens=new_aliens
            )
