import random
import dataclasses
import pygame
import constants

from gamestate import GameState
from clown import Clown
from typing import Callable, List


GameRule = Callable[[GameState, List[pygame.event.Event]], GameState]


def clown_move_rule(state: GameState, events=None) -> GameState:
    clown = state.clown
    new_clown = Clown(
        x=clown.x + clown.dx * clown.velocity,
        y=clown.y + clown.dy * clown.velocity,
        velocity=clown.velocity,
        dx=clown.dx,
        dy=clown.dy
    )


    return GameState(
        clown=new_clown,
        player=state.player
    )


class ClownBounceRule(GameRule):
    def __init__(self, max_x: int, max_y: int, min_x: int = 0, min_y: int = 0) -> None:
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
    
    def __call__(self, state: GameState, events=None) -> GameState:
        clown = state.clown
        dx, dy = clown.dx, clown.dy
        x, y = clown.x, clown.y

        new_dx = -dx  if not (self.min_x < x < self.max_x) else dx
        new_dy = -dy if not (self.min_y < y < self.max_y) else dy

        return GameState(
            clown=dataclasses.replace(clown, dx=new_dx, dy=new_dy),
            player=state.player
        )



class ClickClownRule(GameRule):
    def __init__(self, clown_rect, click_sound, miss_sound) -> None:
        self.clown_rect = clown_rect
        self.click_sound = click_sound
        self.miss_sound = miss_sound
    

    def __call__(self, state:GameState, events: List[pygame.event.Event]) -> GameState:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if self.clown_rect.collidepoint(mouse_x, mouse_y):
                    self.click_sound.play()
                    
                    new_state = dataclasses.replace(
                        state,
                        clown=dataclasses.replace(
                            state.clown,
                            velocity=state.clown.velocity + constants.CLOWN_ACCELERATION,
                            dx=random.choice([-1, 1]),
                            dy=random.choice([-1, 1])
                        ),
                        player=dataclasses.replace(
                            state.player,
                            score=state.player.score + 1
                        )
                    )

                    return new_state
                
                else:
                    self.miss_sound.play()
                    new_state = dataclasses.replace(
                        state,
                        player=dataclasses.replace(
                            state.player,
                            lives=state.player.lives - 1
                        )
                    )

                    return new_state
        
        return state
    