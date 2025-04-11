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
                    # if board_array[r][c] in {' ', "TLS", "TWS", "DLS", "DWS"}:
                    #     space_counter += 1  # found a space
                    if not board_array[r][c].isalpha():
                        space_counter += 1
                    else:
                        break

                possible_positions[(cell, row, col, dir_name)] = space_counter

        return possible_positions  # return the dictionary of possible positions

    def choose_word(self):
        rack_letters = [tile.get_letter() for tile in self.get_rack_arr()]
        print("before checking: ", rack_letters)
        playing_positions = self.playing_position()

        playable_words = []

        for (letter, row, col, direction), spaces in playing_positions.items():

            # iterate over each word in the word_list.
            for word in self.word_list:
                # convert the current word into a list of individual letters.
                if len(word) > spaces:
                    continue

                word_letters = list(word)
                # create a copy of the rack_letters to avoid modifying the original rack during checks.
                temp_rack = rack_letters.copy()
                counter = 0
                # check if the letter is at the start
                # this will check for Right and Down
                if (direction == "right" or direction == "down") and word_letters[0] == letter:
                    # check each letter in the word to see if it exists in the rack.
                    for rack_letter in word_letters[1:]:
                        # if the letter exists in the temp_rack, remove it (use it).
                        if rack_letter in temp_rack:
                            temp_rack.remove(rack_letter)
                            counter += 1
                    if counter + 1 >= len(word) and len(word) >= 2:
                        if direction == "right":
                            playable_words.append((word, row + len(word) - 1, col, "right"))
                        if direction == "down":
                            playable_words.append((word, row, col + (len(word) - 1), "down"))
                # check if the letter is at the start, this will check for Up and Left
                elif (direction == "left" or direction == "up") and word_letters[-1] == letter:
                    # check each letter in the word to see if it exists in the rack.
                    for rack_letter in word_letters[:-1]:
                        # if the letter exists in the temp_rack, remove it (use it).
                        if rack_letter in temp_rack:
                            temp_rack.remove(rack_letter)
                            counter += 1
                    if counter + 1 >= len(word) and len(word) >= 2:
                        if direction == "up":
                            playable_words.append((word, row, col - (len(word) - 1), "down"))
                        if direction == "left":
                            playable_words.append((word, row - (len(word) - 1), col, "right"))

        # randomly choose a word and return the word, staring location and the
        # directions the word should be going
        # print(playable_words)
        random.choice(playable_words)  # Shuffle to randomize order
        for chosen_word in playable_words:
            print(chosen_word)
            word = chosen_word[0]
            location = (chosen_word[1], chosen_word[2])
            direction = chosen_word[3]
            can_play_word = self.is_valid_placement(word, location, direction)
            if can_play_word:
                return word, location, direction

    def is_valid_placement(self, word, location, direction):
        from start import round_number, players, premium_spots, LETTER_VALUES
        temp_word = Word(word, location, self, direction, self.board.board_array(), round_number, players,
                         premium_spots, LETTER_VALUES)
        checked = temp_word.check_word()
        if checked:
            return True
        else:
            return False
