import pygame


SOUND1_PATH = './assets/sounds/sound_1.wav'
SOUND2_PATH = './assets/sounds/sound_2.wav'
MUSIC_PATH = './assets/sounds/music.wav'

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Adding Sound')

sound1 = pygame.mixer.Sound(SOUND1_PATH)
sound2 = pygame.mixer.Sound(SOUND2_PATH)

sound1.play()
pygame.time.delay(2000)
sound2.play()
pygame.time.delay(2000)
sound2.set_volume(0.1)
sound2.play()

#load background music
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.play(-1, 0, 0)

running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()