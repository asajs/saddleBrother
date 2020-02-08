from random import shuffle

class MazeGenerator:
    def __init__(self, wall, empty):
        self.wall = wall
        self.empty = empty

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
                    maze[(i, j)] = self.empty
                else:
                    maze[(i, j)] = self.wall

        # Fill in border.
        for i in range(rows):
            maze[(i, 0)] = self.wall
            maze[(i, cols - 1)] = self.wall
        for j in range(cols):
            maze[(0, j)] = self.wall
            maze[(rows - 1, j)] = self.wall

        for i in range(rows):
            for j in range(cols):
                if maze[(i, j)] == self.empty:
                    spaceCells.add((i, j))
                if maze[(i, j)] == self.wall:
                    walls.add((i, j))

        # Prim's algorithm to knock down walls.
        originalSize = len(spaceCells)
        connected.add((1, 1))
        while len(connected) < len(spaceCells):
            doA, doB = None, None
            cns = list(connected)
            shuffle(cns)
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
            maze[A] = self.empty
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