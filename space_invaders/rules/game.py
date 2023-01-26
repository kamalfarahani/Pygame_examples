import pygame
import constants

from typing import List, Tuple
from rules import GameRule
from state.gamestate import GameState
from state.alien import Alien


def create_aliens():
    alines = [
        Alien(x=i * 60, y=j * 60 + constants.TOP_MARGIN)
        for i in range(1, 11)
        for j in range(1, 4)
    ]

    return alines


class GameOverRule(GameRule):
    def __init__(self, max_height: int, breach_sound: pygame.mixer.Sound) -> None:
        self.max_height = max_height
        self.breach_sound = breach_sound

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        if state.player.lives <= 0:
            return state._replace(gameover=True)
        
        is_breached = any(map(
            lambda alien: alien.y >= self.max_height,
            state.aliens
        ))

        if is_breached:
            self.breach_sound.play()
            return state._replace(gameover=True)

        return state


class NewRoundRule(GameRule):
    def __init__(self, new_round_sound: pygame.mixer.Sound) -> None:
        self.new_round_sound = new_round_sound

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        if len(state.aliens) > 0:
            return state

        self.new_round_sound.play()
        new_aliens = create_aliens()
        return state._replace(
            aliens=new_aliens,
            aliens_velocity=abs(state.aliens_velocity) + 1,
            round=state.round + 1
        )