import pygame

from typing import List
from rules import GameRule
from state.gamestate import GameState


class PlayerMoveRule(GameRule):
    def __init__(self, max_width: int, max_height: int) -> None:
        self.max_width = max_width
        self.max_height = max_height
        self.min_width = 0
        self.min_height = 0
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player
        velocity = player.velocity
        movements = {
            pygame.K_DOWN: (0, velocity),
            pygame.K_UP: (0, -velocity),
            pygame.K_RIGHT: (velocity, 0),
            pygame.K_LEFT: (-velocity, 0)
        }

        def get_dx_dy():
            pressed_keys = pygame.key.get_pressed()
            for key in movements:
                if pressed_keys[key]:
                    dx, dy = movements[key]
                    return dx, dy
            
            return 0, 0 
        
        dx, dy = get_dx_dy()
        new_x = player.x + dx if self.min_width < player.x + dx < self.max_width else player.x
        new_y = player.y + dy if self.min_height < player.y + dy < self.max_height else player.y

        return state._replace(
            player=player._replace(
                x=new_x,
                y=new_y
            )
        )