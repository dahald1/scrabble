import random
import tile as t

class TileBag:
    def __init__(self):
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tile_distribution = {
            'A': (9, 1), 'B': (2, 3), 'C': (2, 3), 'D': (4, 2), 'E': (12, 1), 'F': (2, 4), 'G': (3, 2), 'H': (4, 2), 'I': (9, 1), 'J': (1, 8), 'K': (1, 5), 'L': (4, 1), 'M': (2, 3), 'N': (6, 1), 'O': (8, 1), 'P': (2, 3), 'Q': (1, 10), 'R': (6, 1), 'S': (4, 1), 'T': (6, 1), 'U': (4, 1), 'V': (2, 4), 'W': (2, 4), 'X': (1, 8), 'Y': (2, 4), 'Z': (1, 10)
        }
        tiles = []
        for letter, (count, value) in tile_distribution.items():
            tiles.extend([t.Tile(letter, value) for _ in range(count)])
        random.shuffle(tiles)
        return tiles

    def draw_tile(self):
        return self.tiles.pop() if self.tiles else None  # Draw a tile from the bag
