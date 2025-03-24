"""
Test file for window.py
Mainly used for compile_word functions
"""
from window import GameView


def test_compile_word():
    game_view = GameView()

    added_tiles = [(7, 7), (7, 8), (7, 9)]
    game_view.compile_word(added_tiles)
