import random
import heapq
import GlobalInfo


class CellularAutomata:
    def __init__(self):
        self.number_of_steps = 2
        self.chance_to_stay_alive = 0.35
        self.death_limit = 3
        self.birth_limit = 4

        self.__empty = 0
        self.__wall = 1
        self.__water = 2
        self.__grass = 3

    def generate(self, width, height):
        """Generate a map and return it in ascii characters"""
        automata_map = self.__create_grid(width, height)
        self.__initialize_grid(automata_map)
        for step in range(self.number_of_steps):
            automata_map = self.__do_simulation_step(automata_map)

        set_of_validated = self.__validate_map(automata_map)
        self.__add_oasis(automata_map, set_of_validated)
        ascii_map = self.__make_ascii_map(automata_map)
        return ascii_map

    def __initialize_grid(self, grid):
        """ Randomly set grid locations to on/off based on chance. """
        height = len(grid)
        width = len(grid[0])
        for row in range(height):
            for column in range(width):
                if random.random() <= self.chance_to_stay_alive:
                    grid[row][column] = 1

    def __do_simulation_step(self, old_grid):
        """ Run a step of the cellular automaton. """
        height = len(old_grid)
        width = len(old_grid[0])
        new_grid = self.__create_grid(width, height)
        for x in range(width):
            for y in range(height):
                alive_neighbors = self.__count_alive_neighbors(old_grid, x, y)
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

    def __make_ascii_map(self, automata_map):
        """Convert the map from 0, 1, to the chosen empty ascii character and the chosen ascii wall character"""
        ascii_map = list()
        height_of_map = len(automata_map)
        width_of_map = len(automata_map[0])
        for row in range(height_of_map):
            temp_row = list()
            for col in range(width_of_map):
                if automata_map[row][col] == self.__wall:
                    temp_row.append(GlobalInfo.WALL)
                elif automata_map[row][col] == self.__empty:
                    temp_row.append(GlobalInfo.EMPTY)
                elif automata_map[row][col] == self.__water:
                    temp_row.append(GlobalInfo.WATER)
                elif automata_map[row][col] == self.__grass:
                    temp_row.append(GlobalInfo.GRASS)
            ascii_row = ''.join(temp_row)
            ascii_map.append(ascii_row)
        return ascii_map

    def __validate_map(self, automata_map):
        """Make sure that every empty spot can be visited"""
        height_of_map = len(automata_map)
        width_of_map = len(automata_map[0])

        list_of_areas = list()
        unvisited = set()
        visited = set()
        local = set()
        for _y in range(height_of_map):
            for _x in range(width_of_map):
                if automata_map[_y][_x] == self.__empty:
                    unvisited.add((_y, _x))

        while len(unvisited) > 0:
            coord = unvisited.pop()
            visited.add(coord)
            # wander around a local space to see if we can reach every corner
            while True:
                self.__helper_for_sets((coord[0] + 1, coord[1]), unvisited, visited, local)
                self.__helper_for_sets((coord[0] - 1, coord[1]), unvisited, visited, local)
                self.__helper_for_sets((coord[0], coord[1] + 1), unvisited, visited, local)
                self.__helper_for_sets((coord[0], coord[1] - 1), unvisited, visited, local)
                if len(local) == 0:
                    break
                coord = local.pop()

            list_of_areas.append(visited)
            visited = set()

        list_of_areas.sort(key=lambda x: len(x), reverse=True)

        set_largest = list_of_areas[0]

        while len(list_of_areas) > 1:
            # Grab largest and second largest sets and try to connect them
            set_largest = list_of_areas[0]
            set_second_largest = list_of_areas[1]

            largest_set_coord = set_largest.pop()
            set_largest.add(largest_set_coord)
            second_largest_set_coord = set_second_largest.pop()
            set_second_largest.add(second_largest_set_coord)
            set_new = self.__make_paths_in_map(automata_map, largest_set_coord, second_largest_set_coord)

            set_largest.union(set_second_largest)
            set_largest.union(set_new)
            list_of_areas.pop(1)

        return set_largest

    def __make_paths_in_map(self, automata_map, visited_coord, unvisited_coord):
        """Make holes in the walls of the map from two coordinates"""
        # first "walk" the coordinates to each other
        newly_made_area = set()
        unvisited_coord = self.__greedy_best_search(unvisited_coord, visited_coord, automata_map)
        visited_coord = self.__greedy_best_search(visited_coord, unvisited_coord, automata_map)
        vy = visited_coord[0]
        vx = visited_coord[1]
        uy = unvisited_coord[0]
        ux = unvisited_coord[1]
        # then delete them
        while vy != uy or vx != ux:
            if vy < uy:
                vy += 1
            elif vy > uy:
                vy -= 1
            automata_map[vy][vx] = self.__empty
            newly_made_area.add((vy, vx))

            if vx < ux:
                vx += 1
            elif vx > ux:
                vx -= 1
            newly_made_area.add((vy, vx))
            automata_map[vy][vx] = self.__empty
            self.__random_walk(automata_map, vy, vx, self.__empty, 2, 3)
        return newly_made_area

    def __random_walk(self, automata_map, vy, vx, tile, min, max):
        """Randomly move from a specified coordinate"""
        height_of_map = len(automata_map)
        width_of_map = len(automata_map[0])
        y = vy
        x = vx
        number_of_steps = random.randrange(min, max)
        while number_of_steps > 0:
            y = self.__clamp(random.randrange(-1, 1) + y, height_of_map, 0)
            automata_map[y][x] = tile
            x = self.__clamp(random.randrange(-1, 1) + x, width_of_map, 0)
            automata_map[y][x] = tile
            number_of_steps -= 1

    def __greedy_best_search(self, start, goal, automata_map):
        """Look for the shortest path between to points. Returns the coordinate that gets the closest"""
        height_of_map = len(automata_map)
        width_of_map = len(automata_map[0])
        i = 0
        frontier = []
        heapq.heappush(frontier, [0, i, start])
        best_so_far = (self.__manhattan_distance(start, goal), start)
        came_from = {}
        came_from[start] = None
        iterations_without_improvement = 0

        while len(frontier) > 0:
            iterations_without_improvement += 1
            _, _, current = heapq.heappop(frontier)

            neighbors = list()

            if current[0] - 1 > 0 and automata_map[current[0] - 1][current[1]] == self.__empty:
                neighbors.append((current[0] - 1, current[1]))
            if current[0] + 1 < height_of_map and automata_map[current[0] + 1][current[1]] == self.__empty:
                neighbors.append((current[0] + 1, current[1]))
            if current[1] - 1 > 0 and automata_map[current[0]][current[1] - 1] == self.__empty:
                neighbors.append((current[0], current[1] - 1))
            if current[1] + 1 < width_of_map and automata_map[current[0]][current[1] + 1] == self.__empty:
                neighbors.append((current[0], current[1] + 1))

            for next in neighbors:
                if next not in came_from:
                    i += 1
                    priority = self.__manhattan_distance(next, goal)
                    if priority < best_so_far[0]:
                        best_so_far = (priority, current)
                        iterations_without_improvement = 0
                    heapq.heappush(frontier, [priority, i, next])
                    came_from[next] = current
            if iterations_without_improvement > 50:
                break

        return best_so_far[1]

    def __add_oasis(self, automata_map, set_of_validated):
        """Pick random spot not too near the edge and add oasis"""
        lowest_allowed = len(automata_map) / 10
        highest_allowed = len(automata_map) - lowest_allowed
        leftest_allowed = len(automata_map[0]) / 10
        rightest_allowed = len(automata_map[0]) - leftest_allowed
        coord = set_of_validated.pop()
        set_of_validated.add(coord)
        while coord[0] < lowest_allowed or coord[0] > highest_allowed and coord[1] < leftest_allowed or coord[1] > rightest_allowed:
            coord = set_of_validated.pop()
            set_of_validated.add(coord)

        width_of_oasis = random.randrange(int(len(automata_map) / 20), int(len(automata_map) / 10) - 1)
        height_of_oasis = random.randrange(int(len(automata_map[0]) / 20), int(len(automata_map[0]) / 10) - 1)

        x_start = coord[0] - height_of_oasis
        x_end = coord[0] + width_of_oasis
        y_start = coord[1] - height_of_oasis
        y_end = coord[1] + height_of_oasis
        i = x_start
        while i < x_end:
            automata_map[i][y_start:y_end] = [2] * (y_end - y_start)
            i += 1
        self.__add_grass(automata_map, x_start, x_end, y_start, y_end)

    def __add_grass(self, automata_map, x_start, x_end, y_start, y_end):
        list_top_x = [(x, y_start - 1) for x in range(x_start - 1, x_end + 1)]
        list_bottom_x = [(x, y_end + 1) for x in range(x_start - 1, x_end + 1)]
        list_left_y = [(x_start - 1, y) for y in range(y_start - 1, y_end + 2)]
        list_right_y = [(x_end, y) for y in range(y_start - 1, y_end + 2)]
        unique_tuples = set(list_top_x + list_bottom_x + list_left_y + list_right_y)

        while len(unique_tuples) > 0:
            coord = unique_tuples.pop()
            automata_map[coord[0]][coord[1]] = self.__grass
            self.__random_walk(automata_map, coord[0], coord[1], self.__grass, 1, 3)


    @staticmethod
    def __count_alive_neighbors(grid, x, y):
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

    @staticmethod
    def __create_grid(width, height):
        """ Create a two-dimensional grid of specified size. """
        return [[0 for _x in range(width)] for _y in range(height)]

    @staticmethod
    def __clamp(number, max, min):
        """Make sure a number does not exceed its bounds"""
        if number > max:
            return max
        elif number < min:
            return min
        return number

    @staticmethod
    def __manhattan_distance(x, y):
        """Return the manhattan distance"""
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    @staticmethod
    def __helper_for_sets(coord, unvisited, visited, local):
        """Remove a coord from unvisited and add it to visited"""
        if coord in unvisited:
            unvisited.remove(coord)
            if coord not in visited:
                visited.add(coord)
                local.add(coord)
