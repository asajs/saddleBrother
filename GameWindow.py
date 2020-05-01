from os import path, chdir
from MonsterManager import MonsterManager
from GameMap import GameMap
import PauseView
import arcade
import Character
import ImageHandler
import EnumTypes
import GlobalInfo
import math


class GameWindow(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.csscolor.LIGHT_GOLDENROD_YELLOW)

        file_path = path.dirname(path.abspath(__file__))
        chdir(file_path)

        self.score = 0

        self.player_list = None
        self.item_list = None
        self.wall_list = None
        self.ground_list = None
        self.water_list = None
        self.lasso_list = None
        self.grass_list = None

        self.player = None
        self.goal = None

        self.monster_manager = MonsterManager()
        self.game_map = GameMap()

        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.lasso_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        self.ground_list = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        self.water_list = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        self.grass_list = arcade.SpriteList(is_static=True, use_spatial_hash=True)

        self.player = Character.Character(ImageHandler.get_path("Images/saddlebrother.png"))
        self.goal = arcade.Sprite(ImageHandler.get_specific("desert/item/lasso.png"),
                                  GlobalInfo.CHARACTER_SCALING)

        self.monster_manager.add_monster(EnumTypes.MonsterType.SCORPION)

        row = 0
        for line in self.game_map.PUBLIC_MAP:
            col = 0
            for ground_ascii in line:
                ground_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                              EnumTypes.ImageType.GROUND),
                                              GlobalInfo.CHARACTER_SCALING)
                ground_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                ground_sprite.left = col * GlobalInfo.IMAGE_SIZE
                self.ground_list.append(ground_sprite)
                if ground_ascii == GlobalInfo.WALL:
                    wall_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                EnumTypes.ImageType.WALL),
                                                GlobalInfo.CHARACTER_SCALING)
                    wall_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    wall_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.wall_list.append(wall_sprite)
                elif ground_ascii == GlobalInfo.WATER:
                    water_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                 EnumTypes.ImageType.WATER),
                                                 GlobalInfo.CHARACTER_SCALING)
                    water_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    water_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.water_list.append(water_sprite)
                elif ground_ascii == GlobalInfo.GRASS:
                    grass_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                 EnumTypes.ImageType.LUSHGROUND),
                                                 GlobalInfo.CHARACTER_SCALING)
                    grass_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    grass_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.grass_list.append(grass_sprite)
                col += 1
            row += 1

        self.game_map.place_object_random_empty_spot(self.player)
        self.game_map.place_object_random_empty_spot(self.goal)

        self.player_list.append(self.player)
        self.item_list.append(self.goal)

    def on_draw(self):
        arcade.start_render()

        # screen is drawn in layered order. Items on the topmost layer get called last
        self.ground_list.draw()
        self.wall_list.draw()
        self.grass_list.draw()
        self.water_list.draw()
        self.item_list.draw()
        self.lasso_list.draw()

        self.monster_manager.draw()

        self.player_list.draw() # This should always be drawn last

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.BLACK, 20)
        lasso_count_text = f"Lassos: {self.player.lasso_count}"
        arcade.draw_text(lasso_count_text, self.view_left + 10, 40 + self.view_bottom, arcade.csscolor.BLACK, 20)

    def on_update(self, delta_time: float):
        self.player.move()
        if arcade.check_for_collision(self.player, self.goal):
            self.score += 5
            self.player.lasso_count += 1
            self.game_map.place_object_random_empty_spot(self.goal)
            self.monster_manager.add_monster(EnumTypes.MonsterType.SCORPION)

        self.player.account_for_collision_list(self.player, self.wall_list)
        self.player.account_for_collision_list(self.player, self.monster_manager.monster_list)
        self.monster_manager.update(self.wall_list)
        self.monster_manager.update(self.player_list)

        viewport_changed = False

        # Scroll left
        left_boundary = self.view_left + GlobalInfo.VIEWPORT_MARGIN_HORT
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            viewport_changed = True

        # Scroll right
        right_boundary = self.view_left + GlobalInfo.SCREEN_WIDTH - GlobalInfo.VIEWPORT_MARGIN_HORT
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            viewport_changed = True

        # Scroll up
        top_boundary = self.view_bottom + GlobalInfo.SCREEN_HEIGHT - GlobalInfo.VIEWPORT_MARGIN_VERT
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            viewport_changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + GlobalInfo.VIEWPORT_MARGIN_VERT
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            viewport_changed = True

        if viewport_changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                GlobalInfo.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                GlobalInfo.SCREEN_HEIGHT + self.view_bottom)

        self.lasso_list.update()

        top = self.player.center_y + GlobalInfo.VIEWPORT_MARGIN_VERT
        bottom = self.player.center_y - GlobalInfo.VIEWPORT_MARGIN_VERT
        right = self.player.center_x + GlobalInfo.VIEWPORT_MARGIN_HORT
        left = self.player.center_x - GlobalInfo.VIEWPORT_MARGIN_HORT

        for lasso in self.lasso_list:

            monster_hit_list = arcade.check_for_collision_with_list(lasso, self.monster_manager.monster_list)
            wall_hit_list = arcade.check_for_collision_with_list(lasso, self.wall_list)

            if len(monster_hit_list) > 0 or len(wall_hit_list) > 0:
                lasso.remove_from_sprite_lists()

            for monster in monster_hit_list:
                monster.remove_from_sprite_lists()

            if lasso.bottom > top or lasso.top < bottom or lasso.right < left or lasso.left > right:
                lasso.remove_from_sprite_lists()

        self.player_list.update()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player.up_pressed = True
        elif symbol == arcade.key.DOWN:
            self.player.down_pressed = True
        elif symbol == arcade.key.LEFT:
            self.player.left_pressed = True
        elif symbol == arcade.key.RIGHT:
            self.player.right_pressed = True
        elif symbol == arcade.key.ESCAPE:
            paused_view = PauseView.PausedScreenView(self)
            self.window.show_view(paused_view)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player.up_pressed = False
        elif symbol == arcade.key.DOWN:
            self.player.down_pressed = False
        elif symbol == arcade.key.LEFT:
            self.player.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.player.right_pressed = False

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # i = 0
        # while i < 200:
        #     self.monster_manager.add_monster(EnumTypes.MonsterType.SCORPION)
        #     i += 1
        if self.player.lasso_count == 0:
            return

        self.player.lasso_count -= 1

        lasso = arcade.Sprite(ImageHandler.get_specific("desert/item/lasso.png"),
                              GlobalInfo.CHARACTER_SCALING)

        lasso.center_x = self.player.center_x
        lasso.center_y = self.player.center_y

        x_diff = (x + self.view_left) - lasso.center_x
        y_diff = (y + self.view_bottom) - lasso.center_y

        angle = math.atan2(y_diff, x_diff)
        lasso.angle = math.degrees(angle) - 90

        bullet_speed = 5.0
        lasso.change_x = math.cos(angle) * bullet_speed
        lasso.change_y = math.sin(angle) * bullet_speed

        self.lasso_list.append(lasso)

    def reset(self):
        self.monster_manager.reset()
        self.game_map.reset()