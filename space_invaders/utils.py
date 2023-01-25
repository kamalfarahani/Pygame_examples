import constants
from state.alien import Alien


def create_aliens():
    alines = [
        Alien(x=i * 60, y=j * 60 + constants.TOP_MARGIN)
        for i in range(1, 11)
        for j in range(1, 4)
    ]

    return alines