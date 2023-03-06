import pygame
import state.animatable
from pathlib import PosixPath
from typing import Tuple


class Animatable(pygame.sprite.Sprite):
    def __init__(
            self,
            animatable_state: state.animatable.Animatable,
            animation_images_paths: PosixPath,
            size: Tuple[int, int] 
        ) -> None:
        super().__init__()
        img_index = animatable_state.animation_index
        self.image = pygame.transform.scale(
            pygame.image.load(animation_images_paths[img_index]),
            size
        )
