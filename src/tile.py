class Tile:
    def __init__(self, image, original_row, original_col):
        self.image = image
        self.original_row = original_row
        self.original_col = original_col

        self.current_row = original_row
        self.current_col = original_col

        self.rotation = 0
        self.flipped = False

    def rotate_clockwise(self):
        self.rotation = (self.rotation + 90) % 360
        self.image = self.image.rotate(-90, expand=False)

    def flip_horizontal(self):
        self.flipped = not self.flipped
        self.image = self.image.transpose(method=0)

    def is_correct(self):
        return (
            self.current_row == self.original_row
            and self.current_col == self.original_col
            and self.rotation == 0
            and not self.flipped
        )
