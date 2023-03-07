import pygame
import constants
from typing import List, Union, Any
from rules import GameRule
from state.gamestate import GameState
from state.accelerable import Accelerable
from rules.animate import Animate


def map_state(fn, state: GameState) -> GameState:
    result = state
    for field in result._fields:
        entity = getattr(state, field)
        new_entity = fn(entity)
        result = result._replace(**{ field: new_entity })

    return result 


class GravityRule(GameRule):
    def __init__(self, gravity_constant: float) -> None:
        self.gravity_constant = gravity_constant

    def apply_gravity(self, entity: Union[Any, Accelerable, List]) -> Union[Any, Accelerable, List]:
        if isinstance(entity, List):
            return [self.apply_gravity(x) for x in entity]
        elif hasattr(entity, 'acceleration'):
            acc = entity.acceleration
            new_acc = pygame.math.Vector2(acc[0], self.gravity_constant)
            return entity._replace(
                acceleration=new_acc
            )

        return entity
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        return map_state(self.apply_gravity, state)


class AccelerationRule(GameRule):
    def apply_acceleration(self, entity: Union[Any, Accelerable, List]) -> Union[Any, Accelerable, List]:
        if isinstance(entity, List):
            return [self.apply_acceleration(x) for x in entity]
        elif hasattr(entity, 'acceleration') and hasattr(entity, 'velocity') :
            acc = entity.acceleration
            velocity = entity.velocity
            new_velocity = velocity + acc
            return entity._replace(
                velocity=new_velocity
            )

        return entity

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        return map_state(self.apply_acceleration, state)


class VelocityRule(GameRule):
    def apply_velocity(self, entity: Union[Any, Accelerable, List]) -> Union[Any, Accelerable, List]:
        if isinstance(entity, List):
            return [self.apply_velocity(x) for x in entity]
        elif hasattr(entity, 'velocity') and hasattr(entity, 'position'):
            velocity = entity.velocity
            position = entity.position
            new_position = position + velocity
            return entity._replace(
                position=new_position
            )

        return entity

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        return map_state(self.apply_velocity, state)

