import pygame
import constants
import render.portal
from typing import List, Callable, Union
from rules import GameRule
from state.gamestate import GameState
from state.bullet import Bullet
from state.general import Direction
from state.player import AnimationState


class BulletShootRule(GameRule):
    def __init__(self, horizontal_velocity: float, range: float):
        self.horizontal_velocity = horizontal_velocity
        self.range = range
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                bullets = state.bullets
                player = state.player
                horizontal_velocity = self.horizontal_velocity if player.direction == Direction.RIGHT else -self.horizontal_velocity
                start_position = player.position + pygame.math.Vector2(5, -20)
                new_bullet = Bullet(
                    position=start_position,
                    start_position=start_position,
                    velocity=pygame.math.Vector2(horizontal_velocity, 0),
                    direction=player.direction,
                    range=self.range
                )

                new_bullets = bullets + [new_bullet]
                return state._replace(
                    bullets=new_bullets,
                    player=player._replace(
                        animation_index=0,
                        animation_state=AnimationState.ATTACKING
                    )
                )
        
        return state


class BulletDestroyRule(GameRule):
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        bullets = state.bullets
        new_bullets = list(filter(
            lambda b: pygame.math.Vector2.magnitude(b.position - b.start_position) < b.range,
            bullets
        ))

        return state._replace(
            bullets=new_bullets
        )