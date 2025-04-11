""" Log in/sign up screen with user authentication """
from __future__ import annotations

import arcade
from arcade.gui import UIInputText, UIView
from arcade.gui.experimental.password_input import UIPasswordInput
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources
from game_start_screen import StartScreenView
from data import DataManager

# data manager for authentication
# and saving/loading game save data
data_manager = DataManager()

# Load kenny fonts shipped with arcade
resources.load_kenney_fonts()

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
        self.background_color = arcade.color.LIGHT_PINK
        self.manager = arcade.gui.UIManager()

        self.grid = UIGridLayout(
            size_hint=(0, 0),  # wrap children
            row_count=9,  # title | user, pw | login button | sing up button
            column_count=2,  # label and input field
            vertical_spacing=10,
            horizontal_spacing=5,
        )
        self.grid.with_padding(all=50)
        self.grid.with_background(color=arcade.color.BEIGE)

        self.grid.add(
            UILabel(text="SCRABBLE", width=150, font_size=40,
                    font_name="Kenney Future", text_color=arcade.color.LIGHT_RED_OCHRE),
            column=0,
            row=0,
            column_span=2,
        )

        self.grid.add(
            UILabel(text="-----------------------------------", width=150, font_size=10,
                    font_name="Kenney Future", text_color=arcade.color.LIGHT_RED_OCHRE),
            column=0,
            row=1,
            column_span=2,
        )

        title = self.grid.add(
            UILabel(text="Login", width=150, font_size=20,
                    font_name="Kenney Future", text_color=arcade.color.LIGHT_RED_OCHRE),
            column=0,
            row=2,
            column_span=2,
        )
        title.with_padding(bottom=20)

        self.grid.add(UILabel(text="Username:",
                                width=80,
                                font_name="Kenney Future",
                                text_color=arcade.color.LIGHT_PINK),
                        column=0,
                        row=3)
        self.username_input = self.grid.add(
            UIInputText(width=150, font_name="Kenney Future",
                        border_color=arcade.color.LIGHT_PINK,
                        text_color=arcade.color.LIGHT_PINK,
                        caret_color=arcade.color.BLACK,
                        ), column=1, row=3
        )
        self.username_input.with_background(color=arcade.color.BEIGE)
        self.username_input.padding = (0, 3)  # text padding left

        password_label = self.grid.add(UILabel(text="Password:",
                              width=80,
                              font_name="Kenney Future",
                              text_color=arcade.color.LIGHT_PINK
                              ),
                      column=0,
                      row=4
        )
        password_label._padding_bottom = 10

        self.password_input = self.grid.add(
            UIPasswordInput(width=150, font_name="Kenney Future",
                            border_color=arcade.color.LIGHT_PINK,
                            text_color=arcade.color.LIGHT_PINK,
                            caret_color=arcade.color.BLACK), column=1, row=4
        )
        self.password_input.with_background(color=arcade.color.BEIGE)
        self.password_input._padding_left = 3  # text padding left

        # set background to prevent full render on blinking caret

        login_button = self.grid.add(
            UIFlatButton(text="Login", height=30, width=150, size_hint=(1, None),
                         style=BUTTON_STYLE),
            column=0,
            row=5,
            column_span=2,
        )

        sign_up_button = self.grid.add(
            UIFlatButton(text="Sign Up", height=30, width=150, size_hint=(1, None),
                         style=BUTTON_STYLE),
            column=0,
            row=6,
            column_span=2,
        )

        # add warning label
        self.warning_label = self.grid.add(
            UILabel(
                text="Use 'TAB' to switch fields, then enter to login",
                width=150,
                font_size=10,
                font_name="Kenney Future",
                text_color=arcade.color.LIGHT_RED_OCHRE,
            ),
            column=0,
            row=8,
            column_span=2,
        )

        # initialize incorrect password label for later use
        self.incorrect_password_label= UILabel(
            text="Incorrect username or password",
            width=150,
            font_size=10,
            font_name="Kenney Future",
            text_color=(255, 0, 0),
        )

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        self.manager.add(anchor)

        @login_button.event("on_click")
        def on_login(_):
            self.on_login_action()

        @sign_up_button.event("on_click")
        def on_click_sign_up(_):
            # Navigate to the sign-up page
            sign_up_view = SignUpView(self)
            self.window.show_view(sign_up_view)

        # activate username input field
        self.username_input.activate()
    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        """Called when the view is switched to."""
        self.manager.enable()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.manager.draw()

    def on_login_action(self):
        """ Tries authenticating using with entered user and pass """
        entered_username = self.username_input.text.strip()
        entered_password = self.password_input.text.strip()

        # remove previous warning messages, if any
        for child in self.grid.children:
            if child == self.incorrect_password_label:
                self.grid.remove(child)

        success = data_manager.authenticate_user(entered_username, entered_password)

        if success:
            # show the StartScreenView after login
            self.window.show_view(StartScreenView())
        else:
            # shows incorrect credentials label
            self.grid.add(
                self.incorrect_password_label,
                column=0,
                row=7,
                column_span=2
            )

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


class SignUpView(arcade.View):
    """sign-up view where users can create a new account."""

    def __init__(self, login_view):
        super().__init__()

        self.background_color = arcade.color.LIGHT_PINK
        self.manager = arcade.gui.UIManager()

        self.login_view = login_view

        self.grid = UIGridLayout(
            size_hint=(0, 0),  # wrap children
            row_count=8,  # title | user, pw | login button | sing up button
            column_count=2,  # label and input field
            vertical_spacing=10,
            horizontal_spacing=5,
        )
        self.grid.with_padding(all=50)
        self.grid.with_background(color=arcade.color.BEIGE)

        title = self.grid.add(
            UILabel(text="Sign Up", width=150, font_size=20,
                    font_name="Kenney Future", text_color=arcade.color.LIGHT_RED_OCHRE),
            column=0,
            row=0,
            column_span=2,
        )
        title.with_padding(bottom=20)

        # username label
        self.grid.add(UILabel(text="Username:",
                              width=80,
                              font_name="Kenney Future",
                              text_color=arcade.color.LIGHT_PINK),
                      column=0,
                      row=1)

        self.username_input = self.grid.add(
            UIInputText(width=150, font_name="Kenney Future",
                        border_color=arcade.color.LIGHT_PINK,
                        text_color=arcade.color.LIGHT_PINK), column=1, row=1)
        self.username_input.with_background(color=arcade.color.BEIGE)
        self.username_input.padding = (0, 3)  # text padding left

        # Password label
        self.grid.add(UILabel(text="Password:",
                              width=80,
                              font_name="Kenney Future",
                              text_color=arcade.color.LIGHT_PINK),
                      column=0,
                      row=2)
        self.password_input = self.grid.add(
            UIPasswordInput(width=150, font_name="Kenney Future",
                            border_color=arcade.color.LIGHT_PINK,
                            text_color=arcade.color.LIGHT_PINK), column=1, row=2)
        self.password_input.with_background(color=arcade.color.BEIGE)
        self.password_input.padding = (0, 3)  # text padding left

        # Confirmation Password label
        self.grid.add(UILabel(text="Confirm Password:",
                              width=80,
                              font_name="Kenney Future",
                              text_color=arcade.color.LIGHT_PINK),
                      column=0, row=3)

        # confirmation password input
        self.confirm_password_input = self.grid.add(
            UIPasswordInput(width=150, font_name="Kenney Future",
                            border_color=arcade.color.LIGHT_PINK,
                            text_color=arcade.color.LIGHT_PINK), column=1, row=3)
        self.confirm_password_input.with_background(color=arcade.color.BEIGE)
        self.confirm_password_input.padding = (0, 3)  # text padding left

        sign_up_button = self.grid.add(
            UIFlatButton(text="Sign Up", height=30, width=150, size_hint=(1, None),
                         style=BUTTON_STYLE), column=0, row=4, column_span=2,)
        back_button = self.grid.add(
            UIFlatButton(text="Back", height=30, width=150, size_hint=(1, None),
                         style=BUTTON_STYLE), column=0, row=5, column_span=2,)

        # add hint label
        self.grid.add(UILabel(
            text="Use 'TAB' to switch fields",
            width=150,
            font_size=10,
            font_name="Kenney Future",
            text_color=arcade.color.LIGHT_RED_OCHRE), column=0, row=6, column_span=2
        )

        # -- Error labels --
        # initialize invalid username label for later use
        self.invalid_username_label = UILabel(
            text="Username must be 3 or more characters long",
            width=150,
            font_size=10,
            font_name="Kenney Future",
            text_color=(255, 0, 0)
        )

        # initialize username already taken label for later use
        self.taken_username_label= UILabel(
            text="Username already taken",
            width=150,
            font_size=10,
            font_name="Kenney Future",
            text_color=(255, 0, 0)
        )

        # initialize non-matching passwords label for later use
        self.passwords_no_match_label= UILabel(
            text="Passwords don't match",
            width=150,
            font_size=10,
            font_name="Kenney Future",
            text_color=(255, 0, 0)
        )
        # --

        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        @sign_up_button.event("on_click")
        def on_click_sign_up(_):
            entered_username = self.username_input.text
            entered_password = self.password_input.text
            confirmation_password = self.confirm_password_input.text

            # remove previous warning messages, if any
            for child in self.grid.children:
                if child in [self.invalid_username_label,
                             self.taken_username_label,
                             self.passwords_no_match_label]:
                    self.grid.remove(child)

            if len(entered_username) < 3:
                # show username too short label
                self.grid.add(
                    self.invalid_username_label,
                    column=0,
                    row=7,
                    column_span=2
                )
                return

            if entered_password == confirmation_password:
                print(f"Signing up with username: {entered_username} and\
                       password: {entered_password}")
                success = data_manager.sign_up(entered_username, entered_password)

                if success:
                    self.window.show_view(StartScreenView())
                else:
                    # show username already taken label
                    self.grid.add(
                        self.taken_username_label,
                        column=0,
                        row=7,
                        column_span=2
                    )
            else:
                # show passwords don't match label
                self.grid.add(
                    self.passwords_no_match_label,
                    column=0,
                    row=7,
                    column_span=2
                )

        @back_button.event("on_click")
        def on_click_back_to_login(_):
            # go back to login page
            self.window.show_view(self.login_view)

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
    # window = arcade.Window(title="Login Page")
    window = arcade.Window(title="Login Page", width=720, height=850)
    window.show_view(LoginView())
    window.run()


if __name__ == "__main__":
    main()
