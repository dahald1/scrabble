"""Start screen for playing game"""

import sys
import arcade
from arcade.gui import UIView
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout, UIAnchorLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources
from multiplayer_screen import MultiplayerView

# can't import window without adding demo folder to path
sys.path.insert(0, 'demo')
from window import GameView

resources.load_kenney_fonts()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Start Screen"

# Color Constants
BUTTON_DEFAULT_COLOR = arcade.color.LIGHT_RED_OCHRE
BUTTON_HOVERED_COLOR = arcade.color.LIGHT_GREEN
BUTTON_CLICKED_COLOR = arcade.color.LIGHT_PINK

BACKGROUND_COLOR = arcade.color.LIGHT_PINK
GRID_BACKGROUND_COLOR = arcade.color.BEIGE

TEXT_FONT = ("Kenney Future", "arial bold")
TEXT_COLOR = arcade.color.LIGHT_RED_OCHRE

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


class StartScreenView(UIView):
    """ Main menu with buttons to open different views. """

    def __init__(self):
        super().__init__()
        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()

        self.grid = UIGridLayout(
            size_hint=(0, 0),
            row_count=5,  # title | bar | play with AI | play online | quit
            column_count=1,
            vertical_spacing=10,
            horizontal_spacing=5,
        )

        # anchors grid to center of the screen
        self.manager.add(UIAnchorLayout(children=[self.grid]))

        # adds padding to grid to make its background larger
        self.grid.with_padding(all=50)
        self.grid.with_background(color=GRID_BACKGROUND_COLOR)

        # ------------
        title_text = UILabel(text="Welcome to Scrabble",
                             font_size=20, font_name=TEXT_FONT,
                             text_color=TEXT_COLOR)
        self.grid.add(title_text, row=0)

        title_bar = UILabel(text="--------------------------------------",
                      font_size=10, font_name=TEXT_FONT,
                      text_color=TEXT_COLOR)
        title_bar.with_padding(bottom=30)
        self.grid.add(title_bar, row=1)

        # ------------
        play_with_ai_button = UIFlatButton(text="Play Against AI", height=BUTTON_HEIGHT,
                                           width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.grid.add(play_with_ai_button, row=2)

        @play_with_ai_button.event("on_click")
        def on_play_against_ai(_):
            self.window.show_view(GameView())

        # ------------
        play_online_button = UIFlatButton(text="Play Online", height=BUTTON_HEIGHT,
                                          width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.grid.add(play_online_button, row=3)

        @play_online_button.event("on_click")
        def on_play_online(_):
            self.window.show_view(MultiplayerView(self))

        # ------------

        quit_button = UIFlatButton(text="Quit", height=BUTTON_HEIGHT,
                                          width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.grid.add(quit_button, row=4)

        @quit_button.event("on_click")
        def quit_game(_):
            self.window.close()
            arcade.exit()

    def on_draw(self):
        """ Draws window """
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        """ Called when the view is switched to."""
        self.manager.enable()

    def on_hide_view(self):
        """ Hides the manager """
        self.manager.disable()


def main():
    """ Main function """
    window = arcade.Window(title=WINDOW_TITLE, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    window.show_view(StartScreenView())
    window.run()


if __name__ == "__main__":
    main()
