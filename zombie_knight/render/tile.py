import pygame
import constants


TILE_DIM = (constants.TILE_SIZE, constants.TILE_SIZE)

class BaseTile(pygame.sprite.Sprite):
    def __init__(self, top_left_x: int, top_left_y: int, img_path: str) -> None:
        super().__init__()
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.image = pygame.transform.scale(
            pygame.image.load(img_path),
            TILE_DIM
        )

        self.rect = self.image.get_rect()
        self.rect.topleft = (top_left_x, top_left_y)


class TileOne(BaseTile):
    def __init__(self, top_left_x: int, top_left_y: int) -> None:
        super().__init__(top_left_x, top_left_y, constants.TILE_ONE_IMG_PATH)


class TileTwo(BaseTile):
    def __init__(self, top_left_x: int, top_left_y: int) -> None:
        super().__init__(top_left_x, top_left_y, constants.TILE_TWO_IMG_PATH)


class TileThree(BaseTile):
    def __init__(self, top_left_x: int, top_left_y: int) -> None:
        super().__init__(top_left_x, top_left_y, constants.TILE_THREE_IMG_PATH)


class TileFour(BaseTile):
    def __init__(self, top_left_x: int, top_left_y: int) -> None:
        super().__init__(top_left_x, top_left_y, constants.TILE_FOUR_IMG_PATH)

class TileFive(BaseTile):
    def __init__(self, top_left_x: int, top_left_y: int) -> None:
        super().__init__(top_left_x, top_left_y, constants.TILE_FIVE_IMG_PATH)