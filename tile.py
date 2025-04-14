class Tile:
    def __init__(self, letter, letter_values):
        self.letter = letter.upper()
        if self.letter in letter_values:
            self.score = letter_values[self.letter]
        else:
            self.score = 0

    def get_letter(self):
        return self.letter

    def get_score(self):
        return self.score