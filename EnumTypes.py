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


class MovingType(Enum):
    SCORPION = "scorpion.png"
    CHARACTER = "saddlebrother.png"


class ItemType(Enum):
    PICKUP_LASSO = "lasso.png"
