"""Displays game lobby and allows host to start game"""
import arcade
from arcade.gui import UIView
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout, UIAnchorLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources

resources.load_kenney_fonts()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Scrabble | Lobby"

# Color Constants
BUTTON_DEFAULT_COLOR = arcade.color.LIGHT_RED_OCHRE
BUTTON_HOVERED_COLOR = arcade.color.LIGHT_GREEN
BUTTON_CLICKED_COLOR = arcade.color.LIGHT_PINK

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
    ),
}

class LobbyView(UIView):
    """View where users can join or host games."""

    def __init__(self, multiplayer_screen):
        super().__init__()

        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()

        self.multiplayer_screen = multiplayer_screen

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
        title_text = UILabel(text="SCRABBLE", width=150, font_size=40,
                        font_name=TEXT_FONT, text_color=TEXT_COLOR)
        self.grid.add(title_text, column=0, row=0, column_span=2)

        # ------------
        title_bar = UILabel(text="-----------------------------------",
                            width=150, font_size=10, font_name=TEXT_FONT,
                            text_color=TEXT_COLOR)
        self.grid.add(title_bar, column=0, row=1, column_span=2)

        # ------------
        subtitle = UILabel(text=f"Lobby ID: {1234567890}", width=150,
                           font_size=20, font_name=TEXT_FONT,
                           text_color=TEXT_COLOR)
        subtitle.with_padding(bottom=10)
        self.grid.add(subtitle, column=0, row=2, column_span=2)

        # ------------
        player_one_label = UILabel(text="Player One:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(player_one_label, column=0, row=3)

        player_one_user_label = UILabel(text=f"{''}", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(player_one_user_label, column=1, row=3)

        # ------------
        player_two_label = UILabel(text="Player Two:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        player_two_label.with_padding(bottom=10)
        self.grid.add(player_two_label, column=0, row=4)

        player_two_user_label = UILabel(text="", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.player_two_user_label = self.grid.add(player_two_user_label,
                                                   column=1, row=3)

        # ------------
        # TODO: If host, don't create start game button
        start_game_button = UIFlatButton(text="Start Game", height=30, width=150,
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(start_game_button, column=0, row=5, column_span=2)

        start_game_button.on_click = self.on_start_game_action

        # ------------
        exit_lobby_button = UIFlatButton(text="Leave Lobby", height=30, width=50,
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(exit_lobby_button, column=0, row=6, column_span=2)

        @exit_lobby_button.event("on_click")
        def on_exit_lobby(_event):
            self.window.show_view(self.multiplayer_screen)

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

    def on_start_game_action(self, _event):
        """ Handles action for starting a game """
        # TODO: If lobby has 2 players, create game doc, set game_start flag,
        # else display error message
        print("starting game not implemented!")

    def on_exit_game_action(self, _event):
        """ Handles action for leaving a lobby """
        # TODO: If host, delete lobby, else just leave lobby
        self.window.show_view(self.multiplayer_screen)


def main():
    """ Main function """
    window = arcade.Window(title=WINDOW_TITLE, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    window.show_view(LobbyView(None))
    window.run()


if __name__ == "__main__":
    main()
