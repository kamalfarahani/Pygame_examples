import pygame
import constants
import state.portal
import render.animatable
from pathlib import PosixPath
from typing import List

green_portal_images = [
    pygame.transform.scale(
        pygame.image.load(path),
        (constants.PORTAL_SIZE, constants.PORTAL_SIZE)
    )
    for path in constants.GREEN_PORTAL_ANIMATION_IMAGES_PATHS
]

purple_portal_images = [
    pygame.transform.scale(
        pygame.image.load(path),
        (constants.PORTAL_SIZE, constants.PORTAL_SIZE)
    )
    for path in constants.PURPLE_PORTAL_ANIMATION_IMAGES_PATHS
]


class BasePortal(render.animatable.Animatable):
    def __init__(self, portal_state: state.portal.BasePortal, animation_images: List[pygame.Surface]) -> None:
        super().__init__(
            portal_state,
            animation_images,
        )
        
        self.rect = self.image.get_rect()
        self.rect.center = (portal_state.x, portal_state.y)


class GreenPortal(BasePortal):
    def __init__(self, portal_state: state.portal.GreenPortal) -> None:
        super().__init__(
            portal_state,
            green_portal_images,
        )


class PurplePortal(BasePortal):
    def __init__(self, portal_state: state.portal.GreenPortal) -> None:
        super().__init__(
            portal_state,
            purple_portal_images,
        )