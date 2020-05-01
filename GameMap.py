from CellularAutomata import CellularAutomata
import GlobalInfo
import random


class GameMap:
    PUBLIC_MAP = CellularAutomata().generate(GlobalInfo.MAP_COUNT_X, GlobalInfo.MAP_COUNT_Y)

    @staticmethod
    def place_object_random_empty_spot(sprite):
        x, y = GameMap.get_random_empty_spot()
        sprite.bottom = y * GlobalInfo.IMAGE_SIZE
        sprite.left = x * GlobalInfo.IMAGE_SIZE

    @staticmethod
    def get_random_empty_spot():
        x = 0
        y = 0
        while GameMap.PUBLIC_MAP[y][x] != ' ':
            y = random.randrange(1, len(GameMap.PUBLIC_MAP))
            x = random.randrange(1, len(GameMap.PUBLIC_MAP[0]))
        return x, y

    @staticmethod
    def reset():
        del GameMap.PUBLIC_MAP[:]
        GameMap.PUBLIC_MAP = CellularAutomata().generate(GlobalInfo.MAP_COUNT_X, GlobalInfo.MAP_COUNT_Y)

