from Demo import board
from player import Player
from word import Word
import random
from dictionary import load_dictionary_upper


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
                cell = board_array[row][col].strip()  # Remove padding spaces
                if len(cell) == 1 and cell.isalpha():  # Check if it's a single letter
                    letters_on_board.append((cell, row, col))
        return letters_on_board
    def choose_word(self):
        rack_letters = [tile.get_letter() for tile in self.get_rack_arr()]
        print("Rack letters: ", rack_letters)
        # print(self.word_list)
        on_board = self.get_board_letters()
        letter_in_board = []
        for i in range(len(on_board)):
            letter_in_board.append(on_board[i][i])

        playable_words = []


        # Iterate over each word in the word_list.
        for word in self.word_list:
            # convert the current word into a list of individual letters.
            counter = 0
            word_letters = list(word)
            # create a copy of the rack_letters to avoid modifying the original rack during checks.
            temp_rack = rack_letters.copy()

            # check each letter in the word to see if it exists in the rack.
            for letter in word_letters:
                # if the letter exists in the temp_rack, remove it (use it).
                if letter in temp_rack:
                    temp_rack.remove(letter)
                    counter += 1
            if counter >= 2 and len(word) == 2:
                print(counter, word)
                can_play = True
            elif counter >= 3 and len(word) == 3:
                print(counter, word)
                can_play = True
            elif counter >= 4 and len(word) == 4:
                print(counter, word)
                can_play = True
            elif counter >= 5 and len(word) == 5:
                print(counter, word)
                can_play = True
            elif counter >= 6 and len(word) == 6:
                print(counter, word)
                can_play = True
            elif counter >= 7 and len(word) == 7:
                print(counter, word)
                can_play = True
            else:
                can_play = False

            if can_play:
                playable_words.append(word)

        # Print the list of playable words.
        # print("playable words: ", playable_words)

        if not playable_words:
            return "", [7, 7], "right"

        chosen_word = random.choice(playable_words)
        location, direction = self.find_placement(chosen_word)
        return chosen_word, location, direction

    def find_placement(self, word):
        print("not an array board: ", self.board)
        board_array = self.board.board_array()
        print("board", board_array)

        # if all cells are empty
        if any(" " not in cell for row in board_array for cell in row):

            # TODO needs to print out the index
            # todo then needs to check if the the letter at the index exits in list of words
            # todo if the letter does exits get the length of words
            # todo then check if their idx in right or down is empty and only place it down or right for now
            # todo then return the starting index
            return [7, 6], "right"

        # todo in the future the AI needs to focus on scoring the most points

        # every cell in a 15x15 board
        for row in range(15):
            for col in range(15):
                # check if the word fits within the board when placed horizontally (right)
                if col + len(word) <= 15:
                    # check if placing the word at (row, col) in the right is valid
                    if self.is_valid_placement(word, [row, col], "right"):
                        return [row, col], "right"  # return the valid position and direction

                # check if the word fits within the board when placed vertically (down)
                if row + len(word) <= 15:
                    # check if placing the word at (row, col) in the "down" direction is valid
                    if self.is_valid_placement(word, [row, col], "down"):
                        return [row, col], "down"  # Return the valid position and direction

        # if no valid placement is found, default to starting at the center of the board
        return [7, 7], "right"

    def is_valid_placement(self, word, location, direction):
        from start import round_number, players, premium_spots, LETTER_VALUES
        temp_word = Word(word, location, self, direction, self.board.board_array(), round_number, players,
                         premium_spots, LETTER_VALUES)
        checked = temp_word.check_word()
        if checked:
            return True
        else:
            return False

    def play_turn(self, board):
        word, location, direction = self.choose_word()
        if word == "":
            print(f"{self.name} skips their turn.")
            return True

        print(f"{self.name} plays: {word} at {location} going {direction}")
        from start import round_number, players, premium_spots, LETTER_VALUES
        word_obj = Word(word, location, self, direction, board.board_array(), round_number, players, premium_spots,
                        LETTER_VALUES)
        board.place_word(word, location, direction, self)
        word_obj.calculate_word_score()
        return True







































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

