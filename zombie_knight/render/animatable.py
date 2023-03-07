import pygame
import state.animatable
from pathlib import PosixPath
from typing import Tuple, List


class Animatable(pygame.sprite.Sprite):
    def __init__(
            self,
            animatable_state: state.animatable.Animatable,
            animation_images: List[pygame.Surface]
        ) -> None:
        super().__init__()
        img_index = animatable_state.animation_index
        self.image = animation_images[img_index]
