"""
Starting Template from Python Arcade Documentation
"""
import random
import arcade
import arcade.gui

# TODO - Diwas, I added a TODO down below in the get_board_matrix function.
#  That's what you can call to get the matrix from another file. Enter will
#  end the current turn, update the board matrix, and print it to the console.
#  The played tiles will no longer be draggable. If you import this file,
#  you should be able to call the function. Find_added_tiles is a function that
#  returns the differences in tiles between two matrices.  It can be called
#  when enter is hit after the board matrix is updated if need be. The other
#  methods are for internal stuff like dragging, drawing, and positioning.

# Global Sprite List
global tiles

# Window Constants
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Scrabble"
PADDING = 40

# Tile Constants
TILE_SPACING = 60
TILE_PADDING = 154

# Text Constants
LINE_SPACING = 5
LINE_TRACING = 22

# Mat constants
MAT_PADDING_TOP_BOT = 5
MAT_PADDING_LEFT_RIGHT = 1.7
TILE_MAT_HEIGHT = 45

# Snapping Constants
SNAPPING_ERROR = 0.5

# Grid Constants
GRID_SIZE = 15
TILE_SIZE = (WINDOW_WIDTH - PADDING) // GRID_SIZE

# Mat Position Constants
MAT_POSITIONS = [(176, 67), (236, 67), (296, 67), (356, 67), (416, 67), (476, 67), (536, 67)]

# Special Tile Constants (ZERO INDEX)
TRIPLE_WORD = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
TRIPLE_LETTER = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13),
                 (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)]
DOUBLE_WORD = [(1, 1), (2, 2), (3, 3), (4, 4), (10, 10), (11, 11), (12, 12), (13, 13),
               (1, 13), (2, 12), (3, 11), (4, 10), (10, 4), (11, 3), (12, 2), (13, 1)]
DOUBLE_LETTER = [(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14),
                 (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2),
                 (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14),
                 (12, 6), (12, 8), (14, 3), (14, 11)]
CENTER = [(7, 7)]

# Global Board Matrix (15x15, top left is (0, 0))
BOARD_MATRIX = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Tile bag dictionary. Format (value: quantity remaining). Represents default scrabble distribution
TILE_BAG = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2,
            "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2,
            "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1,
            "Y": 2, "Z": 1, " ": 2}

# Letter's points values
POINTS_VALUE = {0: [" "],
                1: ["A", "E", "I", "O", "U", "L", "N", "S", "T", "R"],
                2: ["D", "G"],
                3: ["B", "C", "M", "P"],
                4: ["F", "H", "V", "W", "Y"],
                5: ["K"],
                8: ["J", "X"],
                10: ["Q", "Z"]}

# Mat Positions Tracking
MAT_POSITIONS_FILLED = [False for _ in range(7)]


class Tile(arcade.SpriteSolidColor):
    """Main Tile class deals with data and dragging logic."""

    # Position of the tile in the tile mat
    mat_position = 0
    value = ""

    def __init__(self, x, y, width, height, mat_pos, value):
        super().__init__(width, height, color=arcade.color.BONE)
        self.offset_y = None
        self.offset_x = None
        self.dragging = False
        self.draggable = True
        self.center_x = x + width // 2
        self.center_y = y + height // 2
        self.mat_position = mat_pos
        self.value = value

    def end_turn(self):
        """Setting values at end of turn to freeze tiles."""
        if (PADDING / 2 <= self.center_x <= WINDOW_WIDTH - PADDING / 2
                and WINDOW_HEIGHT - (GRID_SIZE * TILE_SIZE) - PADDING / 2
                <= self.center_y <= WINDOW_HEIGHT - PADDING / 2):
                self.draggable = False
                MAT_POSITIONS_FILLED[self.mat_position] = False
                self.mat_position = -1

    # Tile Letter Logic
    def set_letter(self):
        """Draw letter on top of the tile."""
        # TODO - Make sure tiles print on top of the letters for other tiles.
        # Tile letter text object
        text = arcade.Text(
            self.value,
            self.center_x,
            self.center_y,
            arcade.color.BLACK,
            20,
            anchor_x="center",
            anchor_y="center"
        )

        # Calculating points value based on global dictionary
        points_value = ""
        for i in POINTS_VALUE.keys():
            if self.value in POINTS_VALUE[i]:
                points_value = str(i)

        # Points value text object
        points_text = arcade.Text(
            points_value,
            self.center_x + 15,
            self.center_y + 15,
            arcade.color.BLACK,
            10,
            anchor_x="center",
            anchor_y="center"
        )
        text.draw()
        points_text.draw()

    @staticmethod
    def refill_mat(self):
        """Refill the tile mat with a new tile."""
        # Initializing player's initial tile draw
        for i in range(7):
            # Filling only positions that need to be filled
            if not MAT_POSITIONS_FILLED[i]:
                value = ""
                valid = False
                while not valid:
                    # Turning the tile bag into a list for random distribution selection
                    tile_bag_list = []
                    for letter, quantity in TILE_BAG.items():
                        tile_bag_list.extend([letter] * quantity)

                    # Selecting a random tile from the bag
                    value = random.choice(tile_bag_list)

                    # Checking if tiles in the distribution have been used up
                    if TILE_BAG[value] > 0:
                        TILE_BAG[value] -= 1
                        valid = True

                # Creating tile sprite objects + updating mat
                tile = Tile(i * TILE_SPACING + TILE_PADDING, TILE_MAT_HEIGHT,
                            TILE_SIZE, TILE_SIZE, i, value=value)
                self.tiles.append(tile)
                MAT_POSITIONS_FILLED[i] = True

    def on_key_press(self, key, modifiers):
        """ Called whenever a key on the keyboard is pressed from method in GameView"""
        if key == arcade.key.ENTER:
            self.end_turn()

    def on_mouse_press(self, x, y, button):
        """ Called when the user presses a mouse button."""
        # Dragging Logic
        if button == arcade.MOUSE_BUTTON_LEFT and self.collides_with_point((x, y)):
            if self.draggable:
                self.dragging = True
                self.offset_x = self.center_x - x
                self.offset_y = self.center_y - y

    def snap_to_grid(self):
        # Snap to grid coordinates calculation
        snap_x = (round((self.center_x - PADDING / 2) / TILE_SIZE + SNAPPING_ERROR)
                  * TILE_SIZE + TILE_SIZE / 2 + PADDING / 2)
        snap_y = (round((self.center_y - PADDING / 2) / TILE_SIZE + SNAPPING_ERROR)
                  * TILE_SIZE + TILE_SIZE / 2 + PADDING / 2)

        # Restricting snapping to game board.
        if (snap_y > WINDOW_HEIGHT + 20 or snap_y < WINDOW_HEIGHT - (TILE_SIZE * GRID_SIZE)
                + PADDING or snap_x < PADDING or snap_x > WINDOW_WIDTH):
            # Back to mat
            self.center_x = MAT_POSITIONS[self.mat_position][0]
            self.center_y = MAT_POSITIONS[self.mat_position][1]
            MAT_POSITIONS_FILLED[self.mat_position] = True

        else:
            # Snap to grid
            self.center_y = snap_y - self.height
            self.center_x = snap_x - self.width

            # Updating mat's positional information
            MAT_POSITIONS_FILLED[self.mat_position] = False


    def on_mouse_release(self, x, y, button):
        """ Called when a user releases a mouse button."""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dragging = False
            self.snap_to_grid()


    def on_mouse_motion(self, x, y, dx, dy):
        """ Called when the user moves the mouse. """
        if self.dragging:
            self.center_x = x + self.offset_x
            self.center_y = y + self.offset_y

            # Keeping the tile on screen
            if self.center_x - self.width // 2 < 0:
                self.center_x = self.width // 2
            if self.center_x + self.width // 2 > WINDOW_WIDTH:
                self.center_x = WINDOW_WIDTH - self.width // 2
            if self.center_y - self.height // 2 < 0:
                self.center_y = self.height // 2
            if self.center_y + self.height // 2 > WINDOW_HEIGHT:
                self.center_y = WINDOW_HEIGHT - self.height // 2

class SaveButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        """ Save button logic. """
        # TODO - implement save logic
        print("Save button clicked!")

class GameView(arcade.Window):
    """ Main application class. """
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        # Initial setup of variables
        self.special_tile_text = None
        self.background_color = arcade.color.BABY_BLUE
        self.tiles = arcade.SpriteList()

        # Initializing player's initial tile draw
        Tile.refill_mat(self)

        # Initializing GUI
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        # Drawing Save Button
        save_button = SaveButton(text="Save", width=100, height=40, x=WINDOW_WIDTH - PADDING - 85, y=PADDING + 20)
        self.ui_manager.add(save_button)

    @staticmethod
    def coordinates_to_px(row, col):
        """Converts row and column coordinates to pixel coordinates."""
        x = col * TILE_SIZE + PADDING // 2
        y = WINDOW_HEIGHT - ((row + 1) * TILE_SIZE) - PADDING // 2
        return x, y

    @staticmethod
    def find_added_tiles(prev_board_matrix, curr_board_matrix):
        """Finds the word that was placed on the board."""
        added_tiles = []

        # Find the tile that was placed
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if prev_board_matrix[row][col] is None and curr_board_matrix[row][col] is not None:
                    added_tiles.append((row, col))

    @staticmethod
    def print_board_matrix():
        """Prints the board matrix to console for debugging purposes."""
        for row in BOARD_MATRIX:
            print(row)
        print("\n\n")

    # TODO - Diwas, this returns the board matrix.
    @staticmethod
    def get_board_matrix():
        """Returns the current board matrix."""
        return BOARD_MATRIX

    def update_board_matrix(self):
        """Updates the board matrix with the current tile positions."""

        # Uncomment to debug board matrix positioning
        prev_matrix = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                prev_matrix[row][col] = BOARD_MATRIX[row][col]


        # Clear matrix
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                BOARD_MATRIX[row][col] = None

        # Update matrix
        for tile in self.tiles:
            if (PADDING / 2 <= tile.center_x <= WINDOW_WIDTH - PADDING /2 and
                WINDOW_HEIGHT - (GRID_SIZE * TILE_SIZE) - PADDING / 2 < tile.center_y
                    <= WINDOW_HEIGHT - PADDING / 2):

                # Calculate row and column of tile by positioning within window
                row = (WINDOW_HEIGHT - tile.center_y - PADDING / 2) // TILE_SIZE
                col = (tile.center_x - PADDING / 2) // TILE_SIZE

                BOARD_MATRIX[int(row)][int(col)] = tile.value

        # Uncomment to debug board matrix positioning
        # self.print_board_matrix()
        # self.find_added_tiles(prev_board_matrix=prev_matrix, curr_board_matrix=BOARD_MATRIX)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

    def draw_board(self):
        # Draw Board Boxes
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                text = []
                # Aligning the board to the left and top
                x = col * TILE_SIZE + PADDING // 2
                y = WINDOW_HEIGHT - ((row + 1) * TILE_SIZE) - PADDING // 2

                # Coloring and writing in special squares
                if (row, col) in TRIPLE_WORD:
                    color = arcade.color.LIGHT_RED_OCHRE
                    text = ["TRIPLE", "WORD", "SCORE"]
                elif (row, col) in TRIPLE_LETTER:
                    color = arcade.color.BALL_BLUE
                    text = ["TRIPLE", "LETTER", "SCORE"]
                elif (row, col) in DOUBLE_WORD:
                    color = arcade.color.LIGHT_PINK
                    text = ["DOUBLE", "WORD", "SCORE"]
                elif (row, col) in DOUBLE_LETTER:
                    color = arcade.color.LIGHT_BLUE
                    text = ["DOUBLE", "LETTER", "SCORE"]
                elif (row, col) in CENTER:
                    color = arcade.color.LIGHT_GREEN
                else:
                    color = arcade.color.BEIGE
                    text = []

                # TODO - increase special score colored tile size
                # Drawing Board Tiles
                arcade.draw_lbwh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, color)
                arcade.draw_lbwh_rectangle_outline(x, y, TILE_SIZE, TILE_SIZE,
                                                   arcade.color.NAVY_BLUE)

                # Writing Text
                x = x + LINE_TRACING
                start_y = y + LINE_SPACING
                for i, word in enumerate(text):
                    # Spacing out words
                    y = start_y - (i * 10)
                    self.special_tile_text = arcade.Text(
                        word,
                        x,
                        y + 25,
                        arcade.color.BLACK,
                        5,
                        anchor_x="center"
                    )
                    self.special_tile_text.draw()

    def on_draw(self):
        self.clear()
        self.draw_board()

        # Draw Tile Mat at Bottom of Screen
        arcade.draw_lbwh_rectangle_filled(WINDOW_WIDTH // MAT_PADDING_TOP_BOT, 25,
                                          WINDOW_WIDTH // MAT_PADDING_LEFT_RIGHT,
                                          100, arcade.color.DARK_BROWN)
        arcade.draw_lbwh_rectangle_filled(WINDOW_WIDTH // MAT_PADDING_TOP_BOT, 25,
                                          WINDOW_WIDTH // MAT_PADDING_LEFT_RIGHT,
                                          20, arcade.color.BISTRE_BROWN)

        # Draw Tiles
        self.tiles.draw()
        for tile in self.tiles:
            tile.set_letter()

        self.ui_manager.draw()


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        if key == arcade.key.ENTER:
            GameView.update_board_matrix(self)
            GameView.print_board_matrix()

            for tile in self.tiles:
                tile.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

    def on_mouse_motion(self, x, y, dx, dy):
        for tile in self.tiles:
            tile.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for tile in self.tiles:
            tile.on_mouse_press(x, y, button)

    def on_mouse_release(self, x, y, button, modifiers):
        for tile in self.tiles:
            if tile.dragging:
                tile.on_mouse_release(x, y, button)

                # Tests for tile collision with tiles already placed
                if arcade.check_for_collision_with_list(tile, self.tiles):
                    tile.center_x = MAT_POSITIONS[tile.mat_position][0]
                    tile.center_y = MAT_POSITIONS[tile.mat_position][1]

        self.update_board_matrix()


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = GameView()

    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()
