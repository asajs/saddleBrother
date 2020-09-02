import arcade
import ImageHandler
import EnumTypes


class PickupLasso(arcade.Sprite):
    def __init__(self):
        sprite = ImageHandler.get_specifc_image(EnumTypes.ZoneType.DESERT,
                                                EnumTypes.ImageType.ITEM,
                                                EnumTypes.PickupItemType.PICKUP_LASSO)
        super().__init__(sprite)
