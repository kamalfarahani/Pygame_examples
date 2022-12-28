from os import stat
import random
import pygame

from dataclasses import replace
from typing import Callable, List

import constants
from player import Direction
from gamestate import GameState


GameRule = Callable[[GameState, List[pygame.event.Event]], GameState]


def create_new_burger_position(max_height: int):
    return random.randint(5, max_height - 5), -50


class BurgerMoveRule(GameRule):
    def __init__(self, max_height: int) -> None:
        self.max_height = max_height

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        burger = state.burger
        new_points = (self.max_height - burger.y)
        
        return replace(
            state,
            burger=replace(
                burger,
                y=burger.y + burger.velocity,
                points=new_points
            )
        )


class BurgerMissRule(GameRule):
    def __init__(self, max_width: int, max_height: int, sound: pygame.mixer.Sound) -> None:
        self.max_width = max_width
        self.max_height = max_height
        self.sound = sound
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        burger = state.burger
        player = state.player
        if burger.y < self.max_height:
            return state
        
        self.sound.play()
        new_x, new_y = create_new_burger_position(self.max_height)
        
        return replace(
            state,
            player=replace(
                player,
                lives=player.lives - 1
            ),
            burger=replace(
                burger,
                x=new_x,
                y=new_y
            )
        )
        

class DogMoveRule(GameRule):
    def __init__(self, min_width: int, max_width: int, min_height: int, max_height: int) -> None:
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player
        velocity = player.velocity
        movements = {
            pygame.K_DOWN: (0, velocity),
            pygame.K_UP: (0, -velocity),
            pygame.K_RIGHT: (velocity, 0),
            pygame.K_LEFT: (-velocity, 0)
        }

        def is_boosted():
            return pygame.key.get_pressed()[pygame.K_SPACE] and player.boost_level > 0

        def get_dx_dy():
            pressed_keys = pygame.key.get_pressed()
            for key in movements:
                if pressed_keys[key]:
                    dx, dy = movements[key]
                    if is_boosted():
                        return 2 * dx, 2 * dy
                    else:
                        return dx, dy
            return 0, 0 
        
        dx, dy = get_dx_dy()
        new_x = player.x + dx if self.min_width < player.x + dx < self.max_width else player.x
        new_y = player.y + dy if self.min_height < player.y + dy < self.max_height else player.y
        new_direction = Direction.RIGHT if dx > 0 else Direction.LEFT
        new_boost_level = player.boost_level if not is_boosted() else max(0, player.boost_level - 5)
        
        return replace(
            state,
            player=replace(
                player,
                x=new_x,
                y=new_y,
                direction=new_direction if dx != 0 else player.direction,
                boost_level=new_boost_level
            )
        )

class EatBurgerRule(GameRule):
    def __init__(
        self,
        max_height: int,
        sound: pygame.mixer.Sound,
        dog_burger_collision_detector: Callable[[], bool]
    ) -> None:
        self.max_height = max_height
        self.sound = sound
        self.dog_burger_collision_detector = dog_burger_collision_detector
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        if not self.dog_burger_collision_detector():
            return state
        
        self.sound.play()
        player = state.player
        burger = state.burger
        points = burger.points
        boost_points = 20
        new_burger_x, new_burger_y = create_new_burger_position(self.max_height)

        return replace(
            state,
            burger=replace(
                burger,
                x=new_burger_x,
                y=new_burger_y,
                velocity=burger.velocity + burger.acceleration
            ),
            player=replace(
                player,
                score=player.score + points,
                burgers_eaten=player.burgers_eaten + 1,
                boost_level=min(constants.INIT_BOOST_LEVEL, player.boost_level + boost_points)
            )
        )


