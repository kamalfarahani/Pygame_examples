import pygame
import constants
from pathlib import PosixPath
from typing import List
from rules import GameRule
from state.gamestate import GameState
from state.animatable import Animatable


class Animate:
    def __init__(self, animation_size: int, speed: float=1.0) -> None:
        self.animation_size = animation_size
        self.speed = speed

    def __call__(self, entity: Animatable) -> Animatable:
        new_index = (entity.animation_index + 1) % self.animation_size 
        
        return entity._replace(
            animation_index=new_index
        )