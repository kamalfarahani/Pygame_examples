import pygame
import constants
import state.player
from typing import List
from render.animatable import Animatable
from state.general import Direction



def flip_right(imgs: List[pygame.Surface]) -> List[pygame.Surface]:
    return [
        pygame.transform.flip(img, True, False)
        for img in imgs
    ]


run_right_animation_images = [
    pygame.transform.scale(
        pygame.image.load(path),
        (constants.PLAYER_SIZE, constants.PLAYER_SIZE)
    )
    for path in constants.PLAYER_RUN_RIGHT_ANIMATION_PATHS
]

run_left_animation_images = flip_right(run_right_animation_images)

idle_right_animation_images = [
    pygame.transform.scale(
        pygame.image.load(path),
        (constants.PLAYER_SIZE, constants.PLAYER_SIZE)
    )
    for path in constants.PLAYER_IDLE_RIGHT_ANIMATION_PATHS
]

idle_left_animation_images = flip_right(idle_right_animation_images)

jump_right_animation_images = [
    pygame.transform.scale(
        pygame.image.load(path),
        (constants.PLAYER_SIZE, constants.PLAYER_SIZE)
    )
    for path in constants.PLAYER_JUMP_RIGHT_ANIMATION_PATHS
]

jump_left_animation_images = flip_right(jump_right_animation_images)

attack_right_animation_images = [
    pygame.transform.scale(
        pygame.image.load(path),
        (constants.PLAYER_SIZE, constants.PLAYER_SIZE)
    )
    for path in constants.PLAYER_ATTACK_RIGHT_ANIMATION_PATHS
]

attack_left_animation_images = flip_right(attack_right_animation_images)

animation_map = {
    Direction.LEFT: {
        state.player.AnimationState.ATTACKING: attack_left_animation_images,
        state.player.AnimationState.IDLE: idle_left_animation_images,
        state.player.AnimationState.JUMPING: jump_left_animation_images,
        state.player.AnimationState.RUNNING: run_left_animation_images
    },
    Direction.RIGHT: {
        state.player.AnimationState.ATTACKING: attack_right_animation_images,
        state.player.AnimationState.IDLE: idle_right_animation_images,
        state.player.AnimationState.JUMPING: jump_right_animation_images,
        state.player.AnimationState.RUNNING: run_right_animation_images
    }
}

class Player(Animatable):
    def __init__(self, player_state: state.player.Player) -> None:
        animation_images = animation_map[player_state.direction][player_state.animation_state]
        super().__init__(player_state, animation_images)
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = player_state.position