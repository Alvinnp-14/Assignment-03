# HIT137 Assignment 3 - Image Puzzle Application

## Overview

This project is a desktop image puzzle game created for HIT137 Assignment 3. The application loads an image, splits it into a grid of tiles, scrambles the tiles using transformations, and allows the player to restore the original image.

The application is built using Python, Tkinter, Pillow, and object-oriented programming principles.

## Features

- Load JPG, PNG, and BMP images from disk.
- Choose a grid size before loading:
  - 3 x 3
  - 4 x 4
  - 5 x 5
- Display the original image on the left.
- Display the transformed puzzle image on the right.
- Scramble the puzzle using:
  - tile swaps
  - 90, 180, and 270 degree rotations
  - horizontal flips
- Draw grid lines over the puzzle image.
- Select and swap tiles using left click.
- Rotate tiles using right click.
- Flip tiles using Shift + left click.
- Track moves and incorrect tiles.
- Show green ticks on correctly positioned and correctly oriented tiles.
- Provide up to three hints per image.
- Solve the puzzle instantly with the Solve button.
- Stop puzzle input when the puzzle is solved.

## Controls

| Action | Control |
|---|---|
| Select tile | Left click |
| Swap tiles | Left click one tile, then left click another tile |
| Deselect tile | Left click the selected tile again |
| Rotate tile | Right click |
| Flip tile horizontally | Shift + left click |
| Use hint | Hint button |
| Solve puzzle | Solve button |

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
