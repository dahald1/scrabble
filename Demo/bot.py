# from Demo import board
from player import Player
from word import Word
import random
from dictionary import load_dictionary_upper


# TODO connect with the placing tiles and get the turn and playing working

# TODO generate point for that word
# TODO look for the highest points possible and play that word

# TODO concern: a letter can where so How do I check for that?
class AIPlayer(Player):
    def __init__(self, bag, board):
        super().__init__(bag)
        self.name = "AI Player"
        self.board = board

        self.word_list = load_dictionary_upper("dictionary.csv")

    def get_board_letters(self):
        """Returns a list of (letter, row, col) tuples for all letters on the board."""
        board_array = self.board.board_array()
        letters_on_board = []
        for row in range(15):
            for col in range(15):
                # Remove padding spaces
                cell = board_array[row][col].strip()
                if cell not in ["TLS", "TWS", "DLS", "DWS"]:
                    if len(cell) == 1 and cell.isalpha():  # Check if it's a single letter
                        letters_on_board.append((cell, row, col))
        return letters_on_board

    def playing_position(self):
        """Returns a dictionary of possible positions to play and the available spaces in each direction"""
        board_array = self.board.board_array()
        steps = 7  # maximum # of steps a word can extend

        possible_positions = {}  # Dictionary storing playable positions and available spaces
        rows, cols = len(board_array), len(board_array[0])

        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        # gets all the letter positions on the board in the format (letter, row, col)
        on_board = self.get_board_letters()

        # iterate over all placed letters
        for cell, row, col in on_board:
            for dir_name, (dr, dc) in directions.items():
                space_counter = 0

                # Check spaces in the given direction
                for step in range(1, steps + 1):
                    r, c = row + step * dr, col + step * dc
                    if not (0 <= r < rows and 0 <= c < cols):  # out of bounds
                        break
                    if board_array[r][c] in {' ', "TLS", "TWS", "DLS", "DWS"}:
                        space_counter += 1  # found a space
                    else:
                        break

                possible_positions[(cell, row, col, dir_name)] = space_counter

        return possible_positions  # return the dictionary of possible positions


    def choose_word(self):
        rack_letters = [tile.get_letter() for tile in self.get_rack_arr()]

        playing_positions = self.playing_position()

        playable_words = []

        for (letter, row, col, direction), spaces in playing_positions.items():

            # iterate over each word in the word_list.
            for word in self.word_list:
                # convert the current word into a list of individual letters.
                counter = 0
                word_letters = list(word)
                # create a copy of the rack_letters to avoid modifying the original rack during checks.
                temp_rack = rack_letters.copy()
                # check if the letter is at the start
                # this will check for Right and Down
                if direction == "right" or direction == "down":
                    if letter in word_letters[0]:
                        # check each letter in the word to see if it exists in the rack.
                        for rack_letter in word_letters:
                            # if the letter exists in the temp_rack, remove it (use it).
                            if rack_letter in temp_rack:
                                temp_rack.remove(rack_letter)

                        if len(temp_rack) < 7 and direction == "right":
                            playable_words.append((word, row + len(word) - 1, col, "right"))
                        if len(temp_rack) < 7 and direction == "down":
                            playable_words.append((word, row, col + (len(word) - 1), "down"))
                # check if the letter is at the start, this will check for Up and Left
                elif direction == "left" or direction == "up":
                    if letter in word_letters[len(word_letters) - 1]:
                        # check each letter in the word to see if it exists in the rack.
                        for rack_letter in word_letters:
                            # if the letter exists in the temp_rack, remove it (use it).
                            if rack_letter in temp_rack:
                                temp_rack.remove(rack_letter)

                        if len(temp_rack) < 7 and direction == "up":
                            playable_words.append((word, row, col - (len(word) - 1), "down"))
                        if len(temp_rack) < 7 and direction == "left":
                            playable_words.append((word, row - (len(word) - 1), col, "right"))

        # randomly choose a word and return the word, staring location and the
        # directions the word should be going
        # print(playable_words)
        chosen_word = random.choice(playable_words)
        print(chosen_word)
        word = chosen_word[0]
        location = (chosen_word[1], chosen_word[2])
        directions = chosen_word[3]
        # TODO ai_place_tile in window.py
        return word, location, directions



    def is_valid_placement(self, word, location, direction):
        from start import round_number, players, premium_spots, LETTER_VALUES
        temp_word = Word(word, location, self, direction, self.board.board_array(), round_number, players,
                         premium_spots, LETTER_VALUES)
        checked = temp_word.check_word()
        if checked:
            return True
        else:
            return False

    # def play_turn(self, board):
    #     word, location, direction = self.choose_word()
    #     if word == "":
    #         print(f"{self.name} skips their turn.")
    #         return True
    #
    #     print(f"{self.name} plays: {word} at {location} going {direction}")
    #     from start import round_number, players, premium_spots, LETTER_VALUES
    #     word_obj = Word(word, location, self, direction, board.board_array(), round_number, players, premium_spots,
    #                     LETTER_VALUES)
    #     board.place_word(word, location, direction, self)
    #     word_obj.calculate_word_score()
    #     return True


import unittest
from unittest.mock import MagicMock


class TestAIPlayer(unittest.TestCase):

    def setUp(self):
        # Mock a board for testing purposes
        self.board = MagicMock()
        self.board.board_array.return_value = [
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            # Add more rows as needed for tests
        ]
        self.bag = MagicMock()  # You can mock the bag if needed
        self.ai_player = AIPlayer(self.bag, self.board)

    def test_initialization(self):
        self.assertEqual(self.ai_player.name, "AI Player")
        self.assertIsInstance(self.ai_player.word_list, list)

    def test_get_board_letters(self):
        # Setup: Board has a few letters
        self.board.board_array.return_value = [
            [" ", " ", " ", "A", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            # Add more rows as needed
        ]

        letters = self.ai_player.get_board_letters()
        expected_letters = [("A", 0, 3), ("B", 1, 2)]
        self.assertEqual(letters, expected_letters)

    def test_playing_position(self):
        # Mock board state where "A" and "B" are placed
        self.board.board_array.return_value = [
            [" ", " ", " ", "T", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", "B", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            # Add more rows as needed
        ]

        positions = self.ai_player.playing_position()
        # Check if the dictionary contains keys for positions (A at 0,3, B at 1,2)
        self.assertIn(("A", 0, 3, "right"), positions)
        self.assertIn(("B", 1, 2, "down"), positions)

    def test_choose_word(self):
        # Mocking the behavior of get_rack_arr
        self.ai_player.get_rack_arr = MagicMock(return_value=[MagicMock(get_letter=MagicMock(return_value='A')),
                                                              MagicMock(get_letter=MagicMock(return_value='P')),
                                                              MagicMock(get_letter=MagicMock(return_value='F')),
                                                              MagicMock(get_letter=MagicMock(return_value='G'))])
        self.ai_player.playing_position = MagicMock(return_value={("C", 0, 3, "down"): 1})
        self.ai_player.word_list = ["AB", "BA", "CAT"]

        chosen_word, yes, no = self.ai_player.choose_word()
        print("chosen word: ", chosen_word, yes, no)
        self.assertIn(chosen_word, ["CAT"])  # Chosen word should be from the rack and dictionary

    # def test_find_placement(self):
    #     # Mock board state where no word is placed yet
    #     self.board.board_array.return_value = [
    #         [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    #         [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    #         # Add more rows as needed
    #     ]
    #
    #     # Test for word placement
    #     placement = self.ai_player.find_placement("HELLO")
    #     self.assertEqual(placement, ([7, 7], "right"))  # Check if it returns the center position

    def test_is_valid_placement(self):
        # Mock the behavior of the Word class and check valid placement
        self.ai_player.is_valid_placement = MagicMock(return_value=True)
        result = self.ai_player.is_valid_placement("HELLO", [7, 7], "right")
        self.assertTrue(result)

    # def test_play_turn(self):
    #     # Mock word placement behavior
    #     self.ai_player.choose_word = MagicMock(return_value=("HELLO", [7, 7], "right"))
    #     self.board.place_word = MagicMock()
    #
    #     result = self.ai_player.play_turn(self.board)
    #
    #     # Ensure place_word is called
    #     self.board.place_word.assert_called_with("HELLO", [7, 7], "right", self.ai_player)
    #     self.assertTrue(result)
    #
    # def test_play_turn_skip(self):
    #     # Test for turn skipping when no word is chosen
    #     self.ai_player.choose_word = MagicMock(return_value=("", [7, 7], "right"))
    #
    #     result = self.ai_player.play_turn(self.board)
    #
    #     # Ensure it skips the turn
    #     self.assertFalse(self.board.place_word.called)
    #     self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()

########################CODES I WANN THROW AWAY BUT TOO GREDY###################################


# from player import Player
# from word import Word
# import random
#
# class AIPlayer(Player):
#     def __init__(self, bag, board):
#         super().__init__(bag)
#         self.name = "AI Player"
#         self.board = board
#         self.word_list = [
#             "CAT", "DOG", "RAT", "BAT", "HAT", "MAT", "PAT", "SAT",
#             "RUN", "FUN", "SUN", "GUN", "BUN", "THE", "AND", "FOR"
#         ]
#

#
#     def find_connecting_spot(self, word, letter, row, col):
#         """Finds an empty spot to connect the word to an existing letter, checking right or down."""
#         board_array = self.board.board_array()
#         word_letters = list(word)
#
#         # Try connecting horizontally (right)
#         for i in range(len(word)):
#             if word_letters[i] == letter:
#                 start_col = col - i  # Position the word so the letter aligns
#                 if start_col >= 0 and (start_col + len(word)) <= 15:
#                     # Check if the spot before the word is empty or edge, and after is empty or edge
#                     left_ok = start_col == 0 or board_array[row][start_col - 1].strip() == ""
#                     right_ok = (start_col + len(word)) == 15 or board_array[row][start_col + len(word)].strip() == ""
#                     if left_ok and right_ok:
#                         # Check each position for validity
#                         valid = True
#                         for j in range(len(word)):
#                             if j != i and board_array[row][start_col + j].strip() != "":
#                                 valid = False
#                                 break
#                         if valid and self.is_valid_placement(word, [row, start_col], "right"):
#                             return [row, start_col], "right"
#
#         # Try connecting vertically (down)
#         for i in range(len(word)):
#             if word_letters[i] == letter:
#                 start_row = row - i  # Position the word so the letter aligns
#                 if start_row >= 0 and (start_row + len(word)) <= 15:
#                     # Check if the spot above the word is empty or edge, and below is empty or edge
#                     top_ok = start_row == 0 or board_array[start_row - 1][col].strip() == ""
#                     bottom_ok = (start_row + len(word)) == 15 or board_array[start_row + len(word)][col].strip() == ""
#                     if top_ok and bottom_ok:
#                         # Check each position for validity
#                         valid = True
#                         for j in range(len(word)):
#                             if j != i and board_array[start_row + j][col].strip() != "":
#                                 valid = False
#                                 break
#                         if valid and self.is_valid_placement(word, [start_row, col], "down"):
#                             return [start_row, col], "down"
#
#         return None, None  # No valid spot found
#
#     def choose_word(self):
#         """Chooses a word that connects to an existing letter on the board."""
#         rack_letters = [tile.get_letter() for tile in self.get_rack_arr()]
#         board_letters = self.get_board_letters()
#
#         # First turn: place at center if board is empty
#         if not board_letters:
#             playable_words = [w for w in self.word_list if all(w.count(l) <= rack_letters.count(l) for l in w)]
#             if playable_words:
#                 return random.choice(playable_words), [7, 7], "right"
#             return "", [7, 7], "right"
#
#         # Subsequent turns: connect to existing letters
#         playable_words = []
#         for word in self.word_list:
#             word_letters = list(word)
#             temp_rack = rack_letters.copy()
#             can_play = True
#             for letter in word_letters:
#                 if letter in temp_rack:
#                     temp_rack.remove(letter)
#                 else:
#                     can_play = False
#                     break
#             if can_play:
#                 playable_words.append(word)
#
#         if not playable_words:
#             return "", [7, 7], "right"
#
#         # Try to connect each playable word to a board letter
#         for word in playable_words:
#             for letter, row, col in board_letters:
#                 location, direction = self.find_connecting_spot(word, letter, row, col)
#                 if location and direction:
#                     return word, location, direction
#
#         # Fallback: skip turn if no connection found
#         return "", [7, 7], "right"
#
#     def find_placement(self, word):
#         """Finds a valid placement connecting to an existing letter (used as fallback)."""
#         board_letters = self.get_board_letters()
#         if not board_letters:
#             return [7, 7], "right"
#
#         for letter, row, col in board_letters:
#             location, direction = self.find_connecting_spot(word, letter, row, col)
#             if location and direction:
#                 return location, direction
#
#         return [7, 7], "right"
#
#     def is_valid_placement(self, word, location, direction):
#         from main import round_number, players, premium_spots, LETTER_VALUES
#         temp_word = Word(word, location, self, direction, self.board.board_array(), round_number, players,
#                          premium_spots, LETTER_VALUES)
#         return temp_word.check_word() == True
#
#     def play_turn(self, board):
#         word, location, direction = self.choose_word()
#         if word == "":
#             print(f"{self.name} skips their turn.")
#             return True
#
#         print(f"{self.name} plays: {word} at {location} going {direction}")
#         from main import round_number, players, premium_spots, LETTER_VALUES
#         word_obj = Word(word, location, self, direction, board.board_array(), round_number, players, premium_spots,
#                         LETTER_VALUES)
#         board.place_word(word, location, direction, self)
#         word_obj.calculate_word_score()
#         return True
