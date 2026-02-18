import cv2              # OpenCV library for drawing shapes on images
import numpy as np       # NumPy for numerical operations and arrays

# =============================
# SHAPE DRAWING FUNCTIONS
# =============================

# ----------- CIRCLE -----------
def draw_circle(img, center, size, color):
    # img    → image/frame where shape will be drawn
    # center → (x, y) center position of the circle
    # size   → radius of the circle
    # color  → BGR color tuple

    cv2.circle(
        img,        # image to draw on
        center,     # center point (x, y)
        size,       # radius
        color,      # fill color
        -1          # -1 means filled circle
    )


# ----------- SQUARE -----------
def draw_square(img, center, size, color):
    # Extract x and y coordinates from center
    x, y = center

    # Draw a filled rectangle (square)
    cv2.rectangle(
        img,                    # image to draw on
        (x - size, y - size),   # top-left corner
        (x + size, y + size),   # bottom-right corner
        color,                  # fill color
        -1                      # -1 means filled rectangle
    )


# ----------- TRIANGLE -----------
def draw_triangle(img, center, size, color):
    # Extract x and y from center
    x, y = center

    # Define 3 points of the triangle
    points = np.array([
        [x, y - size],          # top point
        [x - size, y + size],   # bottom-left point
        [x + size, y + size]    # bottom-right point
    ])

    # Fill the triangle using these points
    cv2.fillPoly(
        img,        # image to draw on
        [points],   # list of points
        color       # fill color
    )


# ----------- TRAPEZIUM -----------
def draw_trapezium(img, center, size, color):
    # Extract center coordinates
    x, y = center

    # Define 4 points of trapezium
    points = np.array([
        [x - size, y - size],        # top-left
        [x + size, y - size],        # top-right
        [x + size // 2, y + size],   # bottom-right (shorter width)
        [x - size // 2, y + size]    # bottom-left (shorter width)
    ])

    # Draw filled trapezium
    cv2.fillPoly(
        img,
        [points],
        color
    )


# ----------- RHOMBUS -----------
def draw_rhombus(img, center, size, color):
    # Extract center coordinates
    x, y = center

    # Define 4 points of rhombus
    points = np.array([
        [x, y - size],      # top
        [x + size, y],      # right
        [x, y + size],      # bottom
        [x - size, y]       # left
    ])

    # Draw filled rhombus
    cv2.fillPoly(
        img,
        [points],
        color
    )


# ----------- PARALLELOGRAM -----------
def draw_parallelogram(img, center, size, color, shear=20):
    # Extract center coordinates
    x, y = center

    # shear → slant value to tilt the parallelogram

    # Define 4 corner points of parallelogram
    points = np.array([
        [x - size + shear, y - size],  # top-left
        [x + size + shear, y - size],  # top-right
        [x + size - shear, y + size],  # bottom-right
        [x - size - shear, y + size]   # bottom-left
    ], dtype=np.int32)

    # Draw filled parallelogram
    cv2.fillPoly(
        img,
        [points],
        color
    )
