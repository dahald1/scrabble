class Board:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]  # Empty board

    def is_valid_placement(self, word, start_x, start_y, direction):
        """Check if the word can be placed without overlapping existing letters."""
        if direction == "horizontal":
            if start_x + len(word) > self.size:
                return False  # Word goes out of bounds
            for i, letter in enumerate(word):
                if self.grid[start_y][start_x + i] != ' ':
                    return False  # Spot is already occupied
        elif direction == "vertical":
            if start_y + len(word) > self.size:
                return False  # Word goes out of bounds
            for i, letter in enumerate(word):
                if self.grid[start_y + i][start_x] != ' ':
                    return False  # Spot is already occupied
        return True

    def place_word(self, word: str, start_x: int, start_y: int, direction: str):
        """Places a word on the board if valid."""
        if not self.is_valid_placement(word, start_x, start_y, direction):
            print("Invalid placement! The word overlaps existing letters or goes out of bounds.")
            return False  # Word placement failed

        if direction == "horizontal":
            for i, letter in enumerate(word):
                self.grid[start_y][start_x + i] = letter
        elif direction == "vertical":
            for i, letter in enumerate(word):
                self.grid[start_y + i][start_x] = letter
        return True  # Word placed successfully

    def display(self):
        for row in self.grid:
            print(' '.join(row))
