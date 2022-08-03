import random
from re import T
from shutil import move
import pygame


pygame.init()
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Feed the dragon')


FPS=60
clock = pygame.time.Clock()


PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


font = pygame.font.Font('./assets/fonts/AttackGraffiti.ttf', 32)
score_text = font.render(f'Score: {score}', True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render('Feed the Dragon', True, GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH // 2
title_rect.y = 10

lives_text = font.render(f'Lives {player_lives}', True, GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH, 10)

game_over_text = font.render('GAMEOVER', True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 32)


def update_texts():
    global score_text
    global title_text
    global lives_text
    score_text = font.render(f'Score: {score}', True, GREEN, DARKGREEN)
    title_text = font.render('Feed the Dragon', True, GREEN, WHITE)
    lives_text = font.render(f'Lives {player_lives}', True, GREEN, DARKGREEN)


coin_sound = pygame.mixer.Sound('./assets/sounds/coin_sound.wav')
miss_sound = pygame.mixer.Sound('./assets/sounds/miss_sound.wav')
miss_sound.set_volume(0.1)

pygame.mixer.music.load('./assets/sounds/music.wav')

player_img = pygame. transform. scale(
    pygame.image.load('./assets/pics/dragon.png'),
    (50, 50)
)
player_rect = player_img.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT // 2


coin_image = pygame.image.load('./assets/pics/coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


def player_movement_handler(keys, player_rect):
    VELOCITY = 5
    def pos_updater_creator(amount, cord):
        def updater(rect):
            setattr(rect, cord, getattr(rect, cord) + amount)
        
        return updater

    movement_dict = {
        pygame.K_UP: pos_updater_creator(-VELOCITY, 'y'),
        pygame.K_DOWN: pos_updater_creator(VELOCITY, 'y'),
        pygame.K_LEFT: pos_updater_creator(-VELOCITY, 'x'),
        pygame.K_RIGHT: pos_updater_creator(VELOCITY, 'x'),
    }

    for k in movement_dict:
        if keys[k]:
            movement_dict[k](player_rect)
    
    check_players_coordinate(player_rect)


def check_players_coordinate(player_rect):
    players_range = {
        'x': (0, WINDOW_WIDTH),
        'y': (70, WINDOW_HEIGHT)
    }

    is_in_range = lambda range_, value: range_[0] <= value <= range_[1]

    for coord in ['x', 'y']:
        if not is_in_range(players_range[coord], getattr(player_rect, coord)):
            a = getattr(player_rect, coord)
            min_r, max_r = players_range[coord]
            setattr(
                player_rect,
                coord,
                min(max(min_r, a), max_r)
            )


def coin_movement_handler(coin_rect):
    global coin_velocity
    coin_velocity += COIN_ACCELERATION/100
    if coin_rect.x < 0:
        global player_lives
        player_lives -= 1
        miss_sound.play()
        reposition_coin(coin_rect)
    else:
        coin_rect.x -= coin_velocity


def reposition_coin(coin_rect):
    coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
    coin_rect.y = random.randint(64, WINDOW_HEIGHT -  32)


def player_collider_handler(player_rect, coin_rect):
    if player_rect.colliderect(coin_rect):
        reposition_coin(coin_rect)
        coin_sound.play()
        global score
        score += 1

def is_gameover():
    return player_lives <= 0

def start_gameover_window():
    display_surface.blit(game_over_text, game_over_rect)
    pygame.display.update()
    pygame.mixer.music.stop()
    running = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                running = False
                reset_game()
                return True


def reset_game():
    global player_lives, score, coin_velocity
    player_lives = PLAYER_STARTING_LIVES
    score = 0
    coin_velocity = COIN_STARTING_VELOCITY


pygame.mixer.music.play(-1, 0, 0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

    
    player_movement_handler(pygame.key.get_pressed(), player_rect)
    coin_movement_handler(coin_rect)
    player_collider_handler(player_rect, coin_rect)

    if is_gameover():
        running = start_gameover_window()
        pygame.mixer.music.play(-1, 0, 0)


    display_surface.fill(BLACK)

    update_texts()
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)

    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    display_surface.blit(player_img, player_rect)
    display_surface.blit(coin_image, coin_rect)

    pygame.display.update()
    clock.tick(FPS)


pygame.quit()