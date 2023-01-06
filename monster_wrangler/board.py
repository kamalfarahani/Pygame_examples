import random
import pygame
from typing import Callable, List

import constants
from state.gamestate import GameState
from state.player import Player
from state.monster import Monster, Color
from render.renderer import Renderer, monsters_player_collide
from rules.player import PlayerMoveRule, WarpRule
from rules.monster import MonstersMoverRule, MonsterCollideRule, create_random_monster


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
            round=1,
            round_time=0,
            player=Player(
                score=0,
                lives=constants.INIT_LIVES,
                warps=constants.INIT_WARPS,
                x=self.window_width // 2,
                y=self.window_height - 30,
                velocity=constants.INIT_PLAYER_VELOCITY
            ),
            monsters=[
                create_random_monster(c)
                for c in Color
            ],
            catch_type=random.choice(list(Color))
        )

    def setup_rules(self) -> None:
        self.rules = [
            PlayerMoveRule(
                min_width=0,
                min_height=constants.TOP_MARGIN,
                max_width=self.window_width,
                max_height=self.window_height,
                bottom_line=self.window_height - constants.BOTTOM_MARGIN
            ),
            WarpRule(warp_sound=self.warp_sound),
            MonstersMoverRule(
                min_width=0,
                min_height=constants.TOP_MARGIN,
                max_width=self.window_width,
                max_height=self.window_height - constants.BOTTOM_MARGIN
            ),
            MonsterCollideRule(
                monster_player_collide_any=monsters_player_collide,
                catch_sound=self.catch_sound,
                die_sound=self.die_sound,
                next_level_sound=self.next_level_sound
            )
        ]
    
    def setup_sounds(self) -> None:
        self.catch_sound = pygame.mixer.Sound(constants.CATCH_SOUND_PATH)
        self.die_sound = pygame.mixer.Sound(constants.DIE_SOUND_PATH)
        self.warp_sound = pygame.mixer.Sound(constants.WARP_SOUND_PATH)
        self.next_level_sound = pygame.mixer.Sound(constants.NEXT_LEVEL_SOUND_PATH)
    
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