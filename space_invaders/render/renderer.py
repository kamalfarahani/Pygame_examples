import pygame
from typing import Callable, Tuple, List, Dict, Optional

import constants
from state.gamestate import GameState
from render.player import Player
from render.alien import Alien
from render.bullet import RedBullet, GreenBullet


RenderFunc = Callable[[GameState], Tuple[pygame.Surface, pygame.Rect]]


def player_bullet_collide(state: GameState) -> Optional[GreenBullet]:
    aliens_bullets = pygame.sprite.Group(*[GreenBullet(x=b.x, y=b.y) for b in state.aliens_bullets])
    player = Player(x=state.player.x, y=state.player.y)
    return pygame.sprite.spritecollideany(player, aliens_bullets)


def alien_bullet_collide(state: GameState) -> Dict[RedBullet, Alien]:
    aliens_group = pygame.sprite.Group(*[Alien(a.x, a.y) for a in state.aliens])
    player_bullets_group = pygame.sprite.Group(*[RedBullet(b.x, b.y) for b in state.player.bullets])
    collide_dict = pygame.sprite.groupcollide(player_bullets_group, aliens_group, False, False)

    return collide_dict


class Renderer:
    def __init__(self, font: pygame.font.Font) -> None:
        self.font = font

    def get_blit_funcs(self) -> List[RenderFunc]:
        return [
            self.score,
            self.lives,
            self.current_round,
            self.player
        ]
    
    def score(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.SCORE_STR}: {state.player.score}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.centerx = constants.WINDOW_WIDTH // 2
        rect.top = 10

        return (text, rect)
    
    def lives(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.LIVES_STR}: {state.player.lives}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topright = (constants.WINDOW_WIDTH, 10)

        return (text, rect)
    
    def current_round(self, state: GameState) -> Tuple[pygame.Surface, pygame.Rect]:
        text = self.font.render(
            f'{constants.CURRENT_ROUND_STR}: {state.round}',
            True,
            constants.ORANGE
        )

        rect = text.get_rect()
        rect.topleft = (10, 10)

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

    def render_aliens(self, display: pygame.Surface, state: GameState) -> None:
        aliens = [ Alien(a.x, a.y) for a in state.aliens ]
        aliens_group = pygame.sprite.Group(*aliens)
        aliens_group.draw(display)
    

    def render_player_bullets(self, display: pygame.Surface, state: GameState) -> None:
        red_bullets = [RedBullet(x=b.x, y=b.y) for b in state.player.bullets]
        red_bullets_group = pygame.sprite.Group(*red_bullets)
        red_bullets_group.draw(display)
    
    def render_alien_bullets(self, display: pygame.Surface, state: GameState) -> None:
        green_bullets = [GreenBullet(x=b.x, y=b.y) for b in state.aliens_bullets]
        green_bullets_group = pygame.sprite.Group(*green_bullets)
        green_bullets_group.draw(display)

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
        
        self.render_aliens(display, state)
        self.render_player_bullets(display, state)
        self.render_alien_bullets(display, state)
        self.blit(display, state)
    
    def blit(self, display: pygame.Surface, state: GameState) -> None:
        for render_func in self.get_blit_funcs():
            display.blit(*render_func(state))
    
    def blit_gameover(self, display: pygame.Surface, state: GameState) -> None:
        display.fill(constants.BLACK)
        display.blit(*self.gameover(state))