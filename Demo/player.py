import tilebag as tb

class Player:
    def __init__(self, name: str, tile_bag: tb.TileBag):
        self.name = name
        self.rack = [tile_bag.draw_tile() for _ in range(7)]  # Start with 7 tiles
        self.score = 0

    def play_word(self, word: str, board):
        # Logic to check if word is valid and calculate score
        word_score = sum(tile.value for tile in self.rack if tile and tile.letter in word)
        self.score += word_score
        print(f"{self.name} played '{word}' for {word_score} points!")

    def draw_tiles(self, tile_bag):
        while len(self.rack) < 7 and tile_bag.tiles:
            self.rack.append(tile_bag.draw_tile())

    def display(self):
        for tile in self.rack:
            print(' ', tile)
