import arcade
import ImageHandler
import EnumTypes
from MovingEntity import MovementComponent, MovingEntityHandler


class PickupLasso(arcade.sprite):
    def __init__(self):
        sprite = ImageHandler.get_specifc_image(EnumTypes.ZoneType.DESERT,
                                                EnumTypes.ImageType.ITEM,
                                                EnumTypes.ItemType.PICKUP_LASSO)
        super().__init__(sprite)
