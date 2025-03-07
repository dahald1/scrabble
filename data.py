from auth import auth

SAVE_DOC_NAME = "save1"

db = auth()


class ScrabbleGame:
    def __init__(self, board=[], turn=0, player_score=0, ai_score=0):
        self.board = board
        self.turn = turn
        self.player_score = player_score
        self.ai_score = ai_score

    def from_dict(self, dict):
        self.board = dict["board"]
        self.turn = dict["turn"]
        self.player_score = dict["player_score"]
        self.ai_score = dict["ai_score"]

    def to_dict(self):
        return {
            "board": self.board,
            "turn": self.turn,
            "player_score": self.player_score,
            "ai_score": self.ai_score
        }

    def print(self):
        print(f"Board: {self.board}\
        Turn: {self.turn}\
        Player Score: {self.player_score}\
        AI Score: {self.ai_score}\
        ")

def save_game(game: ScrabbleGame, save_name):
    doc_ref = db.collection("saves").document(save_name)
    doc_ref.set(game.to_dict())

def load_game(save_name) -> ScrabbleGame | None:
    doc = db.collection("saves").document(save_name).get()

    if not doc.exists:
        print("No document found for '{save_name}'")
        return None

    game = ScrabbleGame()
    game.from_dict(doc.to_dict())
    
    return game


if __name__ == "__main__":
    # placeholder data structure
    data = {
        "board": [{"x": 2, "y": 3, "letter": "b"}, {"x": 3, "y": 3, "letter": "a"}, {"x": 4, "y": 3, "letter": "d"}],
        "turn": 3, 
        "player_score": 6, 
        "ai_score": 0
    }

    game = ScrabbleGame()
    game.from_dict(data)
    save_game(game, SAVE_DOC_NAME)

    game = load_game(SAVE_DOC_NAME)
    game.print()
    