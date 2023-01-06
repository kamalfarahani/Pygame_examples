import pygame

import constants
from state.monster import Color


color_to_img = {
    Color.BLUE: constants.BLUE_MONSTER_IMG_PATH,
    Color.GREEN: constants.GREEN_MONSTER_IMG_PATH,
    Color.PURPLE: constants.PURPLE_MONSTER_IMG_PATH,
    Color.YELLOW: constants.YELLOW_MONSTER_IMG_PATH
}

class Monster(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: Color) -> None:
        super().__init__()

        self.image = pygame.image.load(color_to_img[color])
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y