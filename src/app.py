import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


class PuzzleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HIT137 Image Puzzle")
        self.root.geometry("1200x750")

        self.original_image = None
        self.original_tk_image = None
        self.puzzle_tk_image = None

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

        image = Image.open(file_path).convert("RGB")
        image = self.resize_for_display(image)

        self.original_image = image

        self.original_tk_image = ImageTk.PhotoImage(image)
        self.puzzle_tk_image = ImageTk.PhotoImage(image)

        self.original_label.config(image=self.original_tk_image, text="")
        self.puzzle_label.config(image=self.puzzle_tk_image, text="")

        grid = self.grid_size.get()
        total_tiles = grid * grid

        self.status_label.config(
            text=f"Moves: 0 | Incorrect tiles: {total_tiles} | Hints left: 3"
        )

    def resize_for_display(self, image):
        max_size = 500
        width, height = image.size

        if width > height:
            new_width = max_size
            new_height = int(height * max_size / width)
        else:
            new_height = max_size
            new_width = int(width * max_size / height)

        return image.resize((new_width, new_height))

    def run(self):
        self.root.mainloop()
