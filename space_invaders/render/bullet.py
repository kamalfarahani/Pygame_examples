import pygame
import constants



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, img_path: str) -> None:
        super().__init__()
        
        self.x = x
        self.y = y

        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class GreenBullet(Bullet):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, constants.GREEN_LASER_IMG_PATH)


class RedBullet(Bullet):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, constants.RED_LASER_IMG_PATH)