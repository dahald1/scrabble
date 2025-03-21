"""
Starting Template from Python Arcade Documentation
"""
import arcade

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

# Position Constants
POSITIONS = [(176, 67), (236, 67), (296, 67), (356, 67), (416, 67), (476, 67), (536, 67)]

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


class Tile(arcade.SpriteSolidColor):
    """Main Tile class deals with data and dragging logic."""

    # Position of the tile in the tile mat
    mat_position = 0
    value = ""

    def __init__(self, x, y, width, height, mat_pos):
        super().__init__(width, height, color=arcade.color.BONE)
        self.offset_y = None
        self.offset_x = None
        self.dragging = False
        self.center_x = x + width // 2
        self.center_y = y + height // 2
        self.mat_position = mat_pos

    # Dragging Logic
    def on_mouse_press(self, x, y, button):
        """ Called when the user presses a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT and self.collides_with_point((x, y)):
            self.dragging = True
            self.offset_x = self.center_x - x
            self.offset_y = self.center_y - y

    def on_mouse_release(self, x, y, button):
        """ Called when a user releases a mouse button. """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dragging = False

            # Setting current corrdinates on mouse release
            curr_x = self.center_x
            curr_y = self.center_y

            # Snap to grid coordinates
            snap_x = (round((self.center_x - PADDING / 2) / TILE_SIZE + SNAPPING_ERROR)
                      * TILE_SIZE + TILE_SIZE / 2 + PADDING / 2)
            snap_y = (round((self.center_y - PADDING / 2) / TILE_SIZE + SNAPPING_ERROR)
                      * TILE_SIZE + TILE_SIZE / 2 + PADDING / 2)

            # Restricting snapping to game board.
            if (snap_y > WINDOW_HEIGHT + 20 or snap_y < WINDOW_HEIGHT - (TILE_SIZE * GRID_SIZE) + PADDING
                    or snap_x < PADDING or snap_x > WINDOW_WIDTH):
                self.center_x = POSITIONS[self.mat_position][0]
                self.center_y = POSITIONS[self.mat_position][1]
            else:
                self.center_y = snap_y - self.height
                self.center_x = snap_x - self.width

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


class GameView(arcade.Window):
    """ Main application class. """
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.background_color = arcade.color.BABY_BLUE
        self.tiles = arcade.SpriteList()
        # Initializing tiles
        for i in range(7):
            tile = Tile(i * TILE_SPACING + TILE_PADDING, TILE_MAT_HEIGHT, TILE_SIZE, TILE_SIZE, i)
            print(tile.center_x, tile.center_y)
            self.tiles.append(tile)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

    def on_draw(self):
        self.clear()

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

                # Drawing Board Tiles
                arcade.draw_lbwh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, color)
                arcade.draw_lbwh_rectangle_outline(x, y, TILE_SIZE, TILE_SIZE,
                                                   arcade.color.NAVY_BLUE)

                # TODO: Change to text object instead of draw_text
                # Writing Text
                x = x + LINE_TRACING
                start_y = y + LINE_SPACING
                for i, word in enumerate(text):
                    # Spacing out words
                    y = start_y - (i * 10)
                    arcade.draw_text(word, x, y + 25, arcade.color.BLACK, 5, anchor_x="center")

        # Draw Tile Mat at Bottom of Screen
        arcade.draw_lbwh_rectangle_filled(WINDOW_WIDTH // MAT_PADDING_TOP_BOT, 25,
                                          WINDOW_WIDTH // MAT_PADDING_LEFT_RIGHT,
                                          100, arcade.color.DARK_BROWN)
        arcade.draw_lbwh_rectangle_filled(WINDOW_WIDTH // MAT_PADDING_TOP_BOT, 25,
                                          WINDOW_WIDTH // MAT_PADDING_LEFT_RIGHT,
                                          20, arcade.color.BISTRE_BROWN)

        # Draw Tiles
        self.tiles.draw()

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


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = GameView()

    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()
