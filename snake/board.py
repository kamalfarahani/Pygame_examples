import random
from tkinter import mainloop
import pygame
from typing import Callable, List

import constants
from gamestate import GameState
from snake import Snake, Position
from rules import AppleCollideRule, snake_move_rule, snake_dx_dy_rule


Action = Callable[[], None]
EndCond = Callable[[], bool]


class Board:
    def __init__(self) -> None:
        self.window_width = constants.WINDOW_WIDTH
        self.window_height = constants.WINDOW_HEIGHT
        self.events = []
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        self.font = pygame.font.SysFont('gabriola', 48)
        self.setup_gamestate()
        self.setup_rules()
        self.setup_texts()

    def setup_gamestate(self) -> None:
        apple_x = random.randint(0, self.window_width)
        apple_y = random.randint(0, self.window_height)
        self.state = GameState(
            score=0,
            snake=Snake(
                size=constants.SNAKE_SIZE,
                head_position=Position(x=self.window_width // 2, y=self.window_height // 2),
                tail=[]
            ),
            apple_position=Position(apple_x, apple_y)
        )
    
    def setup_rules(self):
        pick_sound = pygame.mixer.Sound(constants.PICK_SOUND_PATH)
        apple_collide_rule = AppleCollideRule(
            lambda: self.snake_rect.colliderect(self.apple_rect),
            pick_sound,
            max_width=self.window_width,
            max_height=self.window_height
        )

        self.rules = [
            apple_collide_rule,
            snake_move_rule,
            snake_dx_dy_rule
        ]
    
    def setup_texts(self):
        self.score_text = self.font.render(constants.SCORE_TEXT, True, constants.BLACK_COLOR)
        self.gameover_text = self.font.render(constants.GAMEOVER_TEXT, True, constants.BLACK_COLOR)

        self.score_rect = self.score_text.get_rect()
        self.gameover_rect = self.gameover_text.get_rect()

        self.score_rect.topleft = (0, 0)
        self.gameover_rect.center = (self.window_width // 2, self.window_height // 2)
    
    def update_texts(self):
        self.score_text = self.font.render(
            f'{constants.SCORE_TEXT} {self.state.score}',
            True,
            constants.BLACK_COLOR)

    def update_game_state(self) -> None:
        new_state = self.state
        for rule in self.rules:
            new_state = rule(new_state, self.events)
        
        self.state = new_state

    def refresh_display(self) -> None:
        self.display.fill(constants.WHITE)

    def blit_texts(self):
        self.display.blit(self.score_text, self.score_rect)

    def blit_snake(self) -> None:
        snake = self.state.snake
        head = snake.head_position
        self.snake_rect =  pygame.draw.rect(
            self.display,
            color=constants.HEAD_COLOR,
            rect=pygame.Rect(head.x, head.y, snake.size, snake.size)
        )

        for body in snake.tail:
            pygame.draw.rect(
                self.display,
                color=constants.TAIL_COLOR,
                rect=pygame.Rect(body.x, body.y, snake.size, snake.size)
            )
    
    def blit_apple(self) -> None:
        apple_position = self.state.apple_position
        apple_size = self.state.snake.size
        self.apple_rect = pygame.draw.rect(
            self.display,
            color=constants.APPLE_COLOR,
            rect=pygame.Rect(
                apple_position.x,
                apple_position.y,
                apple_size,
                apple_size
            )
        )
    
    def blit_gameover(self):
        self.display.blit(self.gameover_text, self.gameover_rect)

    def is_snake_out(self):
        snake_head_position = self.state.snake.head_position
        return (
            snake_head_position.x < 0 or
            snake_head_position.x > self.window_width or
            snake_head_position.y < 0 or
            snake_head_position.y > self.window_height
        )
    
    def is_snake_in_it_self(self):
        snake = self.state.snake
        return snake.head_position in snake.tail
    
    def check_gameover(self):
        if self.is_snake_out() or self.is_snake_in_it_self():
            actions = [
                self.blit_gameover
            ]

            def is_clicked() -> bool:
                return any(
                    filter(
                        lambda event: event.type == pygame.MOUSEBUTTONDOWN,
                        self.events
                    )
                )

            self.general_loop(actions, [is_clicked])
            self.setup_gamestate()
    
    def main_loop(self) -> None:
        actions = [
            self.refresh_display,
            self.blit_snake,
            self.blit_apple,
            self.blit_texts,
            self.update_game_state,
            self.update_texts,
            self.check_gameover
        ]

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