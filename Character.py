class Character:
    def __init__(self, symbol):
        self.symbol = symbol
        self.x = 0
        self.y = 0

    def move(self, input, map, wall):
        input = str(input).lower()
        if input == "w" and self.y + 1 < len(map) and map[self.y + 1][self.x] != wall:
            self.y += 1
        elif input == "a" and self.x > 0 and map[self.y][self.x - 1] != wall:
            self.x -= 1
        elif input == "s" and self.y > 0 and map[self.y - 1][self.x] != wall:
            self.y -= 1
        elif input == "d" and self.x + 1 < len(map[self.y]) and map[self.y][self.x + 1] != wall:
            self.x += 1
