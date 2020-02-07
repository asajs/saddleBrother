from os import path, chdir
import arcade
import heapq
import random

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


class Character:
    def __init__(self, symbol):
        self.symbol = symbol
        self.x = 0
        self.y = 0

    def move(self, input, map):
        input = str(input).lower()
        if input == "w" and self.y + 1 < len(map) and map[self.y + 1][self.x] != WALL:
            self.y += 1
        elif input == "a" and self.x - 1 > 0 and map[self.y][self.x - 1] != WALL:
            self.x -= 1
        elif input == "s" and self.y - 1 > 0 and map[self.y - 1][self.x] != WALL:
            self.y -= 1
        elif input == "d" and self.x + 1 < len(map[self.y]) and map[self.y][self.x + 1] != WALL:
            self.x += 1


class MazeGenerator:
    @staticmethod
    def adjacent(cell):
        i, j = cell
        for (y, x) in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            yield (i + y, j + x), (i + 2 * y, j + 2 * x)

    @staticmethod
    def generate(self, width, height):
        """Generates a maze as a list of strings.
           :param width: the width of the maze, not including border walls.
           :param height: height of the maze, not including border walls.
        """
        # add 1 for border walls.

        width += 1
        height += 1
        rows, cols = height, width

        maze = {}

        spaceCells = set()
        connected = set()
        walls = set()

        # Initialize with grid.
        for i in range(rows):
            for j in range(cols):
                if (i % 2 == 1) and (j % 2 == 1):
                    maze[(i, j)] = EMPTY
                else:
                    maze[(i, j)] = WALL

        # Fill in border.
        for i in range(rows):
            maze[(i, 0)] = WALL
            maze[(i, cols - 1)] = WALL
        for j in range(cols):
            maze[(0, j)] = WALL
            maze[(rows - 1, j)] = WALL

        for i in range(rows):
            for j in range(cols):
                if maze[(i, j)] == EMPTY:
                    spaceCells.add((i, j))
                if maze[(i, j)] == WALL:
                    walls.add((i, j))

        # Prim's algorithm to knock down walls.
        originalSize = len(spaceCells)
        connected.add((1, 1))
        while len(connected) < len(spaceCells):
            doA, doB = None, None
            cns = list(connected)
            random.shuffle(cns)
            for (i, j) in cns:
                if doA is not None: break
                for A, B in self.adjacent((i, j)):
                    if A not in walls:
                        continue
                    if (B not in spaceCells) or (B in connected):
                        continue
                    doA, doB = A, B
                    break
            A, B = doA, doB
            maze[A] = EMPTY
            walls.remove(A)
            spaceCells.add(A)
            connected.add(A)
            connected.add(B)
            # if verbose:
            #     cs, ss = len(connected), len(spaceCells)
            #     cs += (originalSize - ss)
            #     ss += (originalSize - ss)
            #     if cs % 10 == 1:
            #         print('%s/%s cells connected ...' % (cs, ss), file=sys.stderr)

        lines = []
        for i in range(rows):
            lines.append(''.join(maze[(i, j)] for j in range(cols)))

        return lines


class CellularAutomata:
    def __init__(self):
        self.number_of_steps = 2
        self.chance_to_stay_alive = 0.4
        self.death_limit = 3
        self.birth_limit = 4

    @staticmethod
    def create_grid(width, height):
        """ Create a two-dimensional grid of specified size. """
        return [[0 for _x in range(width)] for _y in range(height)]

    def initialize_grid(self, grid):
        """ Randomly set grid locations to on/off based on chance. """
        height = len(grid)
        width = len(grid[0])
        for row in range(height):
            for column in range(width):
                if random.random() <= self.chance_to_stay_alive:
                    grid[row][column] = 1

    @staticmethod
    def count_alive_neighbors(grid, x, y):
        """ Count neighbors that are alive. """
        height = len(grid)
        width = len(grid[0])
        alive_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x = x + i
                neighbor_y = y + j
                if i == 0 and j == 0:
                    continue
                elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= height or neighbor_x >= width:
                    # Edges are considered alive. Makes map more likely to appear naturally closed.
                    alive_count += 1
                elif grid[neighbor_y][neighbor_x] == 1:
                    alive_count += 1
        return alive_count

    def do_simulation_step(self, old_grid):
        """ Run a step of the cellular automaton. """
        height = len(old_grid)
        width = len(old_grid[0])
        new_grid = self.create_grid(width, height)
        for x in range(width):
            for y in range(height):
                alive_neighbors = self.count_alive_neighbors(old_grid, x, y)
                if old_grid[y][x] == 1:
                    if alive_neighbors < self.death_limit:
                        new_grid[y][x] = 0
                    else:
                        new_grid[y][x] = 1
                else:
                    if alive_neighbors > self.birth_limit:
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0
        return new_grid

    def generate(self, width, height):
        automata_map = self.create_grid(width, height)
        self.initialize_grid(automata_map)
        for step in range(self.number_of_steps):
            automata_map = self.do_simulation_step(automata_map)

        ascii_map = self.make_ascii_map(automata_map)
        self.validate_map(ascii_map)
        return ascii_map

    @staticmethod
    def make_ascii_map(automata_map):
        ascii_map = list()
        for row in range(len(automata_map)):
            temp_row = list()
            for col in range(len(automata_map[0])):
                if automata_map[row][col] == 1:
                    temp_row.append("#")
                else:
                    temp_row.append(" ")
            ascii_row = ''.join(temp_row)
            ascii_map.append(ascii_row)
        return ascii_map

    def validate_map(self, ascii_map):
        unvisited = set()
        visited = set()
        local = set()
        for _y in range(len(ascii_map)):
            for _x in range(len(ascii_map[0])):
                if ascii_map[_y][_x] == " ":
                    unvisited.add((_y, _x))


        while len(unvisited) > 0:
            coord = unvisited.pop()
            # wander around a local space to see if we can reach every corner
            while True:
                self.helper_for_sets((coord[0] + 1, coord[1]), unvisited, visited, local)
                self.helper_for_sets((coord[0] - 1, coord[1]), unvisited, visited, local)
                self.helper_for_sets((coord[0], coord[1] + 1), unvisited, visited, local)
                self.helper_for_sets((coord[0], coord[1] - 1), unvisited, visited, local)
                if len(local) == 0:
                    break
                coord = local.pop()

            # we failed to reach every corner if this is true
            if len(unvisited) > 0:
                # now to make paths in the map to another corner
                # don't forget to add them back in
                visited_coord = visited.pop()
                visited.add(visited_coord)
                unvisited_coord = unvisited.pop()
                unvisited.add(unvisited_coord)
                self.make_paths_in_map(ascii_map, visited_coord, unvisited_coord)
                # This is ugly and gross, but I'm just curious... Rational: the map is different now
                unvisited.clear()
                visited.clear()
                for _y in range(len(ascii_map)):
                    for _x in range(len(ascii_map[0])):
                        if ascii_map[_y][_x] == " ":
                            unvisited.add((_y, _x))

    def make_paths_in_map(self, ascii_map, visited_coord, unvisited_coord):
        # first "walk" the coordinates to each other
        visited_coord = self.greedy_best_search(visited_coord, unvisited_coord, ascii_map)
        unvisited_coord = self.greedy_best_search(unvisited_coord, visited_coord, ascii_map)
        vy = visited_coord[0]
        vx = visited_coord[1]
        uy = unvisited_coord[0]
        ux = unvisited_coord[1]
        while vy != uy or vx != ux:
            if vy < uy:
                vy += 1
                ascii_map[vy] = ascii_map[vy][:vx] + " " + ascii_map[vy][vx + 1:]
            elif vy > uy:
                vy -= 1
                ascii_map[vy] = ascii_map[vy][:vx] + " " + ascii_map[vy][vx + 1:]
            if vx < ux:
                vx += 1
                ascii_map[vy] = ascii_map[vy][:vx] + " " + ascii_map[vy][vx + 1:]
            elif vx > ux:
                vx -= 1
                ascii_map[vy] = ascii_map[vy][:vx] + " " + ascii_map[vy][vx + 1:]

    @staticmethod
    def manhattan_distance(x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def greedy_best_search(self, start, goal, ascii_map):
        i = 0
        frontier = []
        heapq.heappush(frontier, [0, i, start])
        best_so_far = (self.manhattan_distance(start, goal), start)
        came_from = {}
        came_from[start] = None

        while len(frontier) > 0:
            _, _, current = heapq.heappop(frontier)

            neighbors = list()

            if current[0] - 1 > 0 and ascii_map[current[0] - 1][current[1]] == " ":
                neighbors.append((current[0] - 1, current[1]))
            if current[0] + 1 < len(ascii_map) and ascii_map[current[0] + 1][current[1]] == " ":
                neighbors.append((current[0] + 1, current[1]))
            if current[1] - 1 > 0 and ascii_map[current[0]][current[1] - 1] == " ":
                neighbors.append((current[0], current[1] - 1))
            if current[1] + 1 < len(ascii_map[current[0]]) and ascii_map[current[0]][current[1] + 1] == " ":
                neighbors.append((current[0], current[1] + 1))

            for next in neighbors:
                if next not in came_from:
                    i += 1
                    priority = self.manhattan_distance(next, goal)
                    if priority < best_so_far[0]:
                        best_so_far = (priority, current)
                    heapq.heappush(frontier, [priority, i, next])
                    came_from[next] = current

        return best_so_far[1]

    @staticmethod
    def helper_for_sets(coord, unvisited, visited, local):
        if coord in unvisited:
            unvisited.remove(coord)
            if coord not in visited:
                visited.add(coord)
                local.add(coord)


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

        map = CellularAutomata()
        # max_tile_wide = int((SCREEN_WIDTH - (SCREEN_WIDTH % IMAGE_SIZE)) / IMAGE_SIZE)
        # max_tile_high = int((SCREEN_HEIGHT - (SCREEN_HEIGHT % IMAGE_SIZE)) / IMAGE_SIZE)
        self.map = map.generate(40, 40)

        self.goal = Character(GOAL)
        self.player = Character(AGENT)
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
            self.player.move("w", self.map)
            self.player_sprite.top = self.player.y * IMAGE_SIZE
        elif symbol == arcade.key.DOWN:
            self.player.move("s", self.map)
            self.player_sprite.top = self.player.y * IMAGE_SIZE
        elif symbol == arcade.key.LEFT:
            self.player.move("a", self.map)
            self.player_sprite.left = self.player.x * IMAGE_SIZE
        elif symbol == arcade.key.RIGHT:
            self.player.move("d", self.map)
            self.player_sprite.left = self.player.x * IMAGE_SIZE


def main():
    window = MainWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
