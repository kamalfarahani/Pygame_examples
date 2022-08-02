import pygame


pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mouse Movement')

VELOCITY = 5
FPS = 60
clock = pygame.time.Clock()

dragon_img = pygame. transform. scale(
    pygame.image.load('./assets/pics/dragon.png'),
    (50, 50)
)
dragon_rect = dragon_img.get_rect()
dragon_rect.centerx = WINDOW_WIDTH / 2
dragon_rect.bottom = WINDOW_HEIGHT - 10

running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #All keys that are held
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dragon_rect.x -= VELOCITY
    elif keys[pygame.K_RIGHT]:
        dragon_rect.x += VELOCITY
    elif keys[pygame.K_UP]:
        dragon_rect.y -= VELOCITY
    elif keys[pygame.K_DOWN]:
        dragon_rect.y += VELOCITY


    display_surface.fill((0,0,0))
    display_surface.blit(dragon_img, dragon_rect)
    pygame.display.update()

    clock.tick(FPS)


pygame.quit()