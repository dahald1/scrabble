""" Log in/sign up screen with user authentication """
from __future__ import annotations

import arcade
from arcade.gui import UIInputText, UIView
from arcade.gui.experimental.password_input import UIPasswordInput
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout, UIAnchorLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources
from game_start_screen import StartScreenView
from data import DataManager

# data manager for authentication
# and saving/loading game save data
data_manager = DataManager()

# Load kenny fonts shipped with arcade
resources.load_kenney_fonts()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Scrabble | Login"

BACKGROUND_COLOR = arcade.color.LIGHT_PINK
GRID_BACKGROUND_COLOR = arcade.color.BEIGE

TEXT_FONT = "Kenney Future"
TEXT_COLOR = arcade.color.LIGHT_RED_OCHRE
SECONDARY_TEXT_COLOR = arcade.color.OCHRE

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


class LoginView(UIView):
    """login view where users can log into a existing account """

    def __init__(self):
        super().__init__()
        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()

        self.grid = UIGridLayout(
            size_hint=(0, 0),  # wrap children
            row_count=9,  # title | user, pw | login button | sing up button
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
        login_label = UILabel(text="Login", width=150, font_size=20,
                              font_name=TEXT_FONT, text_color=TEXT_COLOR)
        login_label.with_padding(bottom=20)
        self.grid.add(login_label, column=0, row=2, column_span=2)

        # ------------
        username_label = UILabel(text="Username:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(username_label, column=0, row=3)

        username_input = UIInputText(width=150, font_name=TEXT_FONT,
                                     border_color=SECONDARY_TEXT_COLOR,
                                     text_color=SECONDARY_TEXT_COLOR,
                                     caret_color=arcade.color.BLACK)
        username_input.with_background(color=GRID_BACKGROUND_COLOR)
        username_input.padding = (0, 3)  # text padding left
        self.username_input = self.grid.add(username_input, column=1, row=3)

        # ------------
        password_label = UILabel(text="Password:", width=80,
                                 font_name=TEXT_FONT,
                                 text_color=SECONDARY_TEXT_COLOR)
        password_label._padding_bottom = 10
        self.grid.add(password_label, column=0, row=4)

        password_input = UIPasswordInput(width=150, font_name=TEXT_FONT,
                                         border_color=SECONDARY_TEXT_COLOR,
                                         text_color=SECONDARY_TEXT_COLOR,
                                         caret_color=arcade.color.BLACK)
        password_input.with_background(color=GRID_BACKGROUND_COLOR)
        password_input._padding_left = 3  # text padding left
        self.password_input = self.grid.add(password_input, column=1, row=4)

        # ------------
        login_button = UIFlatButton(text="Login", height=30, width=150, 
                                    size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(login_button, column=0, row=5, column_span=2)

        @login_button.event("on_click")
        def on_login(_):
            self.on_login_action()

        # ------------
        sign_up_button = UIFlatButton(text="Sign Up", height=30, width=150,
                                      size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(sign_up_button, column=0, row=6, column_span=2)

        @sign_up_button.event("on_click")
        def on_click_sign_up(_):
            # Navigate to the sign-up page
            sign_up_view = SignUpView(self)
            self.window.show_view(sign_up_view)

        # ------------
        hint_label = UILabel(
                text="Use 'TAB' to switch fields, then enter to login",
                width=150, font_size=10, font_name=TEXT_FONT,
                text_color=TEXT_COLOR)
        self.grid.add(hint_label, column=0, row=7, column_span=2)

        # ------------
        # initialize error label for later use
        error_label = UILabel(text="", width=150, font_size=10,
            font_name=TEXT_FONT, text_color=arcade.color.RED)
        self.error_label = self.grid.add(error_label, column=0, row=8,
                                         column_span=2)
        # ------------

        # activate username input field
        self.username_input.activate()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        """Called when the view is switched to."""
        self.manager.enable()
        self.window.set_caption(WINDOW_TITLE)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.manager.draw()

    def on_login_action(self):
        """ Tries authenticating using with entered user and pass """
        entered_username = self.username_input.text.strip()
        entered_password = self.password_input.text.strip()

        # remove previous error messages, if any
        self.error_label.text = ""

        success = data_manager.authenticate_user(entered_username, entered_password)

        if success:
            # show the StartScreenView after login
            self.window.show_view(StartScreenView())
        else:
            # shows incorrect credentials message
            self.error_label.text = "Incorrect username or password"

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        # if username field active, switch fields with enter
        if self.username_input.active:
            if symbol == arcade.key.TAB:
                self.username_input.deactivate()
                self.password_input.activate()
                return True
        if symbol == arcade.key.ENTER:
            self.username_input.deactivate()
            self.on_login_action()
            return True
        # if password field active, login with enter
        if self.password_input.active:
            if symbol == arcade.key.TAB:
                self.username_input.activate()
                self.password_input.deactivate()
                return True
            if symbol == arcade.key.ENTER:
                self.password_input.deactivate()
                self.on_login_action()
                return True
        return False


class SignUpView(UIView):
    """sign-up view where users can create a new account."""

    def __init__(self, login_view):
        super().__init__()

        self.background_color = BACKGROUND_COLOR
        self.manager = arcade.gui.UIManager()

        self.login_view = login_view

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
        sign_up_label = UILabel(text="Sign Up", width=150, font_size=20,
                              font_name=TEXT_FONT, text_color=TEXT_COLOR)
        sign_up_label.with_padding(bottom=20)
        self.grid.add(sign_up_label, column=0, row=2, column_span=2)

        # ------------
        username_label = UILabel(text="Username:", width=80,
                                font_name=TEXT_FONT,
                                text_color=SECONDARY_TEXT_COLOR)
        self.grid.add(username_label, column=0, row=3)

        username_input = UIInputText(width=150, font_name=TEXT_FONT,
                                     border_color=SECONDARY_TEXT_COLOR,
                                     text_color=SECONDARY_TEXT_COLOR,
                                     caret_color=arcade.color.BLACK)
        username_input.with_background(color=GRID_BACKGROUND_COLOR)
        username_input.padding = (0, 3)  # text padding left
        self.username_input = self.grid.add(username_input, column=1, row=3)

        # ------------
        password_label = UILabel(text="Password:", width=80,
                                 font_name=TEXT_FONT,
                                 text_color=SECONDARY_TEXT_COLOR)
        password_label._padding_bottom = 10
        self.grid.add(password_label, column=0, row=4)

        password_input = UIPasswordInput(width=150, font_name=TEXT_FONT,
                                         border_color=SECONDARY_TEXT_COLOR,
                                         text_color=SECONDARY_TEXT_COLOR,
                                         caret_color=arcade.color.BLACK)
        password_input.with_background(color=GRID_BACKGROUND_COLOR)
        password_input._padding_left = 3  # text padding left
        self.password_input = self.grid.add(password_input, column=1, row=4)

        # ------------
        confirm_password_label = UILabel(text="Confirm Password:", width=80,
                                 font_name=TEXT_FONT,
                                 text_color=SECONDARY_TEXT_COLOR)
        confirm_password_label._padding_bottom = 10
        self.grid.add(confirm_password_label, column=0, row=5)

        confirm_password_input = UIPasswordInput(width=150,
                                        font_name=TEXT_FONT,
                                        border_color=SECONDARY_TEXT_COLOR,
                                        text_color=SECONDARY_TEXT_COLOR,
                                        caret_color=arcade.color.BLACK)
        confirm_password_input.with_background(color=GRID_BACKGROUND_COLOR)
        confirm_password_input._padding_left = 3  # text padding left
        self.confirm_password_input = self.grid.add(confirm_password_input,
                                                    column=1, row=5)

        # ------------
        sign_up_button = UIFlatButton(text="Sign Up", height=30, width=150,
                                      size_hint=(1, None), style=BUTTON_STYLE)
        self.grid.add(sign_up_button, column=0, row=6, column_span=2)

        @sign_up_button.event("on_click")
        def on_click_sign_up(_):
            self.on_sign_up_action()

        # ------------
        back_button = self.grid.add(
            UIFlatButton(text="Back", height=30, width=150, size_hint=(1, None),
                         style=BUTTON_STYLE), column=0, row=7, column_span=2,)

        @back_button.event("on_click")
        def on_click_back_to_login(_):
            # go back to login page
            self.window.show_view(self.login_view)

        # ------------
        hint_label = UILabel(
                text="Use 'TAB' to switch fields, then enter to sign up",
                width=150, font_size=10, font_name=TEXT_FONT,
                text_color=TEXT_COLOR)
        self.grid.add(hint_label, column=0, row=8, column_span=2)

        # ------------
        # initialize error label for later use
        error_label = UILabel(text="", width=150, font_size=10,
            font_name=TEXT_FONT, text_color=arcade.color.RED)
        self.error_label = self.grid.add(error_label, column=0, row=9,
                                         column_span=2)

        # activate username input field
        self.username_input.activate()

    def on_hide_view(self):
        """hides the manager"""
        self.manager.disable()

    def on_show_view(self):
        """Called when the view is switched to."""
        self.manager.enable()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.manager.draw()

    def on_sign_up_action(self):
        """ Attempts to create user account """
        entered_username = self.username_input.text
        entered_password = self.password_input.text
        confirmation_password = self.confirm_password_input.text

        # remove previous error messages, if any
        self.error_label.text = ""

        if len(entered_username) < 3:
            # show username too short label
            self.error_label.text = "Username must be 3 or more characters long"
            return

        if entered_password == confirmation_password:
            print(f"Signing up with username: {entered_username} and\
                    password: {entered_password}")
            success = data_manager.sign_up(entered_username, entered_password)

            if success:
                self.window.show_view(StartScreenView())
            else:
                # show username already taken label
                self.error_label.text = "Username already taken"
        else:
            # show passwords don't match label
            self.error_label.text = "Passwords don't match"

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        # if username field active, switch fields with enter
        if self.username_input.active:
            if symbol == arcade.key.TAB:
                self.username_input.deactivate()
                self.password_input.activate()
                return True
        # if password field active, login with enter
        if self.password_input.active:
            if symbol == arcade.key.TAB:
                self.password_input.deactivate()
                self.confirm_password_input.activate()
                return True
        if self.confirm_password_input.active:
            if symbol == arcade.key.TAB:
                self.confirm_password_input.deactivate()
                self.username_input.activate()
                return True
        return False


def main():
    """ Main function """
    window = arcade.Window(title=WINDOW_TITLE, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    window.show_view(LoginView())
    window.run()


if __name__ == "__main__":
    main()
