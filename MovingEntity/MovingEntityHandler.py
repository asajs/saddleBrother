import arcade
import EnumTypes
import math
import GameMap
from MovingEntity.Scorpion import ScorpionBase
from MovingEntity.Player import Character


class MovingEntityHandler:
    movingTypes = {}

    @staticmethod
    def add_type(entity_type):
        new_type = MovingEntityHandler.generate(entity_type)
        GameMap.GameMap.place_object_random_empty_spot(new_type)
        if entity_type not in MovingEntityHandler.movingTypes:
            MovingEntityHandler.movingTypes[entity_type] = arcade.SpriteList()

        MovingEntityHandler.movingTypes[entity_type].append(new_type)

    @staticmethod
    def generate(entity_type):
        if entity_type == EnumTypes.MovingType.SCORPION:
            return ScorpionBase.ScorpionBase()
        elif entity_type == EnumTypes.MovingType.CHARACTER:
            return Character.Character()

    @staticmethod
    def draw():
        for sprite_list in MovingEntityHandler.movingTypes.values():
            sprite_list.draw()
            
    @staticmethod
    def update():
        for sprite_list in MovingEntityHandler.movingTypes.values():
            sprite_list.update()
            
    @staticmethod
    def reset():
        for entity_type, sprite_list in MovingEntityHandler.movingTypes.items():
            del sprite_list
            MovingEntityHandler.movingTypes[entity_type] = arcade.SpriteList()

    @staticmethod
    def get_nearest_target(entity, list_of_valid_target_types):
        nearest_target = None
        nearest_distance = 9999999  # High number so that it is overwritten
        for entity_type, sprite_list in MovingEntityHandler.movingTypes.items():
            if entity_type in list_of_valid_target_types:
                for potential_target in sprite_list:
                    if potential_target is not entity:
                        distance = MovingEntityHandler.distance(entity, potential_target)
                        if distance < nearest_distance:
                            nearest_distance = distance
                            nearest_target = potential_target
        return nearest_target, nearest_distance

    @staticmethod
    def distance(entity, target):
        x = entity.center_x - target.center_x
        y = entity.center_y - target.center_y
        return math.hypot(x, y)
