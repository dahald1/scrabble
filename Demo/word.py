
class Word:
    def __init__(self, word, location, player, direction, board, round_number, players, premium_spots, letter_values):
        self.word = "".join(word.split()).upper()
        self.location = location
        self.player = player
        self.direction = direction.lower()
        self.board = board
        self.round_number = round_number
        self.players = players
        self.premium_spots = premium_spots  # Store as instance variable
        self.letter_values = letter_values

    def check_word(self):
        word_score = 0
        global dictionary
        if "dictionary" not in globals():
            dictionary = open("dictionary.csv").read().upper()

        current_board_ltr = ""
        needed_tiles = ""
        blank_tile_val = ""

        if self.word != "":
            if " " in self.word:
                while len(blank_tile_val) != 1:
                    blank_tile_val = input("Please enter the letter value of the blank tile: ")
                self.word = self.word[:self.word.index(" ")] + blank_tile_val.upper() + self.word[
                                                                                        (self.word.index(" ") + 1):]

            # Check bounds and process word placement
            if self.direction == "right":
                if self.location[1] + len(self.word) - 1 >= len(self.board[0]):
                    return "Word extends beyond board width.\n"
                # print(f"Checking word '{self.word}' at {self.location} right")
                # print(f"Row {self.location[0]}: {self.board[self.location[0]]}")
                for i in range(len(self.word)):
                    cell = self.board[self.location[0]][self.location[1] + i]
                    # print(f"Cell [{self.location[0]}, {self.location[1] + i}]: {cell}")
                    if cell in ["   ", "TLS", "TWS", "DLS", "DWS", " * "] or cell == "":
                        current_board_ltr += " "
                    elif len(cell.strip()) == 1:
                        current_board_ltr += cell.strip()
                    else:
                        return f"Invalid board cell at [{self.location[0]}, {self.location[1] + i}]: {cell}"
            elif self.direction == "down":
                if self.location[0] + len(self.word) - 1 >= len(self.board):
                    return "Word extends beyond board height.\n"
                for i in range(len(self.word)):
                    cell = self.board[self.location[0] + i][self.location[1]]
                    if cell in [" ", "TLS", "TWS", "DLS", "DWS", " * "]:
                        current_board_ltr += " "
                    elif len(cell.strip()) == 1:  # Single letter
                        current_board_ltr += cell.strip()
                    else:
                        return f"Invalid board cell at [{self.location[0] + i}, {self.location[1]}]: {cell}"
            else:
                return "Error: please enter a valid direction."

            if self.word not in dictionary:
                return "Please enter a valid dictionary word.\n"

            for i in range(len(self.word)):
                if current_board_ltr[i] == " ":
                    needed_tiles += self.word[i]
                elif current_board_ltr[i] != self.word[i]:
                    print("Current_board_ltr: " + str(
                        current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                    return "The letters do not overlap correctly, please choose another word."

            # Rest of the method remains unchanged...
            if blank_tile_val != "":
                needed_tiles = needed_tiles[needed_tiles.index(blank_tile_val):] + needed_tiles[
                                                                                   :needed_tiles.index(blank_tile_val)]

            if (self.round_number != 1 or (
                    self.round_number == 1 and self.players[0] != self.player)) and current_board_ltr == " " * len(
                    self.word):
                print("Current_board_ltr: " + str(
                    current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                return "Please connect the word to a previously played letter."

            for letter in needed_tiles:
                if letter not in self.player.get_rack_str() or self.player.get_rack_str().count(
                        letter) < needed_tiles.count(letter):
                    return "You do not have the tiles for this word\n"

            if self.location[0] > 14 or self.location[1] > 14 or self.location[0] < 0 or self.location[1] < 0 or (
                    self.direction == "down" and (self.location[0] + len(self.word) - 1) > 14) or (
                    self.direction == "right" and (self.location[1] + len(self.word) - 1) > 14):
                return "Location out of bounds.\n"

            if self.round_number == 1 and self.players[0] == self.player and self.location != [7, 7]:
                return "The first turn must begin at location (7, 7).\n"
            return True
        else:
            if input("Are you sure you would like to skip your turn? (y/n)").upper() == "Y":
                if self.round_number == 1 and self.players[0] == self.player:
                    return "Please do not skip the first turn. Please enter a word."
                return True
            else:
                return "Please enter a word."

    def calculate_word_score(self):
        word_score = 0
        for letter in self.word:
            for spot in self.premium_spots:  # Use instance variable instead of global
                if letter == spot[0]:
                    if spot[1] == "TLS":
                        word_score += self.letter_values[letter] * 2
                    elif spot[1] == "DLS":
                        word_score += self.letter_values[letter]
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