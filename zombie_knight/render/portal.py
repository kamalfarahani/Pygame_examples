import pygame
import constants
import state.portal
import render.animatable
from pathlib import PosixPath
from typing import List


class BasePortal(render.animatable.Animatable):
    def __init__(self, portal_state: state.portal.BasePortal, animation_images_paths: List[PosixPath]) -> None:
        super().__init__(
            portal_state,
            animation_images_paths,
            (constants.PORTAL_SIZE, constants.PORTAL_SIZE)
        )
        
        self.rect = self.image.get_rect()
        self.rect.center = (portal_state.x, portal_state.y)


class GreenPortal(BasePortal):
    def __init__(self, portal_state: state.portal.GreenPortal) -> None:
        super().__init__(
            portal_state,
            constants.GREEN_PORTAL_ANIMATION_IMAGES_PATHS,
        )


class PurplePortal(BasePortal):
    def __init__(self, portal_state: state.portal.GreenPortal) -> None:
        super().__init__(
            portal_state,
            constants.PURPLE_PORTAL_ANIMATION_IMAGES_PATHS,
        )