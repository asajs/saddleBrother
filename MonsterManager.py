import arcade
import Monster
import ImageHandler
import EnumTypes
import GameMap


class MonsterManager:
    monster_list = arcade.SpriteList()

    @staticmethod
    def draw():
        MonsterManager.monster_list.draw()

    @staticmethod
    def update(wall_list):
        for monster in MonsterManager.monster_list:
            monster.computer_next_move()
            monster.move()
            monster.account_for_collision_list(monster, wall_list)
        MonsterManager.monster_list.update()

    @staticmethod
    def add_monster(monster_type):
        if isinstance(monster_type, EnumTypes.MonsterType):
            new_monster = Monster.Monster(ImageHandler.get_specifc_image(EnumTypes.ZoneType.DESERT,
                                                                         EnumTypes.ImageType.MONSTER,
                                                                         monster_type))
            GameMap.GameMap.place_object_random_empty_spot(new_monster)
            MonsterManager.monster_list.append(new_monster)

    @staticmethod
    def reset():
        del MonsterManager.monster_list
        MonsterManager.monster_list = arcade.SpriteList()

