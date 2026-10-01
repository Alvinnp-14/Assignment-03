from PIL import Image, ImageDraw


class ImageProcessor:
    def __init__(self, display_size=500):
        self.display_size = display_size

    def prepare_image(self, image, grid_size):
        image = image.convert("RGB")
        image = self.resize_to_fit(image)
        image = self.crop_to_grid(image, grid_size)
        return image

    def resize_to_fit(self, image):
        width, height = image.size

        if width > height:
            new_width = self.display_size
            new_height = int(height * self.display_size / width)
        else:
            new_height = self.display_size
            new_width = int(width * self.display_size / height)

        return image.resize((new_width, new_height))

    def crop_to_grid(self, image, grid_size):
        width, height = image.size

        new_width = width - (width % grid_size)
        new_height = height - (height % grid_size)

        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height

        return image.crop((left, top, right, bottom))

    def draw_grid(self, image, grid_size):
        image_with_grid = image.copy()
        draw = ImageDraw.Draw(image_with_grid)

        width, height = image_with_grid.size
        tile_width = width // grid_size
        tile_height = height // grid_size

        grid_color = (180, 180, 180)

        for i in range(1, grid_size):
            x = i * tile_width
            draw.line((x, 0, x, height), fill=grid_color, width=1)

            y = i * tile_height
            draw.line((0, y, width, y), fill=grid_color, width=1)

        return image_with_grid
