import pygame
import constants

from typing import List
from rules import GameRule
from state.gamestate import GameState


class PlayerMoveRule(GameRule):
    def __init__(
        self,
        min_width: int, 
        min_height: int, 
        max_width: int, 
        max_height: int, 
        bottom_line: int) -> None:
        
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        self.bottom_line = bottom_line
    
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
        max_height = self.max_height if player.y > self.bottom_line else self.bottom_line
        new_x = player.x + dx if self.min_width < player.x + dx < self.max_width else player.x
        new_y = player.y + dy if self.min_height < player.y + dy < max_height else player.y

        return state._replace(
            player=player._replace(
                x=new_x,
                y=new_y
            )
        )


class WarpRule(GameRule):
    def __init__(self, warp_sound: pygame.mixer.Sound) -> None:
        self.warp_sound = warp_sound

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        if state.player.warps > 0:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.warp_sound.play()
                    return state._replace(
                        player=state.player._replace(
                            y=constants.WINDOW_HEIGHT - 20,
                            warps=state.player.warps - 1
                        )
                    )
                
        return state