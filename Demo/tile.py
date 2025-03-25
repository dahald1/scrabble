class Tile:
    """
    Class that allows for the creation of a tile. Initializes using an uppercase string of one letter,
    and an integer representing that letter's score.
    """

    def __init__(self, letter, letter_values):
        # Initializes the tile class. Takes the letter as a string, and the dictionary of letter values as arguments.
        self.letter = letter.upper()
        if self.letter in letter_values:
            self.score = letter_values[self.letter]
        else:
            self.score = 0

    def get_letter(self):
        # Returns the tile's letter (string).
        return self.letter

    def get_score(self):
        # Returns the tile's score value.
        return self.score
