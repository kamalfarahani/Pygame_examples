import pygame


pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mouse Movement')

VELOCITY = 10

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
        
        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            dragon_rect.centerx, dragon_rect.centery = event.pos

    
    display_surface.fill((0,0,0))
    display_surface.blit(dragon_img, dragon_rect)
    pygame.display.update()


pygame.quit()