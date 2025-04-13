import arcade
from arcade import resources

# Window Constants
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850

resources.load_kenney_fonts()

class GameOverView(arcade.View):
    """ Shows when game ends """

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BABY_BLUE)

    def on_draw(self):
        """ Draw this view """
        self.clear()

        # TODO - add get score logic
        arcade.draw_text(
            "Game Over",
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
            anchor_y="center",
            font_name="Kenney Future"
        )
        arcade.draw_text(
            "Your Score: ",
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 3,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            font_name="Kenney Future"
        )
        arcade.draw_text(
            "Opponent's Score: ",
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 4,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
            anchor_y="center",
            font_name="Kenney Future"
        )

def main():
    """ Main method to run the game end screen """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Game Over Screen")
    game_over_view = GameOverView()
    window.show_view(game_over_view)
    arcade.run()

if __name__ == "__main__":
    main()