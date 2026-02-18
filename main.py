# ============================================================
# SHAPE MATCHING DRAG & DROP GAME USING OPENCV
# ============================================================
# STEP 1  : Read the bg img and resize it to 600 * 900
# STEP 2  : Define all shapes that will be used in the game
# STEP 3  : Decide fixed positions for shapes at TOP (source area)
# STEP 4  : Decide fixed positions for shapes at BOTTOM (target slots)
# STEP 5  : Create drawing functions for each shape (imported from utils)
# STEP 6  : Assign unique colors to each shape
# STEP 7  : Track which shapes are correctly placed
# STEP 8  : Handle mouse events:
#           - Left mouse press   → select shape
#           - Mouse move         → drag shape
#           - Left mouse release → drop shape
# STEP 9  : Check if shape is dropped at correct positionQ
# STEP 10 : Update score and lock shape if matched
# STEP 11 : Show timer, score, shapes, and game result
# ============================================================


# ----------------------------
# Import required librariesQ
# ----------------------------
import cv2                  # OpenCV for graphics, mouse, window handling
import numpy as np           # NumPy for creating image arrays
import time                 # Time module for game timer
from utils import *         # Shape drawing functions


# =============================
# BASIC SETTINGS
# =============================
FONT = cv2.FONT_HERSHEY_SIMPLEX   # Font used for text
GAME_TIME = 12                  # Total game duration (seconds)
SHAPE_SIZE = 50                  # Size of each shape


# =============================
# SHAPE LIST
# =============================
shape_names = [
    "Circle", "Square", "Triangle",
    "Trapezium", "Rhombus", "Parallelogram"
]


# =============================
# MAP SHAPES TO DRAW FUNCTIONS
# =============================
shape_drawer = {
    "Circle": draw_circle,
    "Square": draw_square,
    "Triangle": draw_triangle,
    "Trapezium": draw_trapezium,
    "Rhombus": draw_rhombus,
    "Parallelogram": draw_parallelogram
}


# =============================
# TOP SHAPES POSITIONS
# (Source area – draggable shapes)
# =============================
top_positions = {}

for i, shape in enumerate(shape_names):
    if i < 3:
        # First row (3 shapes)
        top_positions[shape] = [270 + i * 200, 90]
    else:
        # Second row (3 shapes)
        top_positions[shape] = [270 + (i - 3) * 200, 210]


# =============================
# BOTTOM TARGET POSITIONS
# (Drop slots)
# =============================
bottom_positions = {}

for i, shape in enumerate(shape_names):
    bottom_positions[shape] = [100 + i * 140, 400]


# =============================
# COLORS FOR SHAPES
# =============================
colors = {
    "Circle": (252, 89, 163),
    "Square": (135, 200, 48),
    "Triangle": (255, 212, 0),
    "Trapezium": (254, 126, 15),
    "Rhombus": (142, 60, 203),
    "Parallelogram": (4, 161, 43)
}


# # =============================
# # GAME STATE VARIABLES
# # =============================
placed = {shape: False for shape in shape_names}  # Track placed shapes
dragged_shape = None                              # Currently dragged shape
mouse_offset = (0, 0)                             # Offset for smooth drag
score = 0                                         # Player score
start_time = time.time()                          # Game start time


# ============================================================
# MOUSE EVENT FUNCTION
# ============================================================
def mouse_events(event, x, y, flags, param):
    global dragged_shape, mouse_offset, score

    # -------------------------
    # LEFT MOUSE BUTTON DOWN
    # -------------------------
    if event == cv2.EVENT_LBUTTONDOWN:

        # Check all shapes
        for shape in shape_names:

            # Skip already placed shapes
            if placed[shape]:
                continue

            # Get shape center position
            cx, cy = top_positions[shape]

            # Check if mouse is inside shape area
            if abs(x - cx) < SHAPE_SIZE and abs(y - cy) < SHAPE_SIZE:

                # Select this shape
                dragged_shape = shape

                # Store offset between mouse & shape center
                mouse_offset = (x - cx, y - cy)
                break


    # -------------------------
    # MOUSE MOVE (DRAGGING)
    # -------------------------
    elif event == cv2.EVENT_MOUSEMOVE and dragged_shape:

        # Update shape position following mouse
        top_positions[dragged_shape] = [
            x - mouse_offset[0],
            y - mouse_offset[1]
        ]


    # -------------------------
    # LEFT MOUSE BUTTON UP
    # -------------------------
    elif event == cv2.EVENT_LBUTTONUP and dragged_shape:

        # Get correct target position
        target_x, target_y = bottom_positions[dragged_shape]

        # Get current dragged position
        current_x, current_y = top_positions[dragged_shape]

        # Check if shape is dropped close enough
        if abs(current_x - target_x) < 50 and abs(current_y - target_y) < 50:

            # Mark shape as placed
            placed[dragged_shape] = True

            # Increase scoreQ
            score += 1

            # Snap shape to exact target position
            top_positions[dragged_shape] = [target_x, target_y]

        # Release dragged shape
        dragged_shape = None


# =============================
# WINDOW SETUP
# =============================
cv2.namedWindow("Shape Matching Game")
cv2.setMouseCallback("Shape Matching Game", mouse_events)


# =============================
# MAIN GAME LOOP
# =============================
while True:

    # Create white background window
    frame = cv2.imread('bg.jpg')
    frame = cv2.resize(frame,(900,600))

    # Calculate remaining time
    remaining = max(0, GAME_TIME - int(time.time() - start_time))
    # GAME_TIME = 3 sec
    # start_time = 8 sec
    # | time.time() | elapsed (current - start_time) | remaining (3 - elapsed) | max(0, remaining) |
    # |-------------|--------------------------------|--------------------------|-------------------|
    # |      9      |          9 - 8 = 1             |       3 - 1 = 2          |        2          |
    # |     10      |         10 - 8 = 2             |       3 - 2 = 1          |        1          |
    # |     11      |         11 - 8 = 3             |       3 - 3 = 0          |        0          |

    # Display timer and score
    cv2.putText(frame, f"Time: {remaining}", (20, 40), FONT, 1, (0, 0, 0), 2)
    cv2.putText(frame, f"Score: {score}", (20, 80), FONT, 1, (0, 150, 0), 2)

    # Draw bottom target shapes
    for shape in shape_names:

        # Green if placed, gray if not
        color = (0, 200, 0) if placed[shape] else (60, 60, 60)

        shape_drawer[shape](frame, bottom_positions[shape], SHAPE_SIZE, color)

        # Draw shape name
        x, y = bottom_positions[shape]
        cv2.putText(frame, shape, (x - 40, y + SHAPE_SIZE + 30),
                    FONT, 0.6, (0, 0, 0), 2)

    # Draw draggable shapes at top
    for shape in shape_names:
        if not placed[shape]:
            shape_drawer[shape](frame,
                                top_positions[shape],
                                SHAPE_SIZE,
                                colors[shape])

    # # Show frame
    cv2.imshow("Shape Matching Game", frame)

    # # Exit if time over or ESC pressed
    if remaining <= 0 or cv2.waitKey(1) & 0xFF == 27:
        # Get frame height and width
        h, w = frame.shape[:2]   # h = 600, w = 900

        # Text to display
        text = f"Game Over | Final Score: {score}"

        # Calculate centered position
        x = 297
        y = 313

        # Draw text
        cv2.putText(frame, text, (x - 150, y), FONT, 1.5, (0, 0, 255), 4)

        # Show frame
        cv2.imshow("Shape Matching Game", frame)
        cv2.waitKey(3000)
        break


# =============================
# CLEANUP
# =============================
cv2.destroyAllWindows()
print(f"✅ Game Over | Final Score: {score}")
