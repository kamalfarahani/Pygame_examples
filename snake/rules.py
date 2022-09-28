import random
import re
from turtle import width
import pygame
import constants

from typing import Callable, List
from dataclasses import replace

from gamestate import GameState
from snake import Position


GameRule = Callable[[GameState, List[pygame.event.Event]], GameState]


def snake_dx_dy_rule(gamestate: GameState, events: List[pygame.event.Event]) -> GameState:
    snake = gamestate.snake
    moving_unit = snake.size
    halat = {
        pygame.K_LEFT: (-moving_unit, 0),
        pygame.K_RIGHT: (moving_unit, 0),
        pygame.K_DOWN: (0, moving_unit),
        pygame.K_UP: (0, -moving_unit)
    }

    new_dx, new_dy = snake.dx, snake.dy
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key in halat:
                new_dx, new_dy = halat[event.key]
    
    return replace(
        gamestate,
        snake=replace(
            snake,
            dx=new_dx,
            dy=new_dy
        )
    )


def snake_move_rule(gamestate: GameState, events: List[pygame.event.Event]) -> GameState:
    snake = gamestate.snake
    new_head_position = Position(
        x=snake.head_position.x + snake.dx,
        y=snake.head_position.y + snake.dy
    )
    
    new_tail = ([snake.head_position] + snake.tail[:-1]
                if len(snake.tail) > 0
                else [])
    
    return replace(
        gamestate,
        snake=replace(
            snake,
            head_position=new_head_position,
            tail=new_tail
        )
    )


class AppleCollideRule(GameRule):
    def __init__(
        self,
        apple_snake_collision_detector: Callable[[], bool],
        sound: pygame.mixer.Sound,
        max_width: int,
        max_height: int
    ) -> None:
        self.apple_snake_collision_detector = apple_snake_collision_detector
        self.sound = sound
        self.max_width = max_width
        self.max_height = max_height

    def __call__(self, gamestate: GameState, events: List[pygame.event.Event]) -> GameState:
        if not self.apple_snake_collision_detector():
            return gamestate
        
        self.sound.play()
        snake = gamestate.snake
        new_snake = replace(
            snake,
            tail=[snake.head_position] + snake.tail
        )

        apple_size = gamestate.snake.size
        new_apple_position = Position(
            random.randint(apple_size, self.max_width - apple_size),
            random.randint(apple_size, self.max_height - apple_size)
        )
        
        return replace(
            gamestate,
            score=gamestate.score + 1,
            snake=new_snake,
            apple_position=new_apple_position
        )
