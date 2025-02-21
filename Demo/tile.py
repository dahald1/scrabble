class Tile:
    def __init__(self, letter: str, value: int):
        self.letter = letter  # The letter on the tile (e.g., 'A')
        self.value = value    # The point value of the letter (e.g., 1)

    def __str__(self):
        return f"{self.letter}({self.value})"
