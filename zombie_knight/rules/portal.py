import pygame
import constants
import render.portal
from typing import List, Callable, Union
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


class PortalCollideRule(GameRule):
    def __init__(
            self,
            get_collided_portal: Callable[[GameState], Union[render.portal.BasePortal, None]]
        ) -> None:
            self.get_collided_portal = get_collided_portal
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        collided_portal_sprite = self.get_collided_portal(state)
        if collided_portal_sprite is None:
            return state
         
        collided_portal = next(filter(
            lambda p: p.x == collided_portal_sprite.rect.centerx and p.y == collided_portal_sprite.rect.centery,
            state.portals
        ))
        
        out_portal = collided_portal.out_portal
        return state._replace(
            player=state.player._replace(
                position=pygame.math.Vector2(out_portal.x + 86, out_portal.y + 20)
            )
        )