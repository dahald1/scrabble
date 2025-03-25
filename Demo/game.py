import tilebag as tb
import player as p
import board as b
from board import load_dictionary
import word as w


class Game:
    def __init__(self):
        self.tile_bag = tb.Bag()
        self.board = b.Board()
        self.current_player_index = 0

    def is_valid_word(self, word):
        filename = "dictionary.csv"
        dictionary = load_dictionary(filename)

        if word.lower() not in dictionary:
            print("This is not a valid word")
            return False

        return True

    def turn(self, player, board, bag):
        # Begins a turn, by displaying the current board, getting the information to play a turn, and creates a
        # recursive loop to allow the next person to play.
        global round_number, players, skipped_turns

        # If the number of skipped turns is less than 6 and a row, and there are either tiles in the bag,
        # or no players have run out of tiles, play the turn. Otherwise, end the game.
        if (skipped_turns < 6) or (player.rack.get_rack_length() == 0 and bag.get_remaining_tiles() == 0):

            # Displays whose turn it is, the current board, and the player's rack.
            print("\nRound " + str(round_number) + ": " + player.get_name() + "'s turn \n")
            print(board.get_board())
            print("\n" + player.get_name() + "'s Letter Rack: " + player.get_rack_str())

            # Gets information in order to play a word.
            word_to_play = input("Word to play: ")
            location = []
            col = input("Column number: ")
            row = input("Row number: ")
            if (col == "" or row == "") or (
                    col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
                location = [-1, -1]
            else:
                location = [int(row), int(col)]
            direction = input("Direction of word (right or down): ")

            word = w.Word(word_to_play, location, player, direction, board.board_array())

            # If the first word throws an error, creates a recursive loop until the information is given correctly.
            checked = word.check_word()
            while checked != True:
                print(checked)
                word_to_play = input("Word to play: ")
                word.set_word(word_to_play)
                location = []
                col = input("Column number: ")
                row = input("Row number: ")
                if (col == "" or row == "") or (
                        col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
                    location = [-1, -1]
                else:
                    word.set_location([int(row), int(col)])
                    location = [int(row), int(col)]
                direction = input("Direction of word (right or down): ")
                word.set_direction(direction)
                checked = word.check_word()

            # If the user has confirmed that they would like to skip their turn, skip it.
            # Otherwise, plays the correct word and prints the board.
            if word.get_word() == "":
                print("Your turn has been skipped.")
                skipped_turns += 1
            else:
                board.place_word(word_to_play, location, direction, player)
                word.calculate_word_score()
                skipped_turns = 0

            # Prints the current player's score
            print("\n" + player.get_name() + "'s score is: " + str(player.get_score()))

            # Gets the next player.
            if players.index(player) != (len(players) - 1):
                player = players[players.index(player) + 1]
            else:
                player = players[0]
                round_number += 1

            # Recursively calls the function in order to play the next turn.
            self.turn(player, board, bag)

        # If the number of skipped turns is over 6 or the bag has both run out of tiles and a player is out of tiles, end the game.
        else:
            self.end_game()

    def start_game(self):
        # Begins the game and calls the turn function.
        global round_number, players, skipped_turns
        players_names =["Alice", "Bob"]
        num_of_players = 2
        players = []

        # Welcomes players to the game and allows players to choose their name.
        print("\nWelcome to Scrabble! Please enter the names of the players below.")
        for i in range(num_of_players):
            players.append(p.Player(self.tile_bag))
            players[i].set_name(players_names[i])

        # Sets the default value of global variables.
        round_number = 1
        skipped_turns = 0
        current_player = players[0]
        self.turn(current_player, self.board, self.tile_bag)

    def end_game(self):
        # Forces the game to end when the bag runs out of tiles.
        highest_score = 0
        winning_player = ""
        for player in players:
            if player.get_score > highest_score:
                highest_score = player.get_score()
                winning_player = player.get_name()
        print("The game is over! " + winning_player + ", you have won!")

        if input("\nWould you like to play again? (y/n)").upper() == "Y":
            self.start_game()


