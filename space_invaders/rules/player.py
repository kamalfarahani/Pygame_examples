import pygame
import constants

from typing import List, Tuple
from rules import GameRule
from state.gamestate import GameState
from state.bullet import Bullet


class PlayerMoveRule(GameRule):
    def __init__(self, min_width: int, max_width: int) -> None:
        self.min_width = min_width
        self.max_width = max_width
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player
        velocity = player.velocity

        movements = {
            pygame.K_LEFT: (-velocity, 0),
            pygame.K_RIGHT: (velocity, 0)
        }

        def get_dx_dy() -> Tuple[int]:
            for key in movements:
                if pygame.key.get_pressed()[key]:
                    return movements[key]
            
            return (0, 0)
        
        dx, _ = get_dx_dy()

        new_x = player.x + dx if self.min_width <= player.x + dx <= self.max_width else player.x

        return state._replace(
            player=player._replace(x=new_x)
        )

class PlayerShootRule(GameRule):
    def __init__(self, fire_sound: pygame.mixer.Sound) -> None:
        self.fire_sound = fire_sound
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player

        is_space_pressed = any([ e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE for e in events ])
        if (not is_space_pressed) or len(player.bullets) >= constants.MAX_PLAYER_BULLETS:
            return state
        

        self.fire_sound.play()
        new_bullet = Bullet(x=player.x, y=player.y + 30)
        return state._replace(
            player=player._replace(bullets=player.bullets + [new_bullet])
        )
        
