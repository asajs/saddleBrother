import random
import heapq

class CellularAutomata:
    def __init__(self, wall, empty):
        self.number_of_steps = 2
        self.chance_to_stay_alive = 0.4
        self.death_limit = 3
        self.birth_limit = 4
        self.wall = wall
        self.empty = empty

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

    def make_ascii_map(self, automata_map):
        ascii_map = list()
        for row in range(len(automata_map)):
            temp_row = list()
            for col in range(len(automata_map[0])):
                if automata_map[row][col] == 1:
                    temp_row.append(self.wall)
                else:
                    temp_row.append(self.empty)
            ascii_row = ''.join(temp_row)
            ascii_map.append(ascii_row)
        return ascii_map

    def validate_map(self, ascii_map):
        unvisited = set()
        visited = set()
        local = set()
        for _y in range(len(ascii_map)):
            for _x in range(len(ascii_map[0])):
                if ascii_map[_y][_x] == self.empty:
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
                        if ascii_map[_y][_x] == self.empty:
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
                ascii_map[vy] = ascii_map[vy][:vx] + self.empty + ascii_map[vy][vx + 1:]
            elif vy > uy:
                vy -= 1
                ascii_map[vy] = ascii_map[vy][:vx] + self.empty + ascii_map[vy][vx + 1:]
            if vx < ux:
                vx += 1
                ascii_map[vy] = ascii_map[vy][:vx] + self.empty + ascii_map[vy][vx + 1:]
            elif vx > ux:
                vx -= 1
                ascii_map[vy] = ascii_map[vy][:vx] + self.empty + ascii_map[vy][vx + 1:]

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

            if current[0] - 1 > 0 and ascii_map[current[0] - 1][current[1]] == self.empty:
                neighbors.append((current[0] - 1, current[1]))
            if current[0] + 1 < len(ascii_map) and ascii_map[current[0] + 1][current[1]] == self.empty:
                neighbors.append((current[0] + 1, current[1]))
            if current[1] - 1 > 0 and ascii_map[current[0]][current[1] - 1] == self.empty:
                neighbors.append((current[0], current[1] - 1))
            if current[1] + 1 < len(ascii_map[current[0]]) and ascii_map[current[0]][current[1] + 1] == self.empty:
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
