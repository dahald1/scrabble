"""
Turn and Move Example.

Right-click to cause the tank to move to that point.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.turn_and_move
"""
import arcade
from arcade.gui import UIManager
from arcade import resources
from arcade.gui.widgets.buttons import UIFlatButton
from start import start_game
from window import GameView


resources.load_kenney_fonts()
# Load button textures (Replace these with your own image paths)
BUTTON_NORMAL = "back-button.png"  # Default state
BUTTON_HOVER = "left-arrow.png"  # When mouse is over
BUTTON_CLICKED = "left-arrow.png"  # When clicked


class Button(arcade.Sprite):
    """ A Button class that changes appearance on hover and click. """

    def __init__(self, normal_texture, hover_texture, clicked_texture, x, y, scale=0.5):
        super().__init__(normal_texture, scale)

        # Store textures as a list (instead of a dictionary)
        self.textures = [
            arcade.load_texture(normal_texture),  # normal texture
            arcade.load_texture(hover_texture),  # hover texture
            arcade.load_texture(clicked_texture)  # clicked texture
        ]
        # making it small
        self.scale = scale
        self.set_texture(0)  # Set to normal texture (first texture in the list)

        self.position = (x, y)

    def update_button(self, x, y, is_pressed):
        """ Change texture based on hover or click """
        if self.collides_with_point((x, y)):
            if is_pressed:
                self.set_texture(2)  # clicked texture (third texture)
            else:
                self.set_texture(1)  # hover texture (second texture)
        else:
            self.set_texture(0)  # normal texture (first texture)


WINDOW_WIDTH = 720
WINDOW_HEIGHT = 850
WINDOW_TITLE = "Intro Screen"


class Game_view(arcade.View):
    """ Main menu with buttons to open different views. """

    def __init__(self):
        super().__init__()
        self.hovered = False
        self.sprites = arcade.SpriteList()

        self.background_color = arcade.color.WHITE
        self.is_mouse_pressed = False  # track mouse click

        self.title = arcade.SpriteSolidColor(300, 100, self.window.width // 2, self.window.height//1.5,
                                               (255, 255, 255, 255))
        self.sprites.append(self.title)
        self.intro = arcade.Text("Welcome to Scrabble",
                                 self.title.center_x, self.title.center_y,
                                 arcade.color.BLACK, font_size=20,
                                 anchor_x="center", anchor_y="center", font_name=("Kenney Future", "arial bold"))

        self.play = arcade.SpriteSolidColor(300, 100, self.window.width // 2, self.window.height // 2,(0, 0, 255, 255))
        self.sprites.append(self.play)
        self.text = arcade.Text("Play",
                                self.play.center_x, self.play.center_y,
                                arcade.color.WHITE, font_size=20,
                                anchor_x="center", anchor_y="center",font_name=("Kenney Future", "arial bold"))

        # Create a text object for the button label
        self.text = arcade.Text("Play",
                                self.play.center_x, self.play.center_y,
                                arcade.color.WHITE, font_size=30,
                                anchor_x="center", anchor_y="center",
                                font_name=("Kenney Future", "arial bold"))

        self.with_AI = arcade.SpriteSolidColor(300, 100, self.window.width // 2, self.window.height // 4,
                                              (0, 0, 255, 255))
        self.sprites.append(self.with_AI)
        self.text2 = arcade.Text("Play With AI",
                                self.with_AI.center_x, self.with_AI.center_y,
                                arcade.color.WHITE, font_size=20,
                                anchor_x="center", anchor_y="center", font_name=("Kenney Future", "arial bold"))

        self.button1 = Button(BUTTON_NORMAL, BUTTON_HOVER, BUTTON_CLICKED, 200, 300, scale=0.2)
        # self.sprites.append(self.button1)
        self.button2 = Button(BUTTON_NORMAL, BUTTON_HOVER, BUTTON_CLICKED, 600, 300, scale=0.2)
        # self.sprites.append(self.button2)


    def on_draw(self):
        self.clear()
        self.sprites.draw()
        self.intro.draw()
        self.text.draw()
        self.text2.draw()


    def on_mouse_motion(self, x, y, dx, dy):
        """ Detect hover effect """
        self.button1.update_button(x, y, self.is_mouse_pressed)
        self.button2.update_button(x, y, self.is_mouse_pressed)
        if self.play.collides_with_point((x, y)):
            if not self.hovered:
                self.play.color = arcade.color.RED  # Change color on hover
                self.hovered = True
        elif self.with_AI.collides_with_point((x, y)):
            if not self.hovered:
                self.with_AI.color = arcade.color.RED  # Change color on hover
                self.hovered = True
        else:
            if self.hovered:
                self.with_AI.color = arcade.color.BLUE
                self.play.color = arcade.color.BLUE  # Revert when not hovering
                self.hovered = False

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Handle button click """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.is_mouse_pressed = True
            self.button1.update_button(x, y, self.is_mouse_pressed)
            self.button2.update_button(x, y, self.is_mouse_pressed)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """ Handle button release and navigation """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.is_mouse_pressed = False
            self.button1.update_button(x, y, self.is_mouse_pressed)
            self.button2.update_button(x, y, self.is_mouse_pressed)

            if self.play.collides_with_point((x, y)):
                print("play")
                self.window.show_view(start_game())
            if self.with_AI.collides_with_point((x, y)):
                print("this is clicked, for AI")
                self.window.show_view(start_game())

#
# def main():
#     """ Main function """
#     # Create a window class. This is what actually shows up on screen
#     window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
#
#     # Create and set up the GameView
#     game = Game_view()
#     # game.setup()
#
#     # Show GameView on screen
#     window.show_view(game)
#
#     # Start the arcade game loop
#     arcade.run()
#
# if __name__ == "__main__":
#     main()