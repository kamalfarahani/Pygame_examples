import pygame
import constants
from typing import List
from rules import GameRule
from state.gamestate import GameState
from rules.animate import Animate


class RubyMakerAnimateRule(GameRule):
    def __init__(self) -> None:
        self.animate = Animate(len(constants.RUBY_ANIMATION_IMAGES_PATHS))
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        return state._replace(
            ruby_maker=self.animate(state.ruby_maker)
        )