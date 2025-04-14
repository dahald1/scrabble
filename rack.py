from window import MAT_POSITIONS_FILLED
from window import Tile
from bag import LETTER_VALUES
from tile import Tile

empty_positions = []

class Rack:
    def __init__(self, bag, rack=None):
        if rack:
            self.rack = [Tile(letter, LETTER_VALUES) for letter in rack]
        else:
            self.rack = []

        self.bag = bag
        if not rack:
            self.initialize()

    def add_to_rack(self):
        self.rack.append(self.bag.take_from_bag())

    def insert_to_rack(self, index):
        tile = self.bag.take_from_bag()
        self.rack.insert(index, tile)

    def initialize(self):
        for i in range(7):
            self.add_to_rack()

    def get_rack_str(self):
        return ", ".join(str(item.get_letter()) for item in self.rack if item is not None)

    def get_rack_arr(self):
        return self.rack

    def remove_from_rack(self, tile, position, preserve_positions=False):
        if preserve_positions:
            self.rack[position] = None
        else:
            self.rack.remove(tile)


    def get_rack_length(self):
        return len(self.rack)

    def replenish_rack(self, player):
        for index, tile in enumerate(self.rack):
            if tile is None:
                self.rack[index] = self.bag.take_from_bag()
                empty_positions.append(index)
                empty_positions.sort()
                MAT_POSITIONS_FILLED[index] = True
                print(f"Replaced None at position {index}")  # Debugging
        return empty_positions





