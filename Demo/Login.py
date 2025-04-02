from __future__ import annotations

import arcade
from arcade.gui import UIInputText, UIOnClickEvent, UIView
from arcade.gui.experimental.password_input import UIPasswordInput
from arcade.gui.widgets.buttons import UIFlatButton
from arcade.gui.widgets.layout import UIGridLayout, UIAnchorLayout
from arcade.gui.widgets.text import UILabel
from arcade import resources
from game_start_screen import Game_view
import arcade
import arcade.gui
from typing import List

# Load kenny fonts shipped with arcade
resources.load_kenney_fonts()


class MyView(UIView):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.uicolor.BLUE_BELIZE_HOLE
        self.manager = arcade.gui.UIManager()

        self.grid = UIGridLayout(
            size_hint=(0, 0),  # wrap children
            row_count=6,  # title | user, pw | login button | sing up button
            column_count=2,  # label and input field
            vertical_spacing=10,
            horizontal_spacing=5,
        )
        self.grid.with_padding(all=50)
        self.grid.with_background(color=arcade.uicolor.DARK_BLUE_WET_ASPHALT)

        self.title = self.grid.add(
            UILabel(text="Login", width=150, font_size=20, font_name="Kenney Future"),
            column=0,
            row=0,
            column_span=2,
        )
        self.title.with_padding(bottom=20)

        self.username_label = self.grid.add(UILabel(text="Username:", width=80, font_name="Kenney Future"), column=0, row=1)
        self.username_input = self.grid.add(
            UIInputText(width=150, font_name="Kenney Future"), column=1, row=1
        )
        self.username_input.with_background(color=arcade.uicolor.BLACK)
        self.username_input.padding = (0, 3)  # text padding left

        self.password_label = self.grid.add(UILabel(text="Password:", width=80, font_name="Kenney Future"), column=0, row=2)
        self.password_input = self.grid.add(
            UIPasswordInput(width=150, font_name="Kenney Future"), column=1, row=2
        )
        self.password_input.with_background(color=arcade.uicolor.BLACK)
        self.password_input.padding = (0, 3)  # text padding left
        # set background to prevent full render on blinking caret

        login_button = self.grid.add(
            UIFlatButton(text="Login", height=30, width=150, size_hint=(1, None)),
            column=0,
            row=3,
            column_span=2,
        )

        sign_up_button = self.grid.add(
            UIFlatButton(text="Sign Up", height=30, width=150, size_hint=(1, None)),
            column=0,
            row=4,
            column_span=2,
        )

        # add warning label
        self.warning_label = self.grid.add(
            UILabel(
                text="Use 'TAB' to switch fields, then enter to login",
                width=150,
                font_size=10,
                font_name="Kenney Future",
            ),
            column=0,
            row=5,
            column_span=2,
        )

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        @login_button.event("on_click")
        def on_login(event):
            self.on_login_action()

        @sign_up_button.event("on_click")
        def on_click_sign_up(event):
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
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        print(f"User logged in with: {username} {password}")
        # example validation (replace with actual validation logic)
        if username == "yes" and password == "yes123":
            print("Login successful!")
            self.window.show_view(Game_view())  # show the GameView after login
        else:
            print("Invalid credentials!")

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        # if username field active, switch fields with enter
        if self.username_input.active:
            if symbol == arcade.key.TAB:
                self.username_input.deactivate()
                self.password_input.activate()
                return True
            elif symbol == arcade.key.ENTER:
                self.username_input.deactivate()
                self.on_login_action()
                return True
        # if password field active, login with enter
        elif self.password_input.active:
            if symbol == arcade.key.TAB:
                self.username_input.activate()
                self.password_input.deactivate()
                return True
            elif symbol == arcade.key.ENTER:
                self.password_input.deactivate()
                self.on_login_action()
                return True
        return False


class SignUpView(arcade.View):
    """sign-up view where users can create a new account."""

    def __init__(self, login_view):
        super().__init__()

        self.background_color = arcade.uicolor.BLUE_BELIZE_HOLE
        self.manager = arcade.gui.UIManager()

        self.login_view = login_view

        self.grid = UIGridLayout(
            size_hint=(0, 0),  # wrap children
            row_count=7,  # title | user, pw | login button | sing up button
            column_count=2,  # label and input field
            vertical_spacing=10,
            horizontal_spacing=5,
        )
        self.grid.with_padding(all=50)
        self.grid.with_background(color=arcade.uicolor.DARK_BLUE_WET_ASPHALT)

        self.title = self.grid.add(
            UILabel(text="Sign Up", width=150, font_size=20, font_name="Kenney Future"),
            column=0,
            row=0,
            column_span=2,
        )
        self.title.with_padding(bottom=20)

        # username
        self.username_label = self.grid.add(UILabel(text="Username:", width=80, font_name="Kenney Future"), column=0,
                                            row=1)
        self.username_input = self.grid.add(
            UIInputText(width=150, font_name="Kenney Future"), column=1, row=1)
        self.username_input.with_background(color=arcade.uicolor.BLACK)
        self.username_input.padding = (0, 3)  # text padding left

        # Password
        self.password_label = self.grid.add(UILabel(text="Password:", width=80, font_name="Kenney Future"), column=0,
                                            row=2)
        self.password_input = self.grid.add(
            UIPasswordInput(width=150, font_name="Kenney Future"), column=1, row=2)
        self.password_input.with_background(color=arcade.uicolor.BLACK)
        self.password_input.padding = (0, 3)  # text padding left

        # Confirm Password
        self.confirm_password_label = self.grid.add(UILabel(text="Confirm Password:", width=80, font_name="Kenney Future"),
                                                    column=0, row=3)
        self.confirm_password_input = self.grid.add(
            UIPasswordInput(width=150, font_name="Kenney Future"), column=1, row=3)
        self.confirm_password_input.with_background(color=arcade.uicolor.BLACK)
        self.confirm_password_input.padding = (0, 3)  # text padding left

        sign_up_button = self.grid.add(
            UIFlatButton(text="Sign Up", height=30, width=150, size_hint=(1, None)), column=0, row=4, column_span=2,)
        back_button = self.grid.add(
            UIFlatButton(text="Back", height=30, width=150, size_hint=(1, None)), column=0, row=5, column_span=2,)

        # add warning label
        self.warning_label = self.grid.add(
            UILabel(
                text="Use 'TAB' to switch fields",
                width=150,
                font_size=10,
                font_name="Kenney Future",), column=0, row=6, column_span=2,)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

        @sign_up_button.event("on_click")
        def on_click_sign_up(event):
            username = self.username_input.text
            password = self.password_input.text
            confirm_password = self.confirm_password_input.text
            if password == confirm_password:
                print(f"Signing up with Username: {username} and Password: {password}")
            else:
                print("Passwords do not match!")

        @back_button.event("on_click")
        def on_click_back_to_login(event):
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
        elif self.password_input.active:
            if symbol == arcade.key.TAB:
                self.password_input.deactivate()
                self.confirm_password_input.activate()
                return True

        elif self.confirm_password_input.active:
            if symbol == arcade.key.TAB:
                self.confirm_password_input.deactivate()
                self.username_input.activate()

                return True
        return False


def main():
    # window = arcade.Window(title="Login Page")
    window = arcade.Window(title="Login Page", width=720, height=850)
    window.show_view(MyView())
    window.run()


if __name__ == "__main__":
    main()