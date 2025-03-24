"""
Test file for window.py
Mainly used for compile_word functions
"""
from window import GameView

game_view = GameView()

GRID_SIZE = 15

BOARD_MATRIX = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

BOARD_MATRIX[7][5] = "C"
BOARD_MATRIX[7][6] = "U"
BOARD_MATRIX[7][7] = "T"
BOARD_MATRIX[5][7] = "C"
BOARD_MATRIX[6][7] = "A"


def print_board_matrix():
    """Prints the board matrix to console for debugging purposes."""
    for row in BOARD_MATRIX:
        print(row)
    print("\n\n")


def test_compile_word_one():
    """Tests the compile_word function with a simple vertical word addition."""
    added_tiles = [(5, 7), (6, 7)]
    expected_output = ['C', 'A', 'T']

    word = game_view.compile_word(added_tiles, BOARD_MATRIX)

    if word == expected_output:
        print("PASSED")
    else:
        print("FAILED")


def test_compile_word_two():
    """Tests the compile_word function with a simple horizontal word addition."""
    added_tiles = [(7, 5), (7, 6)]
    expected_output = ['C', 'U', 'T']

    word = game_view.compile_word(added_tiles, BOARD_MATRIX)

    if word == expected_output:
        print("PASSED")
    else:
        print("FAILED")

if __name__ == "__main__":
    # Printing board matrix to verify letter positions
    print_board_matrix()

    # Running tests
    test_compile_word_one()
    test_compile_word_two()
