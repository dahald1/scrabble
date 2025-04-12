"""Multiplayer screen for joining and creating new lobbys"""
import arcade
from arcade.gui import UIInputText, UIView
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout, UIAnchorLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources

resources.load_kenney_fonts()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Scrabble | Multiplayer"

# Color Constants
BUTTON_DEFAULT_COLOR = arcade.color.LIGHT_RED_OCHRE
BUTTON_HOVERED_COLOR = arcade.color.LIGHT_GREEN
BUTTON_CLICKED_COLOR = arcade.color.LIGHT_PINK

BACKGROUND_COLOR = arcade.color.LIGHT_PINK
GRID_BACKGROUND_COLOR = arcade.color.BEIGE

TEXT_FONT = "Kenney Future"
TEXT_COLOR = arcade.color.LIGHT_RED_OCHRE
SECONDARY_TEXT_COLOR = arcade.color.LIGHT_PINK

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
    ),
}

class MultiplayerView(UIView):
    """View where users can join or host games."""

    def __init__(self, start_screen_view):
        super().__init__()

        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()

        self.start_screen_view = start_screen_view

        self.grid = UIGridLayout(
            size_hint=(0, 0),  # wrap children
            row_count=10,  # title | user, pw | login button | sing up button
            column_count=2,  # label and input field
            vertical_spacing=10,
            horizontal_spacing=5,
        )
        self.grid.with_padding(all=50)
        self.grid.with_background(color=GRID_BACKGROUND_COLOR)

        self.manager.add(UIAnchorLayout(children=[self.grid]))

        # ------------
        title_text = UILabel(text="SCRABBLE", width=150, font_size=40,
                        font_name=TEXT_FONT, text_color=TEXT_COLOR)
        self.grid.add(title_text, column=0, row=0, column_span=2)

        # ------------
        title_bar = UILabel(text="-----------------------------------",
                            width=150, font_size=10, font_name=TEXT_FONT,
                            text_color=TEXT_COLOR)
        self.grid.add(title_bar, column=0, row=1, column_span=2)

        # ------------
        subtitle = UILabel(text="Join or host a game", width=150, font_size=20,
                              font_name=TEXT_FONT, text_color=TEXT_COLOR)
        subtitle.with_padding(bottom=20)
        self.grid.add(subtitle, column=0, row=2, column_span=2)

        # ------------
        game_id_label = UILabel(text="Game ID:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(game_id_label, column=0, row=3)

        game_id_input = UIInputText(width=150, font_name=TEXT_FONT,
                                    border_color=SECONDARY_TEXT_COLOR,
                                    text_color=SECONDARY_TEXT_COLOR,
                                    caret_color=arcade.color.BLACK)
        game_id_input.with_background(color=GRID_BACKGROUND_COLOR)
        game_id_input.padding = (0, 3)  # text padding left
        self.game_id_input = self.grid.add(game_id_input, column=1, row=3)

        # ------------
        join_game_button = UIFlatButton(text="Join Game", height=30, width=150,
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(join_game_button, column=0, row=5, column_span=2)

        @join_game_button.event("on_click")
        def on_join_game(_):
            print("joining game not implemented!")

        # ------------
        host_game_button = UIFlatButton(text="Host Game", height=30, width=150,
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(host_game_button, column=0, row=6, column_span=2)

        @host_game_button.event("on_click")
        def on_host_game(_):
            print("hosting not implemented!")

        # ------------
        back_button = UIFlatButton(text="Back", height=30, width=50,
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(back_button, column=0, row=7, column_span=2)

        @back_button.event("on_click")
        def on_go_back(_):
            self.window.show_view(self.start_screen_view)

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
    """ Main function """
    window = arcade.Window(title=WINDOW_TITLE, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    window.show_view(MultiplayerView(None))
    window.run()


if __name__ == "__main__":
    main()
