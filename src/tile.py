from PIL import Image


class Tile:
    def __init__(self, image, original_row, original_col):
        self.original_image = image.copy()
        self.image = image.copy()

        self.original_row = original_row
        self.original_col = original_col

        self.current_row = original_row
        self.current_col = original_col

        self.rotation = 0
        self.flipped = False

    def rotate_clockwise(self):
        self.rotation = (self.rotation + 90) % 360
        self.update_image()

    def flip_horizontal(self):
        self.flipped = not self.flipped
        self.update_image()

    def update_image(self):
        image = self.original_image.copy()

        if self.flipped:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        if self.rotation != 0:
            image = image.rotate(-self.rotation, expand=False)

        self.image = image

    def reset_orientation(self):
        self.rotation = 0
        self.flipped = False
        self.update_image()

    def is_correct(self):
        return (
            self.current_row == self.original_row
            and self.current_col == self.original_col
            and self.rotation == 0
            and not self.flipped
        )
