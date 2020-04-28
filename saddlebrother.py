from os import path, chdir
import arcade
import Character
import CellularAutomata
import ImageHandler
import EnumTypes
import GlobalInfo
import GameMap


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(GlobalInfo.SCREEN_WIDTH, GlobalInfo.SCREEN_HEIGHT, GlobalInfo.SCREEN_TITLE)

        screen_width, screen_height = self.get_size()
        arcade.set_background_color(arcade.csscolor.LIGHT_GOLDENROD_YELLOW)

        file_path = path.dirname(path.abspath(__file__))
        chdir(file_path)

        self.score = 0

        self.player_list = None
        self.item_list = None
        self.wall_list = None
        self.ground_list = None
        self.water_list = None
        self.monster_list = None
        self.grass_list = None

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.viewport_margin_hort = screen_width / 2 - GlobalInfo.IMAGE_SIZE * 2
        self.viewport_margin_vert = screen_height / 2 - GlobalInfo.IMAGE_SIZE * 2

        self.player = None
        self.goal = None
        self.monster = None

        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.water_list = arcade.SpriteList()
        self.grass_list = arcade.SpriteList()
        self.monster_list = arcade.SpriteList()
        self.score = 0

        self.player = Character.Character(ImageHandler.get_path("Images/saddlebrother.png"))
        self.monster = Character.Character(ImageHandler.get_specifc_image(EnumTypes.ZoneType.DESERT,
                                                                          EnumTypes.ImageType.MONSTER,
                                                                          EnumTypes.MonsterType.SCORPION))
        self.goal = arcade.Sprite(ImageHandler.get_specific("desert/item/lasso.png"),
                                  GlobalInfo.CHARACTER_SCALING)

        row = 0
        for line in GameMap.PUBLIC_MAP:
            col = 0
            for ascii in line:
                ground_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                              EnumTypes.ImageType.GROUND),
                                              GlobalInfo.CHARACTER_SCALING)
                ground_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                ground_sprite.left = col * GlobalInfo.IMAGE_SIZE
                self.ground_list.append(ground_sprite)
                if ascii == GlobalInfo.WALL:
                    wall_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                EnumTypes.ImageType.WALL),
                                                GlobalInfo.CHARACTER_SCALING)
                    wall_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    wall_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.wall_list.append(wall_sprite)
                elif ascii == "w":
                    water_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                 EnumTypes.ImageType.WATER),
                                                 GlobalInfo.CHARACTER_SCALING)
                    water_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    water_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.water_list.append(water_sprite)
                elif ascii == "g":
                    grass_sprite = arcade.Sprite(ImageHandler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                 EnumTypes.ImageType.LUSHGROUND),
                                                 GlobalInfo.CHARACTER_SCALING)
                    grass_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    grass_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.grass_list.append(grass_sprite)
                col += 1
            row += 1

        GameMap.place_objects(self.player)
        GameMap.place_objects(self.monster)
        GameMap.place_objects(self.goal)

        self.player_list.append(self.player)
        self.monster_list.append(self.monster)
        self.item_list.append(self.goal)

    def on_draw(self):
        arcade.start_render()

        # screen is drawn in layered order. Items on the topmost layer get called last
        self.ground_list.draw()
        self.wall_list.draw()
        self.item_list.draw()
        self.water_list.draw()
        self.grass_list.draw()
        self.monster_list.draw()

        self.player_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.BLACK, 20)

    def on_update(self, delta_time: float):
        self.player.move()
        if arcade.check_for_collision(self.player, self.goal):
            self.score += 5
            goal_x, goal_y = GameMap.get_random_empty_spot()
            self.goal.top = goal_y * GlobalInfo.IMAGE_SIZE
            self.goal.left = goal_x * GlobalInfo.IMAGE_SIZE

        self.player.account_for_collision_list(arcade.check_for_collision_with_list(self.player, self.wall_list))

        viewport_changed = False

        # Scroll left
        left_boundary = self.view_left + self.viewport_margin_hort
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            viewport_changed = True

        # Scroll right
        right_boundary = self.view_left + self.screen_width - self.viewport_margin_hort
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            viewport_changed = True

        # Scroll up
        top_boundary = self.view_bottom + self.screen_height - self.viewport_margin_vert
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            viewport_changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + self.viewport_margin_vert
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
                                self.screen_width + self.view_left,
                                self.view_bottom,
                                self.screen_height + self.view_bottom)

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
            arcade.close_window()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player.up_pressed = False
        elif symbol == arcade.key.DOWN:
            self.player.down_pressed = False
        elif symbol == arcade.key.LEFT:
            self.player.left_pressed = False
        elif symbol == arcade.key.RIGHT:
            self.player.right_pressed = False


def main():
    window = MainWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
