"""
Starting Template from Python Arcade Documentation
"""
import arcade

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Scrabble"
PADDING = 40

# Grid Constants
GRID_SIZE = 15
TILE_SIZE = (WINDOW_WIDTH - PADDING) // GRID_SIZE

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


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_TITLE)

        self.background_color = arcade.color.BABY_BLUE

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.rectangles = []

    def on_draw(self):
        self.clear()

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                text = []
                x = col * TILE_SIZE + PADDING // 2
                y = row * TILE_SIZE + PADDING // 2

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

                arcade.draw_lbwh_rectangle_filled(x, y, TILE_SIZE, TILE_SIZE, color)
                arcade.draw_lbwh_rectangle_outline(x, y, TILE_SIZE, TILE_SIZE, arcade.color.NAVY_BLUE)
                x = x + 22
                start_y = y + 5
                for i, word in enumerate(text):
                    y = start_y - (i * 10)
                    arcade.draw_text(word, x, y + 25, arcade.color.BLACK, 5, anchor_x="center")


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = GameView()

    window.setup()

    arcade.run()


if __name__ == "__main__":
    main()
