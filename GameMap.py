from CellularAutomata import CellularAutomata
import GlobalInfo
import random
import arcade
import ImageHandler
import EnumTypes


class GameMap:
    PUBLIC_ASCII_MAP = CellularAutomata().generate(GlobalInfo.MAP_TILE_COUNT_X, GlobalInfo.MAP_TILE_COUNT_Y)
    GROUND_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)
    WALL_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)
    WATER_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)
    GRASS_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)

    @staticmethod
    def place_object_random_empty_spot(sprite):
        x, y = GameMap.get_random_empty_spot()
        sprite.bottom = y * GlobalInfo.IMAGE_SIZE
        sprite.left = x * GlobalInfo.IMAGE_SIZE

    @staticmethod
    def get_random_empty_spot():
        x = 0
        y = 0
        while GameMap.PUBLIC_ASCII_MAP[y][x] != ' ':
            y = random.randrange(1, len(GameMap.PUBLIC_ASCII_MAP))
            x = random.randrange(1, len(GameMap.PUBLIC_ASCII_MAP[0]))
        return x, y

    @staticmethod
    def reset():
        del GameMap.PUBLIC_ASCII_MAP[:]
        del GameMap.GRASS_LIST
        del GameMap.WATER_LIST
        del GameMap.WALL_LIST
        del GameMap.GROUND_LIST

        GameMap.GROUND_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        GameMap.WALL_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        GameMap.WATER_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        GameMap.GRASS_LIST = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        GameMap.PUBLIC_ASCII_MAP = CellularAutomata().generate(GlobalInfo.MAP_TILE_COUNT_X, GlobalInfo.MAP_TILE_COUNT_Y)

        GameMap.generate_sprites_from_ascii()

    @staticmethod
    def generate_sprites_from_ascii():
        row = 0
        for line in GameMap.PUBLIC_ASCII_MAP:
            col = 0
            for ground_ascii in line:
                ground_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                              EnumTypes.ImageType.GROUND),
                                              GlobalInfo.CHARACTER_SCALING)
                ground_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                ground_sprite.left = col * GlobalInfo.IMAGE_SIZE
                GameMap.GROUND_LIST.append(ground_sprite)
                if ground_ascii == GlobalInfo.WALL:
                    wall_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                EnumTypes.ImageType.WALL),
                                                GlobalInfo.CHARACTER_SCALING)
                    wall_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    wall_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    GameMap.WALL_LIST.append(wall_sprite)
                elif ground_ascii == GlobalInfo.WATER:
                    water_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                 EnumTypes.ImageType.WATER),
                                                 GlobalInfo.CHARACTER_SCALING)
                    water_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    water_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    GameMap.WATER_LIST.append(water_sprite)
                elif ground_ascii == GlobalInfo.GRASS:
                    grass_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                 EnumTypes.ImageType.LUSHGROUND),
                                                 GlobalInfo.CHARACTER_SCALING)
                    grass_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    grass_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    GameMap.GRASS_LIST.append(grass_sprite)
                col += 1
            row += 1

    @staticmethod
    def draw():
        GameMap.GROUND_LIST.draw()
        GameMap.WALL_LIST.draw()
        GameMap.WATER_LIST.draw()
        GameMap.GRASS_LIST.draw()
