import arcade
from arcade.gui import UIView
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout, UIAnchorLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources

resources.load_kenney_fonts()

# Window Constants
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Scrabble | Game Over"

# Color Constants
BACKGROUND_COLOR = arcade.color.LIGHT_PINK
GRID_BACKGROUND_COLOR = arcade.color.BEIGE

TEXT_FONT = "Kenney Future"
TEXT_COLOR = arcade.color.LIGHT_RED_OCHRE
SECONDARY_TEXT_COLOR = arcade.color.OCHRE

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 75

BUTTON_STYLE = {
    'normal': UIFlatButton.UIStyle(
        font_color=arcade.color.WHITE,
        bg=arcade.color.LIGHT_RED_OCHRE,
    ),
    'hover': UIFlatButton.UIStyle(
        font_color=arcade.color.BEIGE,
        bg=arcade.color.LIGHT_GREEN,
    ),
    'press': UIFlatButton.UIStyle(
        font_color=arcade.color.LIGHT_RED_OCHRE,
        bg=arcade.color.LIGHT_PINK,
    )
}

class GameOverView(UIView):
    """ Shows when game ends """

    def __init__(self, player_score, opponent_score):
        super().__init__()

        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()


        self.grid = UIGridLayout(
            size_hint=(0, 0),
            row_count=10,
            column_count=2,
            vertical_spacing=10,
            horizontal_spacing=5,
        )
        self.grid.with_padding(all=50)
        self.grid.with_background(color=GRID_BACKGROUND_COLOR)

        self.manager.add(UIAnchorLayout(children=[self.grid]))

        # ------------
        title_text = UILabel(text="Game Over", width=150, font_size=40,
                        font_name=TEXT_FONT, text_color=TEXT_COLOR)
        self.grid.add(title_text, column=0, row=0, column_span=2)

        # ------------
        title_bar = UILabel(text="-----------------------------------",
                            width=150, font_size=10, font_name=TEXT_FONT,
                            text_color=TEXT_COLOR)
        self.grid.add(title_bar, column=0, row=1, column_span=2)        

        # ------------
        UIAnchorLayout
        your_score_label = UILabel(text="Your score:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(your_score_label, column=0, row=3)

        self.your_score_value_label = UILabel(text=f"{player_score}", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(self.your_score_value_label, column=1, row=3)

        # ------------
        opponent_score_label = UILabel(text="Opponent Score:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        opponent_score_label.with_padding(bottom=10)
        self.grid.add(opponent_score_label, column=0, row=4)

        self.opponent_score_value_label = UILabel(text=f"{opponent_score}", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(self.opponent_score_value_label, column=1, row=4)

        # ------------
        quit_button = UIFlatButton(text="Quit", height=30, width=50,
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(quit_button, column=0, row=6, column_span=2)

        @quit_button.event("on_click")
        def on_quit_action(_event):
            self.window.close()

    def on_draw(self):
        """ Draws window """
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        """ Called when the view is switched to."""
        self.manager.enable()
        self.window.set_caption(WINDOW_TITLE)

    def on_hide_view(self):
        """ Hides the manager """
        self.manager.disable()


def main():
    """ Main method to run the game end screen """
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Game Over Screen")
    game_over_view = GameOverView(30, 24)
    window.show_view(game_over_view)
    arcade.run()


if __name__ == "__main__":
    main()