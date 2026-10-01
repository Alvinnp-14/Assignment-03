import random


class PuzzleBoard:
    def __init__(self, tiles, grid_size):
        self.tiles = tiles
        self.grid_size = grid_size
        self.solved = False

    def scramble(self):
        transformation_count = self.get_transformation_count()

        for _ in range(transformation_count):
            transformation = random.choice(["swap", "rotate", "flip"])

            if transformation == "swap":
                self.random_swap()
            elif transformation == "rotate":
                self.random_rotate()
            elif transformation == "flip":
                self.random_flip()

        self.update_tile_positions()
        self.solved = self.is_solved()

    def get_transformation_count(self):
        if self.grid_size == 3:
            return 6

        if self.grid_size == 4:
            return 12

        if self.grid_size == 5:
            return 20

        return self.grid_size * self.grid_size

    def random_swap(self):
        row1 = random.randint(0, self.grid_size - 1)
        col1 = random.randint(0, self.grid_size - 1)

        row2 = random.randint(0, self.grid_size - 1)
        col2 = random.randint(0, self.grid_size - 1)

        while row1 == row2 and col1 == col2:
            row2 = random.randint(0, self.grid_size - 1)
            col2 = random.randint(0, self.grid_size - 1)

        self.swap_tiles(row1, col1, row2, col2)

    def random_rotate(self):
        row = random.randint(0, self.grid_size - 1)
        col = random.randint(0, self.grid_size - 1)

        rotations = random.choice([1, 2, 3])

        for _ in range(rotations):
            self.tiles[row][col].rotate_clockwise()

    def random_flip(self):
        row = random.randint(0, self.grid_size - 1)
        col = random.randint(0, self.grid_size - 1)

        self.tiles[row][col].flip_horizontal()

    def swap_tiles(self, row1, col1, row2, col2):
        self.tiles[row1][col1], self.tiles[row2][col2] = (
            self.tiles[row2][col2],
            self.tiles[row1][col1],
        )

        self.update_tile_positions()

    def rotate_tile(self, row, col):
        self.tiles[row][col].rotate_clockwise()
        self.solved = self.is_solved()

    def flip_tile(self, row, col):
        self.tiles[row][col].flip_horizontal()
        self.solved = self.is_solved()

    def update_tile_positions(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                tile = self.tiles[row][col]
                tile.current_row = row
                tile.current_col = col

    def count_incorrect_tiles(self):
        incorrect_count = 0

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if not self.tiles[row][col].is_correct():
                    incorrect_count += 1

        return incorrect_count

    def is_solved(self):
        return self.count_incorrect_tiles() == 0

    def solve(self):
        solved_tiles = []

        for row in range(self.grid_size):
            solved_row = []

            for col in range(self.grid_size):
                for search_row in range(self.grid_size):
                    for search_col in range(self.grid_size):
                        tile = self.tiles[search_row][search_col]

                        if tile.original_row == row and tile.original_col == col:
                            tile.current_row = row
                            tile.current_col = col
                            tile.rotation = 0
                            tile.flipped = False
                            solved_row.append(tile)

            solved_tiles.append(solved_row)

        self.tiles = solved_tiles
        self.solved = True
