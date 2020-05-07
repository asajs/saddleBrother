from os import path, chdir
from MovingEntity import MovingEntityHandler
from Items import ItemHandler
import GameMap
import PauseView
import arcade
import EnumTypes
import GlobalInfo


class GameWindow(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.csscolor.LIGHT_GOLDENROD_YELLOW)

        file_path = path.dirname(path.abspath(__file__))
        chdir(file_path)

        self.moving_entity_handler = MovingEntityHandler.MovingEntityHandler()
        self.items = ItemHandler.ItemHandler()
        self.game_map = GameMap.GameMap()

        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.game_map.reset()

        self.moving_entity_handler.add_type(EnumTypes.MovingType.SCORPION)
        self.moving_entity_handler.add_type(EnumTypes.MovingType.CHARACTER)
        self.items.add_type(EnumTypes.ItemType.PICKUP_LASSO)

    def on_draw(self):
        arcade.start_render()

        # screen is drawn in layered order. Items on the topmost layer get called last
        self.game_map.draw()
        self.items.draw()
        self.moving_entity_handler.draw()

        player = MovingEntityHandler.MovingEntityHandler.movingTypes[EnumTypes.MovingType.CHARACTER][0]

        score_text = f"Score: {player.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.BLACK, 20)
        lasso_count_text = f"Lassos: {player.lasso_count}"
        arcade.draw_text(lasso_count_text, self.view_left + 10, 40 + self.view_bottom, arcade.csscolor.BLACK, 20)

    def on_update(self, delta_time: float):
        self.moving_entity_handler.update()
        self.items.update()
        player = MovingEntityHandler.MovingEntityHandler.movingTypes[EnumTypes.MovingType.CHARACTER][0]
        # self.player.move()
        # if arcade.check_for_collision(self.player, self.goal):
        #     self.score += 5
        #     self.player.lasso_count += 1
        #     self.game_map.place_object_random_empty_spot(self.goal)
        #     self.moving_entity_handler.add_type(EnumTypes.MovingType.SCORPION)

        viewport_changed = False

        # Scroll left
        left_boundary = self.view_left + GlobalInfo.VIEWPORT_MARGIN_HORT
        if player.left < left_boundary:
            self.view_left -= left_boundary - player.left
            viewport_changed = True

        # Scroll right
        right_boundary = self.view_left + GlobalInfo.SCREEN_WIDTH - GlobalInfo.VIEWPORT_MARGIN_HORT
        if player.right > right_boundary:
            self.view_left += player.right - right_boundary
            viewport_changed = True

        # Scroll up
        top_boundary = self.view_bottom + GlobalInfo.SCREEN_HEIGHT - GlobalInfo.VIEWPORT_MARGIN_VERT
        if player.top > top_boundary:
            self.view_bottom += player.top - top_boundary
            viewport_changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + GlobalInfo.VIEWPORT_MARGIN_VERT
        if player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - player.bottom
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

        # self.lasso_list.update()
        #
        # top = player.center_y + GlobalInfo.VIEWPORT_MARGIN_VERT
        # bottom = player.center_y - GlobalInfo.VIEWPORT_MARGIN_VERT
        # right = player.center_x + GlobalInfo.VIEWPORT_MARGIN_HORT
        # left = player.center_x - GlobalInfo.VIEWPORT_MARGIN_HORT
        #
        # for lasso in self.lasso_list:
        #
        #     monster_hit_list = arcade.check_for_collision_with_list(lasso, self.monster_manager.monster_list)
        #     wall_hit_list = arcade.check_for_collision_with_list(lasso, self.wall_list)
        #
        #     if len(monster_hit_list) > 0 or len(wall_hit_list) > 0:
        #         lasso.remove_from_sprite_lists()
        #
        #     for monster in monster_hit_list:
        #         monster.remove_from_sprite_lists()
        #
        #     if lasso.bottom > top or lasso.top < bottom or lasso.right < left or lasso.left > right:
        #         lasso.remove_from_sprite_lists()
        #
        # self.player_list.update()

    def on_key_press(self, symbol: int, modifiers: int):
        MovingEntityHandler.MovingEntityHandler.movingTypes[EnumTypes.MovingType.CHARACTER][0].on_key_press(symbol,
                                                                                                            modifiers)

        if symbol == arcade.key.ESCAPE:
            paused_view = PauseView.PausedScreenView(self)
            self.window.show_view(paused_view)

    def on_key_release(self, symbol: int, modifiers: int):
        MovingEntityHandler.MovingEntityHandler.movingTypes[EnumTypes.MovingType.CHARACTER][0].on_key_release(symbol,
                                                                                                              modifiers)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        MovingEntityHandler.MovingEntityHandler.movingTypes[EnumTypes.MovingType.CHARACTER][0].on_mouse_press(x,
                                                                                                              y,
                                                                                                              button,
                                                                                                              modifiers)

        i = 0
        while i < 20:
            MovingEntityHandler.MovingEntityHandler.add_type(EnumTypes.MovingType.SCORPION)
            i += 1
        # if self.player.lasso_count == 0:
        #     return
        #
        # self.player.lasso_count -= 1
        #
        # lasso = arcade.Sprite(ImageHandler.get_specific("desert/item/lasso.png"),
        #                       GlobalInfo.CHARACTER_SCALING)
        #
        # lasso.center_x = self.player.center_x
        # lasso.center_y = self.player.center_y
        #
        # x_diff = (x + self.view_left) - lasso.center_x
        # y_diff = (y + self.view_bottom) - lasso.center_y
        #
        # angle = math.atan2(y_diff, x_diff)
        # lasso.angle = math.degrees(angle) - 90
        #
        # bullet_speed = 5.0
        # lasso.change_x = math.cos(angle) * bullet_speed
        # lasso.change_y = math.sin(angle) * bullet_speed
        #
        # self.lasso_list.append(lasso)

    def reset(self):
        self.moving_entity_handler.reset()
        self.game_map.reset()
