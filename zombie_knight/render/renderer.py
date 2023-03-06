import pygame
from typing import Callable, Tuple, List, Dict, Optional

import constants
import render.tile
import state.tilemap
from state.gamestate import GameState
from render.rubymaker import RubyMaker


RenderFunc = Callable[[GameState], Tuple[pygame.Surface, pygame.Rect]]


state_tile_to_render_tile = {
    state.tilemap.TileOne: render.tile.TileOne,
    state.tilemap.TileTwo: render.tile.TileTwo,
    state.tilemap.TileThree: render.tile.TileThree,
    state.tilemap.TileFour: render.tile.TileFour,
    state.tilemap.TileFive: render.tile.TileFive
}


class Renderer:
    def __init__(self) -> None:
        self.background_img = pygame.transform.scale(
            pygame.image.load(constants.BACKGROUND_IMG_PATH),
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT)
        )

        background_rect = self.background_img.get_rect()
        background_rect.topleft = (0, 0)
        self.background_rect = background_rect

    def get_blit_funcs(self) -> List[RenderFunc]:
        return [self.ruby_maker]
    
    def ruby_maker(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        ruby_maker_sprite = RubyMaker(state.ruby_maker)
        
        return (ruby_maker_sprite.image, ruby_maker_sprite.rect)
    
    def render_tile_map(self, display: pygame.Surface, state: GameState) -> None:
        tile_map = state.tile_map
        tile_sprites = [
            state_tile_to_render_tile[type(tile)](tile.x, tile.y)
            for tile in tile_map
        ]

        tile_group = pygame.sprite.Group(*tile_sprites)
        tile_group.draw(display)


    def render(self, display: pygame.Surface, state: GameState) -> None:
        display.blit(self.background_img, self.background_rect)
        self.render_tile_map(display, state)
        self.blit(display, state)
    
    def blit(self, display: pygame.Surface, state: GameState) -> None:
        for render_func in self.get_blit_funcs():
            display.blit(*render_func(state))
    
    def blit_gameover(self, display: pygame.Surface, state: GameState) -> None:
        display.fill(constants.BLACK)
        display.blit(*self.gameover(state))