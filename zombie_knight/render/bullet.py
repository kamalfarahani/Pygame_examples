import pygame
import constants
import state.bullet
from state.general import Direction


right_bullet_img = pygame.transform.scale(
    pygame.image.load(constants.BULLET_PATH),
    (constants.BULLET_SIZE, constants.BULLET_SIZE)
)

left_bullet_img = pygame.transform.flip(right_bullet_img, True, False)

dir_to_img = {
    Direction.LEFT: left_bullet_img,
    Direction.RIGHT: right_bullet_img
}

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_state: state.bullet.Bullet) -> None:
        super().__init__()
        self.image = dir_to_img[bullet_state.direction]
        self.rect = self.image.get_rect()
        self.rect.center = bullet_state.position
