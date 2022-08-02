import pygame
import random

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Collision Detection")


FPS=60
clock = pygame.time.Clock()
VELOCITY = 5

dragon_img = pygame. transform. scale(
    pygame.image.load('./assets/pics/dragon.png'),
    (50, 50)
)
dragon_rect = dragon_img.get_rect()
dragon_rect.centerx = WINDOW_WIDTH // 2
dragon_rect.bottom = WINDOW_HEIGHT - 10

coin_img = pygame.image.load('./assets/pics/coin.png')
coin_rect = coin_img.get_rect()
coin_rect.centerx = WINDOW_WIDTH // 2
coin_rect.bottom = WINDOW_HEIGHT // 2

def check_movement_pos(rect):
    if rect.x < 0:
        rect.x = 0
    
    if rect.x > WINDOW_WIDTH:
        rect.centerx = WINDOW_WIDTH
    
    if rect.y < 0:
        rect.y = 0
    
    if rect.y > WINDOW_HEIGHT:
        rect.centery = WINDOW_HEIGHT


running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill((0, 0, 0))
    pygame.draw.rect(display_surface, (0, 0, 255), dragon_rect, 1)
    pygame.draw.rect(display_surface, (0, 255, 0), coin_rect, 1)

    display_surface.blit(dragon_img, dragon_rect)
    display_surface.blit(coin_img, coin_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dragon_rect.x -= VELOCITY
    elif keys[pygame.K_RIGHT]:
        dragon_rect.x += VELOCITY
    elif keys[pygame.K_UP]:
        dragon_rect.y -= VELOCITY
    elif keys[pygame.K_DOWN]:
        dragon_rect.y += VELOCITY

    check_movement_pos(dragon_rect)

    if dragon_rect.colliderect(coin_rect):
        rand_pos = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        coin_rect.centerx, coin_rect.centery = rand_pos

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()