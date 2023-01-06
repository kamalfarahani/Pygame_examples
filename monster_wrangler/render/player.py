import pygame

import constants


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()

        self.x = x
        self.y = y
        
        self.image = pygame.image.load(constants.KINIGHT_IMG_PATH)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y