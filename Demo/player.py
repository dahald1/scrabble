from rack import Rack

class Player:
    def __init__(self, bag, rack=None, score=None):
        self.name = ""
        self.rack = rack or Rack(bag)
        self.score = score or 0        

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_rack_str(self):
        return self.rack.get_rack_str()

    def get_rack_arr(self):
        return self.rack.get_rack_arr()
    
    def get_rack_letters(self):
        return [tile.get_letter() for tile in self.get_rack_arr()]

    def increase_score(self, increase):
        self.score += increase

    def get_score(self):
        return self.score
