import pygame
import constants
from typing import List
from rules import GameRule
from state.gamestate import GameState


class RubyMakerAnimateRule(GameRule):
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        ruby_maker = state.ruby_maker
        new_animation_index = (ruby_maker.animation_index + 1) % len(constants.RUBY_ANIMATION_IMAGES_PATHS)
        
        return state._replace(
            ruby_maker=ruby_maker._replace(
                animation_index=new_animation_index
            )
        )