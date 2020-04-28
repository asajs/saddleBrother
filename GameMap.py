import CellularAutomata
import GlobalInfo
import random

PUBLIC_MAP = CellularAutomata.CellularAutomata().generate(GlobalInfo.MAP_COUNT_X, GlobalInfo.MAP_COUNT_Y)


def place_objects(sprite):
    x, y = get_random_empty_spot()
    sprite.bottom = y * GlobalInfo.IMAGE_SIZE
    sprite.left = x * GlobalInfo.IMAGE_SIZE


def get_random_empty_spot():
    x = 0
    y = 0
    while PUBLIC_MAP[y][x] != ' ':
        y = random.randrange(2, len(PUBLIC_MAP))
        x = random.randrange(1, len(PUBLIC_MAP[0]))
    return x, y
