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
    'disabled': UIFlatButton.UIStyle(
        font_color=arcade.color.BEIGE,
        bg=arcade.color.AUROMETALSAURUS,
    )
}

class LobbyView(UIView):
    """View where users can join or host games."""

    def __init__(self, multiplayer_screen, multiplayer_lobby_manager):
        super().__init__()

        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()

        self.multiplayer_screen = multiplayer_screen
        self.multiplayer_lobby_manager = multiplayer_lobby_manager

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
        lobby_id = self.multiplayer_lobby_manager.connected_lobby_id
        subtitle = UILabel(text=f"Lobby ID: {lobby_id}", width=150,
                           font_size=20, font_name=TEXT_FONT,
                           text_color=TEXT_COLOR)
        subtitle.with_padding(bottom=10)
        self.grid.add(subtitle, column=0, row=2, column_span=2)

        # ------------
        player_one_label = UILabel(text="Player One:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(player_one_label, column=0, row=3)

        self.player_one_user_label = UILabel(text="", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(self.player_one_user_label, column=1, row=3)

        # ------------
        player_two_label = UILabel(text="Player Two:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        player_two_label.with_padding(bottom=10)
        self.grid.add(player_two_label, column=0, row=4)

        self.player_two_user_label = UILabel(text="", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(self.player_two_user_label, column=1, row=4)

        # ------------
        if self.multiplayer_lobby_manager.is_host():
            self.start_game_button = UIFlatButton(text="Start Game", height=30, width=150,
                                        size_hint=(1, None), style=BUTTON_STYLE)
            self.grid.add(self.start_game_button, column=0, row=5, column_span=2)

            self.start_game_button.on_click = self.on_start_game_action

        # ------------
        exit_lobby_button = UIFlatButton(text="Leave Lobby", height=30, width=50,
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(exit_lobby_button, column=0, row=6, column_span=2)

        exit_lobby_button.on_click = self.on_leave_lobby_action

    def on_draw(self):
        """ Draws window """
        if not self.multiplayer_lobby_manager.connected_to_lobby:
            self.multiplayer_lobby_manager.connected_lobby_doc_watch.unsubscribe()
            self.window.show_view(self.multiplayer_screen)

        self.clear()
        self.update_ui()
        self.manager.draw()

    def update_ui(self):
        """ Updates certain UI elements to keep up to date with lobby data """
        lobby_data = self.multiplayer_lobby_manager.connected_lobby_data

        self.player_one_user_label.text = lobby_data["player_one"]
        self.player_two_user_label.text = lobby_data["player_two"] or ""

        if self.multiplayer_lobby_manager.is_host():
            # Disables start game button if lobby isn't full
            if self.multiplayer_lobby_manager.full_lobby():
                self.start_game_button.disabled = False
            else:
                self.start_game_button.disabled = True

    def on_show_view(self):
        """ Called when the view is switched to."""
        self.manager.enable()
        self.window.set_caption(WINDOW_TITLE)

    def on_hide_view(self):
        """ Hides the manager """
        self.manager.disable()

    def on_start_game_action(self, _event):
        """ Handles action for starting a game """
        self.multiplayer_lobby_manager.start_game()

    def on_leave_lobby_action(self, _event):
        """ Handles action for leaving a lobby """
        self.multiplayer_lobby_manager.leave_lobby()
        self.window.show_view(self.multiplayer_screen)


if __name__ == "__main__":
    print("Run login.py to play Scrabble!")
