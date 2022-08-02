import pygame


pygame.init()

GREEN = (0, 255, 0)
DARK_GREEN = (10, 50, 10)
BALCK = (0, 0, 0)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Blitting Images")

print(pygame.font.get_fonts())

system_font = pygame.font.SysFont('mono', 64)


system_text = system_font.render("Dragon Rules", True, GREEN, DARK_GREEN)
system_text_rect = system_text.get_rect()
system_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_surface.blit(system_text, system_text_rect)
    pygame.display.update()

pygame.quit()