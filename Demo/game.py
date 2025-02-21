import tilebag as tb
import player as p
import board as b
class Game:
    def __init__(self, players: list):
        self.tile_bag = tb.TileBag()
        self.board = b.Board()
        self.players = [p.Player(name, self.tile_bag) for name in players]
        self.current_player_index = 0

    def play(self):
        """Main game loop: keeps playing until a player reaches x points."""
        while True:
            self.next_turn()
            # Check if any player has reached 10 points
            for player in self.players:
                if player.score >= 10:
                    print(f"\n{player.name} wins with {player.score} points!")
                    return  # End the game

    def next_turn(self):
        player = self.players[self.current_player_index]
        print(f"\nIt's {player.name}'s turn.")
        print(f"Your tiles: {[tile.letter for tile in player.rack]}")

        while True:
            word = input("Enter a word from your tiles: ").upper()
            if self.is_valid_word(word, player):
                break
            print("Invalid word. Please use only the tiles in your rack.")

        while True:
            try:
                start_x = int(input("Enter the starting column (0-14): "))
                start_y = int(input("Enter the starting row (0-14): "))
                direction = input("Enter direction (H for horizontal, V for vertical): ").upper()
                
                if direction in ('H', 'V') and 0 <= start_x < 15 and 0 <= start_y < 15:
                    if self.board.place_word(word, start_x, start_y, "horizontal" if direction == "H" else "vertical"):
                        break  # Placement was successful, break the loop
            except ValueError:
                pass
            print("Invalid placement. Try again.")

        # Update player score
        word_score = sum(tile.value for tile in player.rack if tile and tile.letter in word)
        player.score += word_score
        print(f"{player.name} played '{word}' for {word_score} points! Total Score: {player.score}")

        # Remove used tiles from rack and draw new ones
        player.rack = [tile for tile in player.rack if tile.letter not in word]
        player.draw_tiles(self.tile_bag)

        # Show updated board
        self.board.display()

        # Move to the next player
        self.current_player_index = (self.current_player_index + 1) % len(self.players)


    def is_valid_word(self, word, player):
        """Check if the word can be formed with the player's tiles."""
        available_letters = [tile.letter for tile in player.rack]
        for letter in word:
            if letter in available_letters:
                available_letters.remove(letter)
            else:
                return False
        return True