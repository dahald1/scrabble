from Demo.window import MAT_POSITIONS_FILLED
from window import Tile

class Rack:
    def __init__(self, bag):
        self.rack = []
        self.bag = bag
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
        return ", ".join(str(item.get_letter()) for item in self.rack)

    def get_rack_arr(self):
        return self.rack

    def remove_from_rack(self, tile):
        self.rack.remove(tile)

    def get_rack_length(self):
        return len(self.rack)

    def replenish_rack(self):
        empty_positions = Tile.get_empty_mat_positions()
        # while self.get_rack_length() < 7 and self.bag.get_remaining_tiles() > 0:
        for i, position in enumerate(empty_positions):
            self.insert_to_rack(position)
            MAT_POSITIONS_FILLED[position] = True
            # self.add_to_rack()