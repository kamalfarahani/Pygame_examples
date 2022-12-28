import random
import pygame
from typing import Callable, List

import constants
from gamestate import GameState
from player import Player, Direction
from burger import Burger
from render import Renderer
from rules import BurgerMoveRule, DogMoveRule, BurgerMissRule, EatBurgerRule


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
    
    def setup_gamestate(self):
        self.state = GameState(
            player=Player(
                x=self.window_width // 2,
                y=self.window_height - 40,
                direction=Direction.RIGHT,
                lives=constants.PLAYER_INIT_LIVES,
                boost_level=constants.INIT_BOOST_LEVEL,
                velocity=constants.PLAYER_NORMAL_VELOCITY
            ),
            burger=Burger(
                x=random.randint(5, self.window_width - 5),
                y=0,
                velocity=constants.INIT_BURGER_VELOCITY,
                acceleration=constants.BURGER_ACCELERATION
            )
        )

    def setup_rules(self) -> None:
        self.rules = [
            BurgerMoveRule(max_height=self.window_height),
            BurgerMissRule(
                max_width=self.window_width,
                max_height=self.window_height,
                sound=self.miss_sound),
            DogMoveRule(
                min_width=0,
                max_width=self.window_width - 5,
                min_height=100,
                max_height=self.window_height - 5
            ),
            EatBurgerRule(
                max_height=self.window_height,
                sound=self.eat_sound,
                dog_burger_collision_detector=self.renderer.dog_burger_collision_detector
            )
        ]
    
    def setup_sounds(self) -> None:
        self.miss_sound = pygame.mixer.Sound(constants.MISS_SOUND_PATH)
        self.eat_sound = pygame.mixer.Sound(constants.EAT_SOUND_PATH)
    
    def update_game_state(self) -> None:
        new_state = self.state
        for rule in self.rules:
            new_state = rule(new_state, self.events)
        
        self.state = new_state
    
    def check_gameover(self):
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

        pygame.mixer.music.load(constants.BACKGROUND_MUSIC_PATH)
        pygame.mixer.music.play(-1, 0, 0)
        
        self.general_loop(actions, [])
    
    def general_loop(self, actions: List[Action], end_conditions: List[EndCond]):
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