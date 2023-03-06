import pygame
from typing import List, Callable
from state.gamestate import GameState

GameRule = Callable[[GameState, List[pygame.event.Event]], GameState]