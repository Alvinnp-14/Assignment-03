import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

from src.image_processor import ImageProcessor
from src.puzzle import PuzzleBoard


class PuzzleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HIT137 Image Puzzle")
        self.root.geometry("1200x750")

        self.image_processor = ImageProcessor()

        self.original_image = None
        self.puzzle_board = None

        self.original_tk_image = None
        self.puzzle_tk_image = None

        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.input_locked = False

        self.create_widgets()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        self.grid_size = tk.IntVar(value=3)

        ttk.Label(control_frame, text="Grid size:").pack(side=tk.LEFT, padx=5)

        grid_box = ttk.Combobox(
            control_frame,
            textvariable=self.grid_size,
            values=[3, 4, 5],
            width=5,
            state="readonly"
        )
        grid_box.pack(side=tk.LEFT, padx=5)

        load_button = ttk.Button(
            control_frame,
            text="Load Image",
            command=self.load_image
        )
        load_button.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(
            control_frame,
            text="Moves: 0 | Incorrect tiles: 0 | Hints left: 3"
        )
        self.status_label.pack(side=tk.LEFT, padx=20)

        image_frame = ttk.Frame(self.root)
        image_frame.pack(pady=20)

        left_frame = ttk.Frame(image_frame)
        left_frame.pack(side=tk.LEFT, padx=20)

        right_frame = ttk.Frame(image_frame)
        right_frame.pack(side=tk.LEFT, padx=20)

        ttk.Label(
            left_frame,
            text="Original Image",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        ttk.Label(
            right_frame,
            text="Puzzle Image",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        self.original_label = ttk.Label(
            left_frame,
            text="No image loaded",
            borderwidth=2,
            relief="groove"
        )
        self.original_label.pack()

        self.puzzle_label = ttk.Label(
            right_frame,
            text="No image loaded",
            borderwidth=2,
            relief="groove"
        )
        self.puzzle_label.pack()

        self.puzzle_label.bind("<Button-1>", self.handle_left_click)
        self.puzzle_label.bind("<Button-3>", self.handle_right_click)
        self.puzzle_label.bind("<Shift-Button-1>", self.handle_shift_left_click)

        help_label = ttk.Label(
            right_frame,
            text="Left click: select/swap | Right click: rotate | Shift + left click: flip",
            font=("Arial", 9)
        )
        help_label.pack(pady=5)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.hint_button = ttk.Button(
            button_frame,
            text="Hint",
            command=self.use_hint
        )
        self.hint_button.pack(side=tk.LEFT, padx=10)

        self.solve_button = ttk.Button(
            button_frame,
            text="Solve",
            command=self.solve_puzzle
        )
        self.solve_button.pack(side=tk.LEFT, padx=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            return

        grid = self.grid_size.get()

        image = Image.open(file_path)
        self.original_image = self.image_processor.prepare_image(image, grid)

        tiles = self.image_processor.split_into_tiles(self.original_image, grid)

        self.puzzle_board = PuzzleBoard(tiles, grid)
        self.puzzle_board.scramble()

        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.input_locked = False

        self.display_images()
        self.hint_button.config(state=tk.NORMAL)
        self.update_status()

    def display_images(self):
        if self.original_image is None or self.puzzle_board is None:
            return

        puzzle_image = self.image_processor.reassemble_tiles(
            self.puzzle_board.tiles,
            self.puzzle_board.grid_size
        )

        puzzle_image = self.image_processor.draw_grid(
            puzzle_image,
            self.puzzle_board.grid_size
        )

        puzzle_image = self.draw_selected_tile(puzzle_image)
        puzzle_image = self.draw_correct_ticks(puzzle_image)

        self.original_tk_image = ImageTk.PhotoImage(self.original_image)
        self.puzzle_tk_image = ImageTk.PhotoImage(puzzle_image)

        self.original_label.config(image=self.original_tk_image, text="")
        self.puzzle_label.config(image=self.puzzle_tk_image, text="")

    def draw_selected_tile(self, image):
        if self.selected_tile is None or self.puzzle_board is None:
            return image

        image = image.copy()
        row, col = self.selected_tile

        tile_width = image.width // self.puzzle_board.grid_size
        tile_height = image.height // self.puzzle_board.grid_size

        left = col * tile_width
        top = row * tile_height
        right = left + tile_width
        bottom = top + tile_height

        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (left + 2, top + 2, right - 2, bottom - 2),
            outline=(255, 0, 0),
            width=4
        )

        return image

    def draw_correct_ticks(self, image):
        if self.puzzle_board is None:
            return image

        image = image.copy()

        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)

        grid = self.puzzle_board.grid_size
        tile_width = image.width // grid
        tile_height = image.height // grid

        for row in range(grid):
            for col in range(grid):
                tile = self.puzzle_board.tiles[row][col]

                if tile.is_correct():
                    x = col * tile_width
                    y = row * tile_height

                    draw.line(
                        (x + 8, y + 18, x + 18, y + 28),
                        fill=(0, 180, 0),
                        width=4
                    )
                    draw.line(
                        (x + 18, y + 28, x + 34, y + 8),
                        fill=(0, 180, 0),
                        width=4
                    )

        return image

    def get_clicked_tile_position(self, event):
        if self.puzzle_board is None or self.original_image is None:
            return None

        grid = self.puzzle_board.grid_size

        image_width = self.original_image.width
        image_height = self.original_image.height

        if event.x < 0 or event.y < 0:
            return None

        if event.x >= image_width or event.y >= image_height:
            return None

        tile_width = image_width // grid
        tile_height = image_height // grid

        col = event.x // tile_width
        row = event.y // tile_height

        if row >= grid or col >= grid:
            return None

        return row, col

    def handle_left_click(self, event):
        if self.input_locked or self.puzzle_board is None:
            return

        position = self.get_clicked_tile_position(event)

        if position is None:
            return

        if self.selected_tile is None:
            self.selected_tile = position
            self.display_images()
            return

        if self.selected_tile == position:
            self.selected_tile = None
            self.display_images()
            return

        row1, col1 = self.selected_tile
        row2, col2 = position

        self.puzzle_board.swap_tiles(row1, col1, row2, col2)

        self.selected_tile = None
        self.moves += 1

        self.after_player_move()

    def handle_right_click(self, event):
        if self.input_locked or self.puzzle_board is None:
            return

        position = self.get_clicked_tile_position(event)

        if position is None:
            return

        row, col = position
        self.puzzle_board.rotate_tile(row, col)

        self.selected_tile = None
        self.moves += 1

        self.after_player_move()

    def handle_shift_left_click(self, event):
        if self.input_locked or self.puzzle_board is None:
            return

        position = self.get_clicked_tile_position(event)

        if position is None:
            return

        row, col = position
        self.puzzle_board.flip_tile(row, col)

        self.selected_tile = None
        self.moves += 1

        self.after_player_move()

    def after_player_move(self):
        self.display_images()
        self.update_status()

        if self.puzzle_board.is_solved():
            self.input_locked = True
            self.hint_button.config(state=tk.DISABLED)
            messagebox.showinfo(
                "Puzzle complete",
                f"Congratulations! You solved the puzzle in {self.moves} moves."
            )

    def update_status(self):
        if self.puzzle_board is None:
            incorrect_tiles = 0
        else:
            incorrect_tiles = self.puzzle_board.count_incorrect_tiles()

        self.status_label.config(
            text=f"Moves: {self.moves} | Incorrect tiles: {incorrect_tiles} | Hints left: {self.hints_left}"
        )

    def use_hint(self):
        if self.puzzle_board is None or self.input_locked:
            return

        if self.hints_left <= 0:
            self.hint_button.config(state=tk.DISABLED)
            return

        self.hints_left -= 1

        if self.hints_left == 0:
            self.hint_button.config(state=tk.DISABLED)

        self.update_status()

    def solve_puzzle(self):
        if self.puzzle_board is None:
            return

        self.puzzle_board.solve()
        self.moves = 0
        self.hints_left = 3
        self.selected_tile = None
        self.input_locked = True

        self.display_images()
        self.hint_button.config(state=tk.DISABLED)
        self.update_status()

        messagebox.showinfo("Puzzle solved", "The puzzle has been solved.")

    def run(self):
        self.root.mainloop()
