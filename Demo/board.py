import random
import tile as tiles

def load_dictionary(filename):
    dictionary = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            word = line.strip()
            dictionary.add(word)
    return dictionary


class Board:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[' # ' for _ in range(size)] for _ in range(size)]  # Empty board
        self.add_premium_squares()
        # self.place_first_word("horizontal")

    def get_board(self):
        # Returns the board in string form.
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(
            str(item) for item in range(10, 15)) + " |"
        board_str += ("\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
                      "_\n")
        board = list(self.grid)
        for i in range(len(board)):
            if i < 10:
                board[i] = str(i) + "  | " + " | ".join(str(item) for item in board[i]) + " |"
            if i >= 10:
                board[i] = str(i) + " | " + " | ".join(str(item) for item in board[i]) + " |"
        board_str += ("\n   |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ "
                      "_|\n").join(
            board)
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
        return board_str

    def place_first_word(self, direction="horizontal"):

        # Center square
        filename = "dictionary.csv"
        dictionary = load_dictionary(filename)

        word = random.choice(list(dictionary))

        center = (self.size // 2, self.size // 2)
        start_x, start_y = center

        if direction == "horizontal":
            start_x -= len(word) // 2  # center the word horizontally
        else:
            start_y -= len(word) // 2  # center the word vertically

        # no negative starting positions
        if start_x < 0 or start_y < 0:
            print("Word is too long to be centered.")
            return False

        # Place the word
        for i, letter in enumerate(word):
            x = start_x + i if direction == "horizontal" else start_x
            y = start_y if direction == "horizontal" else start_y + i

            # Check if tile is empty before placing
            if self.grid[y][x] != ' ':
                print(f"Error: Tile at ({y}, {x}) is already occupied.")
                return False

            # Place the tile
            self.grid[y][x] = letter

        print(f"First word '{word}' placed {direction} at ({start_y}, {start_x})")
        return True

    def add_premium_squares(self):
        # Adds all the premium squares that influence the word's score.
        TRIPLE_WORD = ((0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14))
        DOUBLE_WORD = (
        (1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4),
        (13, 13), (12, 12), (11, 11), (10, 10))
        TRIPLE_LETTER = (
        (1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9))
        DOUBLE_LETTER = (
        (0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11),
        (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))

        for coordinate in TRIPLE_WORD:
            self.grid[coordinate[0]][coordinate[1]] = "TWS"
        for coordinate in TRIPLE_LETTER:
            self.grid[coordinate[0]][coordinate[1]] = "TLS"
        for coordinate in DOUBLE_WORD:
            self.grid[coordinate[0]][coordinate[1]] = "DWS"
        for coordinate in DOUBLE_LETTER:
            self.grid[coordinate[0]][coordinate[1]] = "DLS"

    def place_word(self, word, location, direction, player):
        # global premium_spots
        premium_spots = []
        direction = direction.lower()
        word = word.upper()

        if direction.lower() == "horizontal":
            for i in range(len(word)):
                if self.grid[location[0]][location[1] + i] != "   ":
                    premium_spots.append((word[i], self.grid[location[0]][location[1] + i]))
                self.grid[location[0]][location[1] + i] = " " + word[i] + " "

        elif direction.lower() == "vertical":
            for i in range(len(word)):
                if self.grid[location[0] + i][location[1]] != "   ":
                    premium_spots.append((word[i], self.grid[location[0] + i][location[1]]))
                self.grid[location[0] + i][location[1]] = " " + word[i] + " "

        for letter in word:
            for tile in player.get_rack_arr():
                if tile.get_letter() == letter:
                    player.rack.remove_from_rack(tile)
        player.rack.replenish_rack()

    def board_array(self):
        return self.grid

    def display(self):
        for row in self.grid:
            print(' '.join(row))
