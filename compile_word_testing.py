"""
Test file for window.py
Mainly used for compile_word functions
"""
from window import GameView

game_view = GameView()

GRID_SIZE = 15

TEST_BOARD_MATRIX = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

TEST_BOARD_MATRIX[7][5] = "C"
TEST_BOARD_MATRIX[7][6] = "U"
TEST_BOARD_MATRIX[7][7] = "T"

TEST_BOARD_MATRIX[5][7] = "C"
TEST_BOARD_MATRIX[6][7] = "A"

TEST_BOARD_MATRIX[1][1] = "D"
TEST_BOARD_MATRIX[1][2] = "O"
TEST_BOARD_MATRIX[1][3] = "G"

TEST_BOARD_MATRIX[1][6] = "S"
TEST_BOARD_MATRIX[2][6] = "E"
TEST_BOARD_MATRIX[3][6] = "T"


def print_board_matrix():
    """Prints the board matrix to console for debugging purposes."""
    for row in TEST_BOARD_MATRIX:
        print(row)
    print("\n\n")


def test_vertical_existing():
    """Tests the compile_word function with a simple vertical word addition (existing letters on one side)."""
    added_tiles = [(5, 7), (6, 7)]
    expected_output = ['C', 'A', 'T']

    word = game_view.compile_word(added_tiles, TEST_BOARD_MATRIX)

    if word == expected_output:
        print("PASSED")
    else:
        print("FAILED")


def test_horizontal_existing():
    """Tests the compile_word function with a simple horizontal word addition (existing letters on one side)."""
    added_tiles = [(7, 5), (7, 6)]
    expected_output = ['C', 'U', 'T']

    word = game_view.compile_word(added_tiles, TEST_BOARD_MATRIX)

    if word == expected_output:
        print("PASSED")
    else:
        print("FAILED")

def test_vertical():
    """Tests compile_word function for a simple vertical word addition (no existing letters)."""
    added_tiles = [(1, 6), (2, 6), (3, 6)]
    expected_output = ['S', 'E', 'T']

    word = game_view.compile_word(added_tiles, TEST_BOARD_MATRIX)

    if word == expected_output:
        print("PASSED")
    else:
        print("FAILED")


def test_horizontal():
    """Tests compile_word function for a simple horizontal word addition (no existing letters)."""
    added_tiles = [(1, 1), (1, 2), (1, 3)]
    expected_output = ['D', 'O', 'G']

    word = game_view.compile_word(added_tiles, TEST_BOARD_MATRIX)

    if word == expected_output:
        print("PASSED")
    else:
        print("FAILED")

if __name__ == "__main__":
    # Printing board matrix to verify letter positions
    print_board_matrix()

    # Connecting with existing letters (one side)
    print("Connecting with existing letters (one side)")
    test_vertical_existing()
    test_horizontal_existing()

    # No existing letters
    print("No existing letters")
    test_vertical()
    test_horizontal()
