from collections import namedtuple

Color = namedtuple('Color', ['r', 'g', 'b'])

PLAYER_STARTING_LIVES = 5
CLOWN_STARTING_VELOCITY = 3
CLOWN_ACCELERATION = 0.5
FPS = 60

BLUE = Color(1, 175, 209)
YELLOW = Color(248, 231, 28)


FONT_PATH = './assets/fonts/Franxurter.ttf'
FONT_SIZE = 32

WIDOW_WIDTH = 945
WINDOW_HEIGHT = 600

TITLE_TEXT = 'Catch the Clown'
SCORE_TEXT = 'score:'
LIVES_TEXT = 'lives:'
GAMEOVER_TEXT = 'GAMEOVER!'
CLICK_TEXT = 'Click down to continue'

BACKGROUND_IMAGE_PATH = './assets/images/background.png'
CLOWN_IMAGE_PATH = './assets/images/clown.png'


CLICK_SOUND_PATH = './assets/sounds/click_sound.wav'
MISS_SOUND_PATH = './assets/sounds/miss_sound.wav'
BACKGROUND_MUSIC_PATH = './assets/sounds/ctc_background_music.wav'
