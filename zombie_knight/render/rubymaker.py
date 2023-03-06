import pygame
import constants
import state.rubymaker


class RubyMaker(pygame.sprite.Sprite):
    def __init__(self, ruby_maker: state.rubymaker.RubyMaker) -> None:
        super().__init__()
        img_path = constants.RUBY_ANIMATION_IMAGES_PATHS[ruby_maker.animation_index]
        self.image = pygame.transform.scale(
            pygame.image.load(img_path),
            (constants.RUBY_SIZE, constants.RUBY_SIZE)
        )

        self.rect = self.image.get_rect()
        self.rect.center = (ruby_maker.x, ruby_maker.y)