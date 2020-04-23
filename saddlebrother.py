from os import path, chdir
import arcade
import random
import Character
import CellularAutomata
import ImageHandler
import EnumTypes
import GlobalInfo


def insert_symbol_into_random_empty_spot(map, symbol):
    x = 0
    y = 0
    while map[y][x] != ' ':
        y = random.randrange(2, len(map))
        x = random.randrange(1, len(map[0]))
    map[y] = map[y][:x] + symbol + map[y][x + 1:]
    return x, y


def remove_symbol_from_map(x, y, map):
    map[y] = map[y][:x] + GlobalInfo.EMPTY + map[y][x + 1:]


def get_path(file):
    return path.abspath(file)


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

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.viewport_margin_hort = screen_width / 2 - GlobalInfo.IMAGE_SIZE * 2
        self.viewport_margin_vert = screen_height / 2 - GlobalInfo.IMAGE_SIZE * 2

        self.map = None
        self.player = None
        self.player = None
        self.goal_sprite = None
        self.image_handler = ImageHandler.ImageHandler()

        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.water_list = arcade.SpriteList()
        self.grass_list = arcade.SpriteList()
        self.score = 0

        map = CellularAutomata.CellularAutomata(GlobalInfo.WALL, GlobalInfo.EMPTY)
        # max_tile_wide = int((SCREEN_WIDTH - (SCREEN_WIDTH % IMAGE_SIZE)) / IMAGE_SIZE)
        # max_tile_high = int((SCREEN_HEIGHT - (SCREEN_HEIGHT % IMAGE_SIZE)) / IMAGE_SIZE)
        self.map = map.generate(GlobalInfo.MAP_COUNT_X, GlobalInfo.MAP_COUNT_Y)

        self.player = Character.Character(self.image_handler.get_path("Images/saddlebrother.png"))
        insert_symbol_into_random_empty_spot(self.map, GlobalInfo.AGENT)
        insert_symbol_into_random_empty_spot(self.map, GlobalInfo.GOAL)

        row = 0
        for line in self.map:
            col = 0
            for ascii in line:
                ground_sprite = arcade.Sprite(self.image_handler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                    EnumTypes.ImageType.GROUND),
                                              GlobalInfo.CHARACTER_SCALING)
                ground_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                ground_sprite.left = col * GlobalInfo.IMAGE_SIZE
                self.ground_list.append(ground_sprite)
                if ascii == GlobalInfo.WALL:
                    wall_sprite = arcade.Sprite(self.image_handler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                      EnumTypes.ImageType.WALL),
                                                GlobalInfo.CHARACTER_SCALING)
                    wall_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    wall_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.wall_list.append(wall_sprite)
                elif ascii == GlobalInfo.GOAL:
                    self.goal_sprite = arcade.Sprite(self.image_handler.get_specific("desert/item/lasso.png"),
                                                     GlobalInfo.CHARACTER_SCALING)
                    self.goal_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    self.goal_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.item_list.append(self.goal_sprite)
                elif ascii == GlobalInfo.AGENT:
                    self.player.bottom = row * GlobalInfo.IMAGE_SIZE
                    self.player.left = col * GlobalInfo.IMAGE_SIZE
                    self.player_list.append(self.player)
                elif ascii == "w":
                    water_sprite = arcade.Sprite(self.image_handler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                       EnumTypes.ImageType.WATER),
                                                 GlobalInfo.CHARACTER_SCALING)
                    water_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    water_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.water_list.append(water_sprite)
                elif ascii == "g":
                    grass_sprite = arcade.Sprite(self.image_handler.get_random_of_type(EnumTypes.ZoneType.DESERT,
                                                                                       EnumTypes.ImageType.LUSHGROUND),
                                                 GlobalInfo.CHARACTER_SCALING)
                    grass_sprite.bottom = row * GlobalInfo.IMAGE_SIZE
                    grass_sprite.left = col * GlobalInfo.IMAGE_SIZE
                    self.grass_list.append(grass_sprite)
                col += 1
            row += 1

    def on_draw(self):
        arcade.start_render()

        # screen is drawn in layered order. Items on the topmost layer get called last
        self.ground_list.draw()
        self.wall_list.draw()
        self.item_list.draw()
        self.water_list.draw()
        self.grass_list.draw()

        self.player_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.BLACK, 20)

    def on_update(self, delta_time: float):
        self.player.move()
        if arcade.check_for_collision(self.player, self.goal_sprite):
            self.score += 5
            goal_x, goal_y = insert_symbol_into_random_empty_spot(self.map, GlobalInfo.GOAL)
            self.goal_sprite.top = goal_y * GlobalInfo.IMAGE_SIZE
            self.goal_sprite.left = goal_x * GlobalInfo.IMAGE_SIZE

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

        # self.player.update_movement(up, down, left, right)

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
