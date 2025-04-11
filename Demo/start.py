from board import Board
from bag import Bag
from player import Player
from word import Word
from bot import AIPlayer
import arcade
from window import GameView, Tile  # Import GameView from your original code
from window import TRIPLE_WORD, TRIPLE_LETTER, DOUBLE_WORD, DOUBLE_LETTER, CENTER
from data import ScrabbleGame

LETTER_VALUES = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 1,
                 "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1,
                 "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "#": 0}

round_number = 1
players = []
skipped_turns = 0
premium_spots = []


def get_word_from_tiles(added_tiles, board_matrix):
    """Determine the word and direction from the added tiles."""
    if not added_tiles:
        return "", [-1, -1], ""

    added_tiles.sort(key=lambda x: (x[0], x[1]))
    same_row = all(tile[0] == added_tiles[0][0] for tile in added_tiles)
    same_col = all(tile[1] == added_tiles[0][1] for tile in added_tiles)

    if not (same_row or same_col):
        return "", [-1, -1], ""

    if same_row:
        direction = "right"
        row = added_tiles[0][0]
        col_start = added_tiles[0][1]
        while col_start > 0 and board_matrix[row][col_start - 1] != "":
            col_start -= 1
        word = ""
        col = col_start
        while col < 15 and board_matrix[row][col] != "":
            word += board_matrix[row][col]
            col += 1
        location = [row, col_start]
    else:
        direction = "down"
        col = added_tiles[0][1]
        row_start = added_tiles[0][0]
        while row_start > 0 and board_matrix[row_start - 1][col] != "":
            row_start -= 1
        word = ""
        row = row_start
        while row < 15 and board_matrix[row][col] != "":
            word += board_matrix[row][col]
            row += 1
        location = [row_start, col]

    return word, location, direction


def setup():
    """Initialize the game state."""
    global round_number, players, skipped_turns, premium_spots
    board = Board()
    bag = Bag()

    players.clear()
    players.append(Player(bag))
    players[0].set_name("James")
    players.append(AIPlayer(bag, board))

    round_number = 1
    skipped_turns = 0
    current_player = players[0]

    print("\nWelcome to Scrabble! You'll play against an AI opponent.")
    print("\nRound " + str(round_number) + ": " + current_player.get_name() + "'s turn \n")
    print(board.get_board())
    print("\n" + current_player.get_name() + "'s Letter Rack: " + current_player.get_rack_str())

    return board, bag, current_player


class GameController:
    def __init__(self, game_view, board, bag, current_player):
        self.game_view = game_view
        self.board = board
        self.bag = bag
        self.current_player = current_player
        self.prev_board_matrix = None
        self.turn_ended = False
        self.status = ""
        # self.AI = AIPlayer(self.board, self.bag)
        # print(self.AI.playing_position())

    def sync_board_with_matrix(self):
        """Sync the Board instance with the matrix from GameView."""
        matrix = self.game_view.get_board_matrix()
        for row in range(15):
            for col in range(15):
                if matrix[row][col] != "   ":
                    self.board.board_array()[row][col] = matrix[row][col]
                else:
                    self.board.board_array()[row][col] = "   "
        self.board.add_premium_squares()

    def process_turn(self):
        """Process the current player's turn."""
        # Dictionary that saves the current game state
        global round_number, skipped_turns
        save_game = {
            'round_number': round_number,
            'skipped_turns': skipped_turns,
            'current_player': self.current_player.get_name(),
            'board_state': self.board.get_board(),  # Assuming get_board() returns the current board state
            'player_scores': {player.get_name(): player.get_score() for player in players},
            'player_racks': {player.get_name(): player.get_rack_str() for player in players},
            'remaining_tiles': self.bag.get_remaining_tiles(),
            'status': self.status,  # Assuming you have a status attribute for game status
        }

        # end the game if conditions are met
        if (skipped_turns >= 6) or (
                self.current_player.rack.get_rack_length() == 0 and self.bag.get_remaining_tiles() == 0):
            self.end_game()
            save_game['status'] = "finished"
            # save or update game state somewhere
            # self.save_game_state(save_game)  # call save game method here
            return

        if not isinstance(self.current_player, AIPlayer):
            added_tiles = self.game_view.find_added_tiles(self.prev_board_matrix, self.game_view.get_board_matrix())
            if not added_tiles:
                print("No tiles were placed. Your turn has been skipped.")
                skipped_turns += 1
            else:
                word_to_play, location, direction = get_word_from_tiles(added_tiles, self.game_view.get_board_matrix())
                str("".join(word_to_play.split()))
                print(word_to_play, location, direction)
                if word_to_play == "":
                    print("Invalid tile placement. Your turn has been skipped.")
                    skipped_turns += 1
                    for row in range(15):
                        for col in range(15):
                            self.game_view.get_board_matrix()[row][col] = self.prev_board_matrix[row][col]
                else:
                    word = Word(word_to_play, location, self.current_player, direction, self.board.board_array(),
                                round_number, players, premium_spots, LETTER_VALUES)
                    checked = word.check_word()
                    if not checked:
                        print(f"Invalid word: {checked}")
                        print("Your turn has been skipped.")
                        skipped_turns += 1
                        for row in range(15):
                            for col in range(15):
                                self.game_view.get_board_matrix()[row][col] = self.prev_board_matrix[row][col]
                    else:
                        self.board.place_word(word_to_play, location, direction, self.current_player)
                        word.calculate_word_score()
                        skipped_turns = 0
                        print(f"Word played: {word_to_play} at {location} going {direction}")
                        print(f"Current rack1: {self.current_player.rack.get_rack_str()}")
                        # self.current_player.rack.replenish_rack()
                        Tile.refill_mat(self.game_view, player_rack=self.current_player.get_rack_str())
                        self.sync_board_with_matrix()
        elif isinstance(self.current_player, AIPlayer):
            ai_word, location, direction = AIPlayer.choose_word(self.current_player)
            word = Word(ai_word, location, self.current_player, direction, self.board.board_array(),
                        round_number, players, premium_spots, LETTER_VALUES)
            # print("AI chosen word: ", word, location, direction)
            self.board.place_word(ai_word, location, direction, self.current_player)
            word.calculate_word_score()
            print(f"Word played: {word} at {location} going {direction}")
            Tile.ai_place_tile(self.game_view, ai_word, location[0], location[1], direction)
            self.current_player.rack.replenish_rack()
            print(f"Current rack2: {self.current_player.rack.get_rack_str()}")
            Tile.refill_mat(self.game_view, player_rack=self.current_player.get_rack_str())
            self.sync_board_with_matrix()  # ensure board is up-to-date

        print("\n" + self.current_player.get_name() + "'s score is: " + str(self.current_player.get_score()))

        current_player_index = players.index(self.current_player)
        self.current_player = players[(current_player_index + 1) % len(players)]
        if current_player_index == len(players) - 1:
            round_number += 1

        print("\nRound " + str(round_number) + ": " + self.current_player.get_name() + "'s turn \n")
        print(self.board.get_board())
        print("\n" + self.current_player.get_name() + "'s Letter Rack: " + self.current_player.get_rack_str())

        if isinstance(self.current_player, AIPlayer):
            print("AI detected, processing AI turn automatically...")
            self.process_turn()

        save_game['status'] = "in_progress"

    def on_key_press(self, key, modifiers):
        """Handle key presses from GameView."""
        print("this gets called ")
        if key == arcade.key.ENTER:
            if self.prev_board_matrix is None:
                self.prev_board_matrix = [row[:] for row in self.game_view.get_board_matrix()]
            self.sync_board_with_matrix()
            print("this gets entered")
            self.process_turn()

    def end_game(self):
        """End the game and determine the winner."""
        highest_score = 0
        winning_player = ""
        for player in players:
            if player.get_score() > highest_score:
                highest_score = player.get_score()
                winning_player = player.get_name()
        print("The game is over! " + winning_player + ", you have won!")

        if input("\nWould you like to play again? (y/n)").upper() == "Y":
            board, bag, current_player = setup()
            self.board = board
            self.bag = bag
            self.current_player = current_player
            self.game_view.tiles.clear()
            Tile.refill_mat(self.game_view, player_rack=self.current_player.get_rack_str())
        else:
            arcade.close_window()


def start_game():
    """Start the game with the GameView instance."""
    board, bag, current_player = setup()
    # TODO This needs to be changed so the tiles match
    game_view = GameView(player_rack=current_player.get_rack_str())  # Pass initial rack
    controller = GameController(game_view, board, bag, current_player)
    game_view.controller = controller

    # Override GameView's on_key_press to include controller logic
    original_on_key_press = game_view.on_key_press

    def new_on_key_press(key, modifiers):
        original_on_key_press(key, modifiers)
        controller.on_key_press(key, modifiers)

    game_view.on_key_press = new_on_key_press

    game_view.setup()
    return game_view
