import arcade
import GameMap
import EnumTypes
from Items import PickupLasso


class ItemHandler:
    itemTypes = {}

    @staticmethod
    def add_type(item_type):
        new_type = ItemHandler.generate(item_type)
        GameMap.GameMap.place_object_random_empty_spot(new_type)
        if item_type not in ItemHandler.itemTypes:
            ItemHandler.itemTypes[item_type] = arcade.SpriteList()

        ItemHandler.itemTypes[item_type].append(new_type)

    @staticmethod
    def generate(item_type):
        if item_type == EnumTypes.ItemType.PICKUP_LASSO:
            return PickupLasso.PickupLasso()

    @staticmethod
    def draw():
        for sprite_list in ItemHandler.itemTypes.values():
            sprite_list.draw()

    @staticmethod
    def update():
        for sprite_list in ItemHandler.itemTypes.values():
            sprite_list.update()

    @staticmethod
    def reset():
        for item_type, sprite_list in ItemHandler.itemTypes.items():
            del sprite_list
            ItemHandler.itemTypes[item_type] = arcade.SpriteList()
