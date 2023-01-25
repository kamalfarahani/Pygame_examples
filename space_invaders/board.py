import random
import pygame
from typing import Callable, List

import constants
from state.gamestate import GameState
from state.player import Player
from state.alien import Alien
from render.renderer import Renderer, alien_bullet_collide
from rules.player import PlayerMoveRule, PlayerShootRule
from rules.bullet import PlayerBulletMoveRule
from rules.alien import AliensMoveRule
from rules.hit import AlienHitRule
from utils import create_aliens


Action = Callable[[], None]
EndCond = Callable[[], bool]



class Board:
    def __init__(self) -> None:
        self.window_width = constants.WINDOW_WIDTH
        self.window_height = constants.WINDOW_HEIGHT
        
        self.setup_gamestate()
        self.events = []
        
        self.display = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.font = pygame.font.Font(constants.FONT_PATH, constants.FONT_SIZE)
        self.renderer = Renderer(self.font)
        pygame.display.set_caption(constants.TITLE_STR)

        self.setup_sounds()
        self.setup_rules()
    
    def setup_gamestate(self) -> None:
        self.state = GameState(
            player=Player(
                x=self.window_width // 2,
                y=self.window_height - 40,
                score=0,
                lives=constants.PLAYER_INIT_LIVES,
                velocity=constants.PLAYER_INIT_VELOCITY,
                bullets=[]
            ),
            aliens=create_aliens(),
            aliens_bullets=[],
            aliens_velocity=constants.ALIENS_INIT_VELOCITY,
            round=0
        )

    def setup_rules(self) -> None:
        self.rules = [
            PlayerMoveRule(min_width=0, max_width=self.window_width),
            PlayerShootRule(fire_sound=self.player_fire_sound),
            PlayerBulletMoveRule(
                min_height=0,
                max_height=self.window_height
            ),
            AliensMoveRule(
                min_width=0,
                max_width=self.window_width,
                min_height=0,
                max_height=self.window_height
            ),
            AlienHitRule(
                alien_bullet_collide=alien_bullet_collide,
                player_hit_sound=self.player_hit_sound
            )
        ]
    
    def setup_sounds(self) -> None:
        self.alien_fire_sound = pygame.mixer.Sound(constants.ALIEN_FIRE_SOUND_PATH)
        self.alien_hit_sound = pygame.mixer.Sound(constants.ALIEN_HIT_SOUND_PATH)
        self.player_fire_sound = pygame.mixer.Sound(constants.PLAYER_FIRE_SOUND_PATH)
        self.player_hit_sound = pygame.mixer.Sound(constants.PLAYER_HIT_SOUND_PATH)
        self.breach_sound = pygame.mixer.Sound(constants.BREACH_SOUND_PATH)
        self.new_round_sound = pygame.mixer.Sound(constants.NEW_ROUND_SOUND_PATH)
    
    def update_game_state(self) -> None:
        new_state = self.state
        for rule in self.rules:
            new_state = rule(new_state, self.events)
        
        self.state = new_state
            
    
    def check_gameover(self) -> None:
        if self.state.player.lives > 0:
            return
        
        actions = [
            lambda: self.renderer.blit_gameover(
                self.display,
                self.state
            )
        ]

        is_clicked = lambda : any(
            filter(
                lambda event: event.type == pygame.MOUSEBUTTONDOWN,
                self.events
            )
        )

        self.general_loop(actions, [is_clicked])
        self.setup_gamestate()
    
    def main_loop(self) -> None:
        actions = [
            lambda : self.renderer.render(self.display, self.state),
            self.update_game_state,
            self.check_gameover
        ]
        
        self.general_loop(actions, [])
    
    def general_loop(self, actions: List[Action], end_conditions: List[EndCond]) -> None:
        clock = pygame.time.Clock()
        running = True
        while running:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    running = False
        
            for action in actions:
                action()
            
            for cond in end_conditions:
                if cond():
                    running = False
        
            pygame.display.update()
            clock.tick(constants.FPS)


def main():
    pygame.init()
    board = Board()
    board.main_loop()
    pygame.quit()


if __name__ == '__main__':
    main()