from enum import Enum


class ImageType(Enum):
    GROUND = "ground/"
    WALL = "wall/"
    WATER = "water/"
    LUSHGROUND = "lushGround/"
    MONSTER = "monster/"
    ITEM = "item"


class ZoneType(Enum):
    DESERT = "desert/"


class MonsterType(Enum):
    SCORPION = "scorpion.png"
