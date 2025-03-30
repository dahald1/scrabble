
class Board:
    def __init__(self):
        # from window import GameView
        # game = GameView().get_board_matrix()
        self.board = [["   " for i in range(15)] for j in range(15)]
        # self.board = game
        self.add_premium_squares()
        self.board[7][7] = " * "
    def get_board(self):
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(
            str(item) for item in range(10, 15)) + " |"
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        board = list(self.board)
        for i in range(len(board)):
            if i < 10:
                board[i] = str(i) + "  | " + " | ".join(str(item) for item in board[i]) + " |"
            if i >= 10:
                board[i] = str(i) + " | " + " | ".join(str(item) for item in board[i]) + " |"
        board_str += "\n   |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|\n".join(
            board)
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
        return board_str

    def add_premium_squares(self):
        TRIPLE_WORD_SCORE = ((0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14))
        DOUBLE_WORD_SCORE = (
        (1, 1), (2, 2), (3, 3), (4, 4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4),
        (13, 13), (12, 12), (11, 11), (10, 10))
        TRIPLE_LETTER_SCORE = (
        (1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9))
        DOUBLE_LETTER_SCORE = (
        (0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11),
        (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))

        for coordinate in TRIPLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "TWS"
        for coordinate in TRIPLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "TLS"
        for coordinate in DOUBLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "DWS"
        for coordinate in DOUBLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "DLS"

    def place_word(self, word, location, direction, player):
        premium_spots = []
        direction = direction.lower()
        word = word.upper()

        if direction == "right":
            if location[1] + len(word) - 1 >= len(self.board[0]):
                raise ValueError("Word extends beyond board width")
            for i in range(len(word)):
                cell = self.board[location[0]][location[1] + i]
                if cell in ["TWS", "TLS", "DWS", "DLS", " * "]:
                    premium_spots.append((word[i], cell))
                self.board[location[0]][location[1] + i] = word[i]
        elif direction == "down":
            if location[0] + len(word) - 1 >= len(self.board):
                raise ValueError("Word extends beyond board height")
            for i in range(len(word)):
                cell = self.board[location[0] + i][location[1]]
                if cell in ["TWS", "TLS", "DWS", "DLS", " * "]:
                    premium_spots.append((word[i], cell))
                self.board[location[0] + i][location[1]] = word[i]

        for letter in word:
            for tile in player.get_rack_arr():
                if tile.get_letter() == letter:
                    player.rack.remove_from_rack(tile)
                    break
        player.rack.replenish_rack()
        return premium_spots  # Return for scoring in Word class

    def board_array(self):
        return self.board
