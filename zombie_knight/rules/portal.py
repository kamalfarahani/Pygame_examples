import pygame
import constants
from typing import List
from rules import GameRule
from state.gamestate import GameState
from rules.animate import Animate


class PortalsAnimateRule(GameRule):
    def __init__(self) -> None:
        self.animate = Animate(len(constants.GREEN_PORTAL_ANIMATION_IMAGES_PATHS))
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        portals = state.portals
        return state._replace(
            portals=[self.animate(portal) for portal in portals]
        )