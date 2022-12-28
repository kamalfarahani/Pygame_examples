from ctypes import pointer
from numpy import disp
import pygame
from typing import Callable, List, Tuple

import constants
from gamestate import GameState
from player import Direction


RenderFunc = Callable[[GameState], Tuple[pygame.Surface, pygame.Rect]]

class Renderer:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def get_blit_funcs(self) -> List[RenderFunc]:
        return [
            self.points,
            self.score,
            self.title,
            self.eaten,
            self.lives,
            self.boost,
            self.dog,
            self.burger
        ]

    def points(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.PONTS_STR} {state.burger.points}',
            True ,
            constants.ORANGE)
    
        rect = text.get_rect()
        rect.topleft = (10, 10)

        return (text, rect)

    def score(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.SCORE_STR} {state.player.score}',
            True,
            constants.ORANGE
        )
        
        rect = text.get_rect()
        rect.topleft = (10, 50)

        return (text, rect)
    
    def title(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.TITLE_STR}',
            True,
            constants.ORANGE
        )
        
        rect = text.get_rect()
        rect.centerx = constants.WINDOW_WIDTH // 2    
        rect.y = 10

        return (text, rect)
    
    def eaten(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.EATEN_STR} : {state.player.burgers_eaten}',
            True,
            constants.ORANGE
        )
        
        rect = text.get_rect()
        rect.centerx = constants.WINDOW_WIDTH // 2
        rect.y = 50
        
        return (text, rect)
    
    def lives(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.LIVES_STR} : {state.player.lives}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topright = (constants.WINDOW_WIDTH - 10, 10)
        
        return (text, rect)
    
    def boost(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.BOOST_SRT} {state.player.boost_level}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topright = (constants.WINDOW_WIDTH - 10, 50)

        return (text, rect)
    
    def gameover(self, state: GameState):
        text = self.font.render(
            constants.GAME_OVER_STR,
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.centerx = constants.WINDOW_WIDTH // 2
        rect.centery = constants.WINDOW_HEIGHT // 2

        return (text, rect)
    
    def dog(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        img = (
            pygame.image.load(constants.RIGHT_DOG_IMG_PATH) 
            if state.player.direction == Direction.RIGHT 
            else pygame.image.load(constants.LEFT_DOG_IMG_PATH)
        )

        rect = img.get_rect()
        rect.centerx = state.player.x
        rect.centery = state.player.y
        self.dog_rect = rect

        return (img, rect)
    
    def burger(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        img = pygame.image.load(constants.BURGER_IMG_PATH)
        rect = img.get_rect()
        rect.centerx = state.burger.x
        rect.centery = state.burger.y
        self.burger_rect = rect

        return (img, rect)
    
    def render(self, display: pygame.Surface, state: GameState) -> None:
        display.fill(constants.BLACK)
        pygame.draw.line(
            surface=display,
            color=constants.ORANGE,
            start_pos=(0, 100),
            end_pos=(constants.WINDOW_WIDTH, 100)
        )
        self.blit(display, state)
    
    def blit(self, display: pygame.Surface, state: GameState) -> None:
        for render_func in self.get_blit_funcs():
            display.blit(*render_func(state))
    
    def blit_gameover(self, display: pygame.Surface, state: GameState) -> None:
        display.blit(*self.gameover(state))

    def dog_burger_collision_detector(self) -> bool:
        return self.dog_rect.colliderect(self.burger_rect)