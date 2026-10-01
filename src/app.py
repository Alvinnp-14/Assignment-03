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

        self.original_tk_image = ImageTk.PhotoImage(self.original_image)
        self.puzzle_tk_image = ImageTk.PhotoImage(puzzle_image)

        self.original_label.config(image=self.original_tk_image, text="")
        self.puzzle_label.config(image=self.puzzle_tk_image, text="")

    def update_status(self):
        if self.puzzle_board is None:
            incorrect_tiles = 0
        else:
            incorrect_tiles = self.puzzle_board.count_incorrect_tiles()

        self.status_label.config(
            text=f"Moves: {self.moves} | Incorrect tiles: {incorrect_tiles} | Hints left: {self.hints_left}"
        )

    def use_hint(self):
        if self.puzzle_board is None:
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

        self.display_images()
        self.hint_button.config(state=tk.NORMAL)
        self.update_status()

        messagebox.showinfo("Puzzle solved", "The puzzle has been solved.")

    def run(self):
        self.root.mainloop()
