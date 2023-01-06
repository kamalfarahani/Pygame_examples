import pygame
from typing import Callable, Tuple, List, Optional

import constants
from state.gamestate import GameState
from render.monster import Monster
from render.player import Player


RenderFunc = Callable[[GameState], Tuple[pygame.Surface, pygame.Rect]]

def monsters_player_collide(state: GameState) -> Optional[Monster]:
        monsters = [ Monster(m.x, m.y, m.color) for m in state.monsters ]
        player = Player(state.player.x, state.player.y)
        monsters_group = pygame.sprite.Group(*monsters)

        return pygame.sprite.spritecollideany(player, monsters_group)


class Renderer:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def get_blit_funcs(self) -> List[RenderFunc]:
        return [
            self.score,
            self.lives,
            self.current_round,
            self.current_catch,
            self.current_catch_monster,
            self.round_time,
            self.warps,
            self.player
        ]
    
    def score(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.SCORE_STR}: {state.player.score}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topleft = (10, 10)

        return (text, rect)
    
    def lives(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.LIVES_STR}: {state.player.lives}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topleft = (10, 40)

        return (text, rect)
    
    def current_round(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.CURRENT_ROUND_STR}: {state.round}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topleft = (10, 70)

        return (text, rect)
    
    def current_catch(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.CURRENT_CATCH_STR}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.centerx = constants.WINDOW_WIDTH // 2
        rect.y = 10

        return (text, rect)
    
    def current_catch_monster(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        color = state.catch_type
        monster = Monster(x=constants.WINDOW_WIDTH // 2, y=80, color=color)
        
        return monster.image, monster.rect
    
    def round_time(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.ROUND_TIME_STR}: {state.round_time}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topright = (constants.WINDOW_WIDTH - 10, 10)

        return (text, rect)
    
    def warps(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.WARPS_STR}: {state.player.warps}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topright = (constants.WINDOW_WIDTH - 10, 40)

        return (text, rect)
    
    def player(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        player = Player(state.player.x, state.player.y)
        
        return (player.image, player.rect)
    
    def gameover(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.GAME_OVER_STR}  {constants.SCORE_STR}: {state.player.score}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.centerx = constants.WINDOW_WIDTH // 2
        rect.centery = constants.WINDOW_HEIGHT // 2

        return (text, rect)

    def render_monsters(self, display: pygame.Surface, state: GameState) -> None:
        monsters = [ Monster(m.x, m.y, m.color) for m in state.monsters ]
        monsters_group = pygame.sprite.Group(*monsters)
        monsters_group.draw(display)

    def render(self, display: pygame.Surface, state: GameState) -> None:
        display.fill(constants.BLACK)
        pygame.draw.line(
            surface=display,
            color=constants.ORANGE,
            start_pos=(0, constants.TOP_MARGIN),
            end_pos=(constants.WINDOW_WIDTH, constants.TOP_MARGIN)
        )

        pygame.draw.line(
            surface=display,
            color=constants.ORANGE,
            start_pos=(0, constants.WINDOW_HEIGHT - constants.BOTTOM_MARGIN),
            end_pos=(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT - constants.BOTTOM_MARGIN)
        )
        
        self.render_monsters(display, state)
        self.blit(display, state)
    
    def blit(self, display: pygame.Surface, state: GameState) -> None:
        for render_func in self.get_blit_funcs():
            display.blit(*render_func(state))
    
    def blit_gameover(self, display: pygame.Surface, state: GameState) -> None:
        display.fill(constants.BLACK)
        display.blit(*self.gameover(state))