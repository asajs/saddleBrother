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


class PickupItemType(Enum):
    PICKUP_LASSO = "lassoGround.png"


class AttackItemType(Enum):
    ATTACK_LASSO = "lasso.png"
