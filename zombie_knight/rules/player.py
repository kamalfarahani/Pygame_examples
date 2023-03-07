import pygame
import constants
from typing import List
from rules import GameRule
from state.gamestate import GameState
from rules.animate import Animate


class PlayerAnimationRule(GameRule):
    def __init__(self) -> None:
        self.animate = Animate(len(constants.PLAYER_IDLE_RIGHT_ANIMATION_PATHS))
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        player = state.player
        
        return state._replace(
            player=self.animate(player)
        )