import pygame
from typing import Callable, List

import constants
import state.tilemap
from state.gamestate import GameState
from state.player import Player
from state.rubymaker import RubyMaker
from render.renderer import Renderer
from rules.rubymaker import RubyMakerAnimateRule


Action = Callable[[], None]
EndCond = Callable[[], bool]


def generate_tile_map(int_map: List[List[int]]) -> state.tilemap.TileMap:
    number_to_class = {
        1: state.tilemap.TileOne,
        2: state.tilemap.TileTwo,
        3: state.tilemap.TileThree,
        4: state.tilemap.TileFour,
        5: state.tilemap.TileFive
    }

    tile_map = [
        number_to_class[int_map[i][j]](x=constants.TILE_SIZE * j, y=constants.TILE_SIZE * i)
        for i in range(len(int_map))
        for j in range(len(int_map[0]))
        if int_map[i][j] in number_to_class
    ]

    return tile_map


class Board:
    def __init__(self) -> None:
        self.window_width = constants.WINDOW_WIDTH
        self.window_height = constants.WINDOW_HEIGHT
        
        self.setup_gamestate()
        self.events = []
        
        self.display = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.renderer = Renderer()
        pygame.display.set_caption(constants.TITLE_STR)

        self.setup_sounds()
        self.setup_rules()
    
    def setup_gamestate(self) -> None:
        self.state = GameState(
            player=Player(
                lives=constants.INIT_PLAYER_LIVES,
                score=0
            ),
            tile_map=generate_tile_map(constants.TILE_MAP),
            ruby_maker=RubyMaker(
                x=constants.WINDOW_WIDTH // 2,
                y=constants.RUBY_MAKER_TOP_MARGIN,
                animation_index=0
            )
        )

    def setup_rules(self) -> None:
        self.rules = [
            RubyMakerAnimateRule()
        ]
    
    def setup_sounds(self) -> None:
        pass
    
    def update_game_state(self) -> None:
        new_state = self.state
        for rule in self.rules:
            new_state = rule(new_state, self.events)
        
        self.state = new_state
            
    
    def check_gameover(self) -> None:
        if not self.state.gameover:
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