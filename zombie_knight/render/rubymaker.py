import pygame
import constants
import state.rubymaker
from render.animatable import Animatable


ruby_animation_images = [
    pygame.transform.scale(
        pygame.image.load(path),
        (constants.RUBY_SIZE, constants.RUBY_SIZE)
    )
    for path in constants.RUBY_ANIMATION_IMAGES_PATHS
] 

class RubyMaker(Animatable):
    def __init__(self, ruby_maker_state: state.rubymaker.RubyMaker) -> None:
        super().__init__(ruby_maker_state, ruby_animation_images)
        self.rect = self.image.get_rect()
        self.rect.center = (ruby_maker_state.x, ruby_maker_state.y)