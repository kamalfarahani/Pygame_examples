import pygame
import constants


class Alien(pygame.sprite.Sprite):

    def __init__(self, x: int, y: int) -> None:
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.image.load(constants.ALIEN_IMG_PATH)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y