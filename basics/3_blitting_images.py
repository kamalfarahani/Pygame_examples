import pygame


pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Blitting")

dragon_left_img = pygame. transform. scale(
    pygame.image.load('./assets/pics/dragon_left.png'),
    (50, 50)
)
dragon_left_rect = dragon_left_img.get_rect()
dragon_left_rect.topleft = (0, 0)

dragon_right_img = pygame. transform. scale(
    pygame.image.load('./assets/pics/dragon_right.png'),
    (50, 50)
)
dragon_right_rect = dragon_right_img.get_rect()
dragon_right_rect.topright = (WINDOW_WIDTH, 0)

print(dragon_right_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surface.blit(dragon_left_img, dragon_left_rect)
    display_surface.blit(dragon_right_img, dragon_right_rect)
    pygame.draw.line(display_surface, (255,255,255), (0, 75), (WINDOW_WIDTH, 75), 4)
    pygame.display.update()

pygame.quit()