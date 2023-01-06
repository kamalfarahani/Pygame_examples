import pygame
import random
import constants
import state.monster
import render.monster

from typing import List, Callable, Optional
from rules import GameRule
from state.gamestate import GameState


def create_random_monster(color: state.monster.Color):
    return state.monster.Monster(
        color=color,
        x=random.randint(constants.LEFT_MARGIN, constants.WINDOW_WIDTH),
        y=random.randint(constants.TOP_MARGIN, constants.WINDOW_HEIGHT - constants.BOTTOM_MARGIN),
        velocity_x=random.randint(-2 *constants.INIT_MONSTER_VELOCITY, constants.INIT_MONSTER_VELOCITY * 2),
        velocity_y=random.randint(-2 * constants.INIT_MONSTER_VELOCITY, constants.INIT_MONSTER_VELOCITY * 2)
    )


class MonstersMoverRule(GameRule):
    def __init__(self, min_width: int, min_height: int, max_width: int, max_height: int):
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
    
    def move_monser(self, monster: state.monster.Monster) -> state.monster.Monster:
        x, y = monster.x, monster.y
        velocity_x = monster.velocity_x
        velocity_y = monster.velocity_y

        new_velocity_x = velocity_x if self.min_width < x + velocity_x < self.max_width else  -velocity_x
        new_velocity_y = velocity_y if self.min_height < y + velocity_y < self.max_height else -velocity_y

        return monster._replace(
            x=x + new_velocity_x,
            y=y + new_velocity_y,
            velocity_x=new_velocity_x,
            velocity_y=new_velocity_y
        )
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        monsters = state.monsters
        new_monsters = list(map(self.move_monser, monsters))

        return state._replace(
            monsters=new_monsters
        )


class MonsterCollideRule(GameRule):
    def __init__(
        self,
        monster_player_collide_any: Callable[[GameState], Optional[render.monster.Monster]],
        catch_sound: pygame.mixer.Sound,
        die_sound: pygame.mixer.Sound,
        next_level_sound: pygame.mixer.Sound
        ) -> None:
        self.monster_player_collide_any = monster_player_collide_any
        self.catch_sound = catch_sound
        self.die_sound = die_sound
        self.next_level_sound = next_level_sound
    
    def next_level(self, game_state: GameState) -> GameState:
        self.next_level_sound.play()
        new_round = game_state.round + 1
        new_monsters =[
            create_random_monster(c)
            for c in list(state.monster.Color) * new_round
        ]

        return game_state._replace(
            monsters=new_monsters,
            round=new_round,
            round_time=0,
            player=game_state.player._replace(
                y=constants.WINDOW_HEIGHT - 20,
                warps=game_state.player.warps + 1
            )
        )
    
    def __call__(self, state: GameState, events: List[pygame.event.Event]) -> GameState:
        collided_monster = self.monster_player_collide_any(state)
        if not collided_monster:
            return state
        
        if collided_monster.color == state.catch_type:
            self.catch_sound.play()
            new_monsters = list(filter(
                lambda m: m.x != collided_monster.rect.centerx and m.y != collided_monster.rect.centery,
                state.monsters
            ))

            if len(new_monsters) == 0:
                return self.next_level(state)

            new_catch_type = random.choice([m.color for m in new_monsters])
            added_score = max(10, 100*state.round - state.round_time)

            return state._replace(
                monsters=new_monsters,
                catch_type=new_catch_type,
                player=state.player._replace(
                    score=state.player.score + added_score
                )
            )
        else:
            self.die_sound.play()
            return state._replace(
                player=state.player._replace(
                    lives=state.player.lives - 1,
                    x=constants.WINDOW_WIDTH // 2,
                    y=constants.WINDOW_HEIGHT - 20
                )
            )