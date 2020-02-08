from os import path, chdir
import arcade
import random
import Character
import CellularAutomata

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Saddle Brother"
CHARACTER_SCALING = 1.0
IMAGE_SIZE = 64.0

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = SCREEN_WIDTH / 2 - IMAGE_SIZE * 2


EMPTY = ' '
WALL = '#'
AGENT = '@'
GOAL = 'x'


def insert_symbol_into_random_empty_spot(map, actor, symbol):
    x = 0
    y = 0
    while map[y][x] != ' ':
        y = random.randrange(2, len(map))
        x = random.randrange(1, len(map[0]))
    map[y] = map[y][:x] + symbol + map[y][x + 1:]
    actor.x = x
    actor.y = y


def remove_symbol_from_map(x, y, map):
    map[y] = map[y][:x] + EMPTY + map[y][x + 1:]


def get_path(file):
    return path.abspath(file)


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.LIGHT_GOLDENROD_YELLOW)

        file_path = path.dirname(path.abspath(__file__))
        chdir(file_path)

        self.score = 0

        self.player_list = None
        self.item_list = None
        self.wall_list = None
        self.ground_list = None

        self.map = None
        self.goal = None
        self.player = None
        self.player_sprite = None
        self.goal_sprite = None

        self.view_bottom = 0
        self.view_left = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.item_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.score = 0

        map = CellularAutomata.CellularAutomata(WALL, EMPTY)
        # max_tile_wide = int((SCREEN_WIDTH - (SCREEN_WIDTH % IMAGE_SIZE)) / IMAGE_SIZE)
        # max_tile_high = int((SCREEN_HEIGHT - (SCREEN_HEIGHT % IMAGE_SIZE)) / IMAGE_SIZE)
        self.map = map.generate(40, 40)

        self.goal = Character.Character(GOAL)
        self.player = Character.Character(AGENT)
        insert_symbol_into_random_empty_spot(self.map, self.player, AGENT)
        insert_symbol_into_random_empty_spot(self.map, self.goal, GOAL)

        row = 0
        for line in self.map:
            col = 0
            for ascii in line:
                ground_sprite = arcade.Sprite(get_path("Images/ground.png"), CHARACTER_SCALING)
                ground_sprite.top = row * IMAGE_SIZE
                ground_sprite.left = col * IMAGE_SIZE
                self.ground_list.append(ground_sprite)
                if ascii == WALL:
                    wall_sprite = arcade.Sprite(get_path("Images/cactus.png"), CHARACTER_SCALING)
                    wall_sprite.top = row * IMAGE_SIZE
                    wall_sprite.left = col * IMAGE_SIZE
                    self.wall_list.append(wall_sprite)
                elif ascii == GOAL:
                    self.goal_sprite = arcade.Sprite(get_path("Images/lasso.png"), CHARACTER_SCALING)
                    self.goal_sprite.top = row * IMAGE_SIZE
                    self.goal_sprite.left = col * IMAGE_SIZE
                    self.item_list.append(self.goal_sprite)
                elif ascii == AGENT:
                    self.player_sprite = arcade.Sprite(get_path("Images/saddlebrother.png"), CHARACTER_SCALING)
                    self.player_sprite.top = row * IMAGE_SIZE
                    self.player_sprite.left = col * IMAGE_SIZE
                    self.player_list.append(self.player_sprite)
                col += 1
            row += 1

    def on_draw(self):
        arcade.start_render()

        self.ground_list.draw()
        self.wall_list.draw()
        self.item_list.draw()
        self.player_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom, arcade.csscolor.BLACK, 20)

    def on_update(self, delta_time: float):
        if arcade.check_for_collision(self.player_sprite, self.goal_sprite):
            self.score += 5
            remove_symbol_from_map(self.goal.x, self.goal.y, self.map)
            insert_symbol_into_random_empty_spot(self.map, self.goal, GOAL)
            self.goal_sprite.top = self.goal.y * IMAGE_SIZE
            self.goal_sprite.left = self.goal.x * IMAGE_SIZE

        viewport_changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            viewport_changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            viewport_changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            viewport_changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            viewport_changed = True

        if viewport_changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.player.move("w", self.map, WALL)
            self.player_sprite.top = self.player.y * IMAGE_SIZE
        elif symbol == arcade.key.DOWN:
            self.player.move("s", self.map, WALL)
            self.player_sprite.top = self.player.y * IMAGE_SIZE
        elif symbol == arcade.key.LEFT:
            self.player.move("a", self.map, WALL)
            self.player_sprite.left = self.player.x * IMAGE_SIZE
        elif symbol == arcade.key.RIGHT:
            self.player.move("d", self.map, WALL)
            self.player_sprite.left = self.player.x * IMAGE_SIZE


def main():
    window = MainWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
