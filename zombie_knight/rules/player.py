import pygame
import constants
import render.tile
from typing import List, Callable
from rules import GameRule
from state.gamestate import GameState
from state.general import Direction
from state.player import AnimationState
from rules.animate import Animate


class PlayerAnimationRule(GameRule):
    def __init__(self) -> None:
        self.animation_length = len(constants.PLAYER_IDLE_RIGHT_ANIMATION_PATHS)
        self.animate = Animate(self.animation_length)
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player
        
        if state.player.animation_state not in {AnimationState.RUNNING, AnimationState.IDLE}:
            if state.player.animation_index == self.animation_length - 1:
                return state._replace(
                    player=state.player._replace(
                        animation_state=AnimationState.IDLE
                    )
                )
        
        return state._replace(
            player=self.animate(player)
        )


class PlayerMoveRule(GameRule):
    def __init__(
            self,
            horizontal_acceleration: float,
            horizontal_friction: float
        ) -> None:
        self.horizontal_acceleration = horizontal_acceleration
        self.horizontal_friction = horizontal_friction
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player
        velocity = player.velocity

        movements = {
            pygame.K_LEFT: -self.horizontal_acceleration,
            pygame.K_RIGHT: self.horizontal_acceleration
        }

        def get_horizontal_acceleration():
            for key in movements:
                if pygame.key.get_pressed()[key]:
                    return movements[key]
            return 0
        
        new_horizontal_acc = get_horizontal_acceleration() - self.horizontal_friction * velocity.x
        new_acc = pygame.math.Vector2(new_horizontal_acc, player.acceleration.y)

        if abs(get_horizontal_acceleration()) > 0:
            new_direction = Direction.RIGHT if new_horizontal_acc > 0 else Direction.LEFT
            return state._replace(
                player=player._replace(
                    acceleration=new_acc,
                    direction=new_direction,
                    animation_state=AnimationState.RUNNING
                )
            )
        else:
            new_animation_state = AnimationState.IDLE if player.animation_state == AnimationState.RUNNING else player.animation_state
            return state._replace(
                player=player._replace(
                    acceleration=new_acc,
                    animation_state=new_animation_state
                )
            )

        

class PlayerJumpRule(GameRule):
    def __init__(
            self,
            jump_speed: float,
            get_collided_tiles: Callable[[GameState], List[render.tile.BaseTile]]
        ) -> None:
        self.jump_speed = jump_speed
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player = state.player
                return state._replace(
                    player=player._replace(
                        velocity=pygame.math.Vector2(player.velocity.x, self.jump_speed),
                        animation_index=0,
                        animation_state=AnimationState.JUMPING
                    )
                )
        
        return state