import pygame
import constants
import render.alien
import render.bullet

from itertools import chain, filterfalse
from typing import List, Optional, Callable, Dict
from rules import GameRule
from state.gamestate import GameState



class AlienHitRule(GameRule):
    def __init__(
        self,
        alien_bullet_collide: Callable[[GameState],Dict[render.bullet.RedBullet, render.alien.Alien]],
        player_hit_sound: pygame.mixer.Sound
    ) -> None:
        self.alien_bullet_collide = alien_bullet_collide
        self.player_hit_sound = player_hit_sound

    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        collide_dict = self.alien_bullet_collide(state)
        if len(collide_dict) == 0:
            return state
        
        self.player_hit_sound.play()
        player_bullets = collide_dict.keys()
        hited_aliens = list(chain(*collide_dict.values()))

        new_palyer_bullets = list(filterfalse(
            lambda bullet: any(bullet.x == b.x and bullet.y == b.y for b in player_bullets),
            state.player.bullets
        ))

        new_aliens = list(filterfalse(
            lambda alien: any(alien.x == a.x and alien.y == a.y for a in hited_aliens),
            state.aliens
        ))

        return state._replace(
            player=state.player._replace(
                bullets=new_palyer_bullets,
                score=state.player.score + len(hited_aliens)
            ),
            aliens=new_aliens
        )