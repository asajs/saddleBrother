import arcade
import GameMap
import EnumTypes
from Items import PickupLasso, AttackLasso


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
        if item_type == EnumTypes.PickupItemType.PICKUP_LASSO:
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

    @staticmethod
    def add_type_with_start_end_points(item_type, start_point, end_point):
        new_type = ItemHandler.generate_with_points(item_type, start_point, end_point)
        if item_type not in ItemHandler.itemTypes:
            ItemHandler.itemTypes[item_type] = arcade.SpriteList()

        ItemHandler.itemTypes[item_type].append(new_type)

    @staticmethod
    def generate_with_points(item_type, start_point, end_point):
        if item_type == EnumTypes.AttackItemType.ATTACK_LASSO:
            return AttackLasso.AttackLasso(start_point, end_point)
