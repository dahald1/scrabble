
class Word:
    def __init__(self, word, location, player, direction, board, round_number, players, letter_values):
        self.word = "".join(word.split()).upper()

        self.location = location
        self.player = player
        self.direction = direction.lower()
        self.board = board
        self.round_number = round_number
        self.players = players
        self.premium_spots = None  # Store as instance variable
        self.letter_values = letter_values
        self.ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    def check_word(self):
        word_score = 0
        with open("dictionary.csv") as f:
            dictionary = set(word.strip().upper() for word in f)

        current_board_ltr = ""
        needed_tiles = ""
        blank_tile_val = ""

        if self.round_number == 1 and self.players[0] == self.player and self.word == "":
            print("Please do not skip the first turn. Please enter a word.")
            return False

        elif self.word != "":

            if " " in self.word:
                word_list = list(self.word)

                # Replace blank tile with each letter of the alphabet
                for letter in self.ALPHABET:
                    index = 0
                    for i, tile in enumerate(word_list):
                        index = i
                        if tile == " ":
                            word_list[i] = letter
                    # Check if each combo is valid
                    if "".join(word_list) in dictionary:
                        # Set blank tile back to " " for scoring (0 point value)
                        word_list[index] = " "
                        self.word = "".join(word_list)
                        break
            # Check bounds and process word placement
            if self.direction == "right":
                if self.location[1] + len(self.word) - 1 >= len(self.board[0]):
                    print("Word extends beyond board width.\n")
                    return False
                for i in range(len(self.word)):
                    cell = self.board[self.location[0]][self.location[1] + i]
                    # print(f"Cell [{self.location[0]}, {self.location[1] + i}]: {cell}")
                    if cell in ["   ", "TLS", "TWS", "DLS", "DWS", " * "] or cell == "   ":
                        current_board_ltr += " "
                    elif len(cell.strip()) == 1:
                        current_board_ltr += cell.strip()
                    else:
                        print(f"Invalid board cell at [{self.location[0]}, {self.location[1] + i}]: {cell}")
                        return False
            elif self.direction == "down":
                if self.location[0] + len(self.word) - 1 >= len(self.board):
                    print( "Word extends beyond board height.\n")
                    return False
                for i in range(len(self.word)):
                    cell = self.board[self.location[0] + i][self.location[1]]
                    if cell in ["   ", "TLS", "TWS", "DLS", "DWS", " * "]:
                        current_board_ltr += " "
                    elif len(cell.strip()) == 1:  # Single letter
                        current_board_ltr += cell.strip()
                    else:
                        print(f"Invalid board cell at [{self.location[0] + i}, {self.location[1]}]: {cell}")
                        return False
            else:
                print( "Error: please enter a valid direction.")
                return False

            if str(self.word) not in dictionary:
                print("Please enter a valid dictionary word.\n")
                return False

            for i in range(len(self.word)):
                if current_board_ltr[i] == " ":
                    needed_tiles += self.word[i]
                elif current_board_ltr[i] != self.word[i]:
                    print("Current_board_ltr: " + str(
                        current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                    print( "The letters do not overlap correctly, please choose another word.")
                    return False

            # Rest of the method remains unchanged...
            if blank_tile_val != "":
                needed_tiles = needed_tiles[needed_tiles.index(blank_tile_val):] + needed_tiles[
                                                                                   :needed_tiles.index(blank_tile_val)]
            if (self.round_number != 1 or (
                    self.round_number == 1 and self.players[0] != self.player)) and current_board_ltr == " " * len(
                    self.word):
                print("Current_board_ltr: " + str(
                    current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                print("Please connect the word to a previously played letter.")
                return False

            if self.location[0] > 14 or self.location[1] > 14 or self.location[0] < 0 or self.location[1] < 0 or (
                    self.direction == "down" and (self.location[0] + len(self.word) - 1) > 14) or (
                    self.direction == "right" and (self.location[1] + len(self.word) - 1) > 14):
                print( "Location out of bounds.\n")
                return False

            if self.round_number == 1 and self.players[0] == self.player and self.location != [7, 7]:
                print("The first turn must begin at location (7, 7).\n")
                return False
            return True

    def update_premium_spots(self, premium_spots):
        self.premium_spots = premium_spots

    def calculate_word_score(self):
        word_score = 0
        print("premium spots: ", self.premium_spots)
        for letter in self.word:
            for spot in self.premium_spots:  # Use instance variable instead of global
                if letter == spot[0]:
                    if spot[1] == "TLS":
                        word_score += self.letter_values[letter] * 3
                    elif spot[1] == "DLS":
                        word_score += self.letter_values[letter] * 2
            word_score += self.letter_values[letter]
        for spot in self.premium_spots:  # Use instance variable instead of global
            if spot[1] == "TWS":
                word_score *= 3
            elif spot[1] == "DWS":
                word_score *= 2
        self.player.increase_score(word_score)

    def set_word(self, word):
        self.word = word.upper()

    def set_location(self, location):
        self.location = location

    def set_direction(self, direction):
        self.direction = direction

    def get_word(self):
        return self.word