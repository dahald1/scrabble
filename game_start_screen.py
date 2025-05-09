"""Start screen for playing game"""

import arcade
from arcade.gui import UIView
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout, UIAnchorLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources
from multiplayer_screen import MultiplayerView
from start import start_game

resources.load_kenney_fonts()

DEFAULT_SAVE_NAME = "save1"

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Scrabble | Start Screen"

# Color Constants
BACKGROUND_COLOR = arcade.color.LIGHT_PINK
GRID_BACKGROUND_COLOR = arcade.color.BEIGE

TEXT_FONT = ("Kenney Future", "arial bold")
TEXT_COLOR = arcade.color.LIGHT_RED_OCHRE

BUTTON_WIDTH = 300
BUTTON_HEIGHT = 50

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
    'disabled': UIFlatButton.UIStyle(
        font_color=arcade.color.BEIGE,
        bg=arcade.color.AUROMETALSAURUS,
    )
}


class StartScreenView(UIView):
    """ Main menu with buttons to open different views. """

    def __init__(self, data_manager):
        super().__init__()
        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()

        self.data_manager = data_manager

        self.grid = UIGridLayout(
            size_hint=(0, 0),
            row_count=7,  # title | bar | play with AI | play online | quit
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
        self.grid.add(title_bar, row=1)

        # ------------
        play_with_ai_button = UIFlatButton(text="Play Against AI", height=BUTTON_HEIGHT,
                                           width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.grid.add(play_with_ai_button, row=2)

        @play_with_ai_button.event("on_click")
        def on_play_against_ai(_event):
            self.window.show_view(start_game(self.data_manager))

        # ------------
        load_game_button = UIFlatButton(text="Load Previous Game", height=BUTTON_HEIGHT,
                                        width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.grid.add(load_game_button, row=3)

        if not DEFAULT_SAVE_NAME in data_manager.saved_games:
            load_game_button.disabled = True

        @load_game_button.event("on_click")
        def on_load_game(_event):
            self.window.show_view(start_game(self.data_manager, load_game=True))

        # ------------
        divider = UILabel(text="---------------------",
                      font_size=10, font_name=TEXT_FONT,
                      text_color=TEXT_COLOR)
        self.grid.add(divider, row=4)

        # ------------
        play_online_button = UIFlatButton(text="Play Online", height=BUTTON_HEIGHT,
                                          width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.grid.add(play_online_button, row=5)

        @play_online_button.event("on_click")
        def on_play_online(_event):
            self.window.show_view(MultiplayerView(self, self.data_manager))

        # ------------

        quit_button = UIFlatButton(text="Quit", height=BUTTON_HEIGHT,
                                          width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.grid.add(quit_button, row=6)

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
        self.window.set_caption(WINDOW_TITLE)

    def on_hide_view(self):
        """ Hides the manager """
        self.manager.disable()


if __name__ == "__main__":
    print("Run login.py to play Scrabble!")
