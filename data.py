"""Contains functions for saving and loading game data from database"""
from auth import auth

SAVE_DOC_NAME = "save1"
DEBUG = True

class ScrabbleGame:
    """Class representing Scrabble game data"""

    def __init__(self, board=None, turn=0, player_score=0, ai_score=0):
        if board is None:
            board = []

        self.board = board
        self.turn = turn
        self.player_score = player_score
        self.ai_score = ai_score

    def from_dict(self, dictionary):
        """Sets fields to passed dictionary values"""
        self.board = dictionary["board"]
        self.turn = dictionary["turn"]
        self.player_score = dictionary["player_score"]
        self.ai_score = dictionary["ai_score"]

    def to_dict(self):
        """Returns game data as a dictionary"""
        return {
            "board": self.board,
            "turn": self.turn,
            "player_score": self.player_score,
            "ai_score": self.ai_score
        }

    def print(self):
        """Prints game data for debugging"""
        print(f"Board: {self.board}\
        Turn: {self.turn}\
        Player Score: {self.player_score}\
        AI Score: {self.ai_score}\
        ")

class DataManager:
    """holds user account, performs authentication, orchestrates saving/loading games"""

    def __init__(self):
        self.database = auth()

        self.username = None
        self.saved_games = None
        self.game_history = None
        self.authenticated = False
        self.user_doc_ref = None

        self.active_game: ScrabbleGame = None

    def authenticate_user(self, entered_username, entered_password):
        """authenticates user and loads user data"""
        user_doc_ref = self.database.collection("users").document(entered_username)
        user_doc = user_doc_ref.get()

        if not user_doc.exists:
            if DEBUG:
                print(f"No document found for user: {entered_username}")
            return 0

        account_data = user_doc.to_dict()

        actual_password = account_data["password"]

        if entered_password == actual_password:
            self.username = entered_username
            self.saved_games = account_data["saved_games"]
            self.game_history = account_data["game_history"]
            self.user_doc_ref = user_doc_ref
            self.authenticated = True
            return 1

        return 0

    def sign_up(self, entered_username, entered_password):
        """creates a new account for a user if username is free"""
        user_doc_ref = self.database.collection("users").document(entered_username)
        user_doc = user_doc_ref.get()

        # if a user doc alreadys exists with username
        if user_doc.exists:
            return 0

        # username is available
        user_doc_ref.set({
            "password": entered_password,
            "saved_games": {},
            "game_history": []
        })

        self.username = entered_username
        self.saved_games = {}
        self.game_history = []
        self.user_doc_ref = user_doc_ref
        self.authenticated = True

        return 1

    def save_game(self, save_name):
        """saves game to firestore document with id save_name"""

        if not self.authenticated:
            if DEBUG:
                print("Cannot save game; not authenticated")
            return 0

        game_data = self.active_game.to_dict()

        # if save already exists with save_name
        if save_name in self.saved_games:
            game_doc_ref = self.saved_games[save_name]
            game_doc_ref.set(game_data)
        else:
            # makes a new game save with name save_name
            _, new_game_doc_ref = self.database.collection("games").add(game_data)
            self.saved_games[save_name] = new_game_doc_ref
            self.user_doc_ref.set({"saved_games": self.saved_games}, merge=True)

        return 1

    def load_game(self, save_name):
        """loads game from firestore document with id save_name"""

        if not self.authenticated:
            if DEBUG:
                print("Cannot load game; not authenticated")
            return 0

        if not save_name in self.saved_games:
            if DEBUG:
                print(f"Cannot load game; game '{save_name}' not found")
            return 0

        doc = self.saved_games[save_name].get()

        if not doc.exists:
            if DEBUG:
                print("No document found for game: {save_name}")
            return 0

        loaded_game = ScrabbleGame()
        loaded_game.from_dict(doc.to_dict())

        self.active_game = loaded_game

        return 1


if __name__ == "__main__":
    data_manager = DataManager()

    data_manager.authenticate_user("jmathies", "password")

    # placeholder data structure
    data = {
        "board": [{"x": 2, "y": 3, "letter": "b"}, \
                  {"x": 3, "y": 3, "letter": "a"}, \
                  {"x": 4, "y": 3, "letter": "d"}],
        "turn": 4,
        "player_score": 6,
        "ai_score": 0
    }

    game = ScrabbleGame()
    game.from_dict(data)
    data_manager.active_game = game

    data_manager.save_game(SAVE_DOC_NAME)
    data_manager.load_game(SAVE_DOC_NAME)

    data_manager.active_game.print()
    