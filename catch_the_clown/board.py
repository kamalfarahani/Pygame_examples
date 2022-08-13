import pygame
from typing import Callable, List

import constants
from player import Player
from clown import Clown
from gamestate import GameState
from rules import clown_move_rule, ClownBounceRule, ClickClownRule


Action = Callable[[], None]
EndCond = Callable[[], bool]


class Board:
    def __init__(self) -> None:
        self.window_width = constants.WIDOW_WIDTH
        self.window_height = constants.WINDOW_HEIGHT

        self.setup_gamestate()
        self.events = []
        
        self.display = pygame.display.set_mode((constants.WIDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.font = pygame.font.Font(constants.FONT_PATH, constants.FONT_SIZE)
        pygame.display.set_caption(constants.TITLE_TEXT)

        self.setup_texts()
        self.setup_images()
        self.setup_sounds()
        self.setup_rules()
    
    def setup_gamestate(self):
        self.state = GameState(
            Clown(
                x=self.window_width // 2,
                y=self.window_height // 2,
                velocity=constants.CLOWN_STARTING_VELOCITY,
                dx=1,
                dy=1
            ),
            Player(score=0, lives=10)
        )

    def setup_rules(self) -> None:
        self.rules = [
            clown_move_rule,
            ClownBounceRule(
                max_x=self.window_width,
                max_y=self.window_height,
                min_x=0,
                min_y=0
            ),
            ClickClownRule(
                self.clown_rect,
                self.click_sound,
                self.miss_sound)
        ]

    def setup_texts(self) -> None:
        self.title_text = self.font.render(constants.TITLE_TEXT, True, constants.BLUE)
        self.score_text = self.font.render(constants.SCORE_TEXT, True, constants.YELLOW)
        self.lives_text = self.font.render(constants.LIVES_TEXT, True, constants.YELLOW)
        self.gameover_text = self.font.render(constants.GAMEOVER_TEXT, True, constants.YELLOW, constants.BLUE)

        self.title_rect = self.title_text.get_rect()
        self.score_rect = self.score_text.get_rect()
        self.lives_rect = self.lives_text.get_rect()
        self.gameover_rect = self.gameover_text.get_rect()

        self.title_rect.topleft = (10, 20)
        self.score_rect.topright = (self.window_width - 50, 10)
        self.lives_rect.topright = (self.window_width - 50, 50)
        self.gameover_rect.center = (self.window_width // 2, self.window_height // 2)
    

    def setup_images(self) -> None:
        self.background_img = pygame.image.load(constants.BACKGROUND_IMAGE_PATH)
        self.clown_img = pygame.image.load(constants.CLOWN_IMAGE_PATH)

        self.background_rect = self.background_img.get_rect()
        self.clown_rect = self.clown_img.get_rect()

        self.background_rect.topleft = (0, 0)
        self.clown_rect.center = (self.state.clown.x, self.state.clown.y)

    
    def setup_sounds(self) -> None:
        self.miss_sound = pygame.mixer.Sound(constants.MISS_SOUND_PATH)
        self.click_sound = pygame.mixer.Sound(constants.CLICK_SOUND_PATH)
        self.background_music = pygame.mixer.Sound(constants.BACKGROUND_MUSIC_PATH)
    

    def blit_texts(self) -> None:
        self.display.blit(self.title_text, self.title_rect)
        self.display.blit(self.score_text, self.score_rect)
        self.display.blit(self.lives_text, self.lives_rect)
    
    def blit_images(self) -> None:
        self.display.blit(self.background_img, self.background_rect)
        self.display.blit(self.clown_img, self.clown_rect)
    
    def update_texts(self) -> None:
        self.score_text = self.font.render(
            f'{constants.SCORE_TEXT} {self.state.player.score}',
            True,
            constants.YELLOW)
        
        self.lives_text = self.font.render(
            f'{constants.LIVES_TEXT} {self.state.player.lives}',
            True,
            constants.YELLOW)
    
    def update_game_state(self) -> None:
        new_state = self.state
        for rule in self.rules:
            new_state = rule(new_state, self.events)
        
        self.state = new_state

    def update_image_rects(self) -> None:
        self.clown_rect.center = (self.state.clown.x, self.state.clown.y)
    
    def check_gameover(self):
        if self.state.player.lives > 0:
            return
        
        def blit_gameover_rect() -> None:
            self.display.blit(self.gameover_text, self.gameover_rect)
        
        def is_clicked() -> bool:
            return any(
                filter(
                    lambda event: event.type == pygame.MOUSEBUTTONDOWN,
                    self.events
                )
            )
        
        actions = [blit_gameover_rect]
        end_conditions = [is_clicked]

        pygame.mixer.music.stop()
        self.general_loop(actions, end_conditions)
        self.setup_gamestate()
        pygame.mixer.music.play(-1, 0, 0)


    
    def main_loop(self) -> None:
        actions = [
            self.blit_images,
            self.blit_texts,
            self.update_game_state,
            self.update_texts,
            self.update_image_rects,
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


if __name__ == '__main__':
    pygame.init()
    board = Board()
    board.main_loop()
    pygame.quit()