
from board import Board
from bag import Bag
from player import Player
from word import Word
from bot import AIPlayer

LETTER_VALUES = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 1,
                 "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1,
                 "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "#": 0}

round_number = 1
players = []
skipped_turns = 0
premium_spots = []


def turn(player, board, bag):
    global round_number, players, skipped_turns, premium_spots

    if (skipped_turns < 6) or (player.rack.get_rack_length() == 0 and bag.get_remaining_tiles() == 0):
        print("\nRound " + str(round_number) + ": " + player.get_name() + "'s turn \n")
        print(board.get_board())
        print("\n" + player.get_name() + "'s Letter Rack: " + player.get_rack_str())

        if not isinstance(player, AIPlayer):
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

            # Pass premium_spots along with round_number and players
            word = Word(word_to_play, location, player, direction, board.board_array(), round_number, players,
                        premium_spots, LETTER_VALUES)

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

            if word.get_word() == "":
                print("Your turn has been skipped.")
                skipped_turns += 1
            else:
                board.place_word(word_to_play, location, direction, player)
                word.calculate_word_score()
                skipped_turns = 0
        else:
            player.play_turn(board)
            if player.get_rack_str() == "":
                skipped_turns += 1
            else:
                skipped_turns = 0

        print("\n" + player.get_name() + "'s score is: " + str(player.get_score()))

        if players.index(player) != (len(players) - 1):
            player = players[players.index(player) + 1]
        else:
            player = players[0]
            round_number += 1

        turn(player, board, bag)
    else:
        end_game()


def start_game():
    global round_number, players, skipped_turns
    board = Board()
    bag = Bag()

    print("\nWelcome to Scrabble! You'll play against an AI opponent.")
    players.clear()

    players.append(Player(bag))
    players[0].set_name(input("Please enter your name: "))

    players.append(AIPlayer(bag, board))

    round_number = 1
    skipped_turns = 0
    current_player = players[0]
    turn(current_player, board, bag)


def end_game():
    global players
    highest_score = 0
    winning_player = ""
    for player in players:
        if player.get_score() > highest_score:
            highest_score = player.get_score()
            winning_player = player.get_name()
    print("The game is over! " + winning_player + ", you have won!")

    if input("\nWould you like to play again? (y/n)").upper() == "Y":
        start_game()


if __name__ == "__main__":
    start_game()

