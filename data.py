"""Contains functions for saving and loading game data from database"""
from uuid import uuid4
from google.cloud import firestore
from auth import auth

DEFAULT_SAVE_NAME = "save1"
LOBBY_LIST_DOC = "lobby_list"
LOBBY_ID_LENGTH = 6
DEBUG = False

db = auth()

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

class MultiplayerLobbyManager:
    """Manages multiplayer lobby data for joining/hosting games"""

    def __init__(self, data_manager):
        self.database = db
        self.data_manager = data_manager

        self.lobby_list_doc_ref = self.database.collection("lobbies").document(LOBBY_LIST_DOC)
        self.lobby_list_data = self.lobby_list_doc_ref.get().to_dict()
        self.lobby_list_doc_watch = self.lobby_list_doc_ref.on_snapshot(self.on_lobby_list_snapshot)

        self.connected_to_lobby = False
        self.connected_lobby_id = None
        self.connected_lobby_doc_ref = None
        self.connected_lobby_doc_watch = None
        self.connected_lobby_data = None

    def on_lobby_list_snapshot(self, doc_snapshot_list, _changes, _read_time):
        """Updates lobby list data when its document changes (new lobby, lobby removed)"""
        doc_snapshot = doc_snapshot_list[0]
        self.lobby_list_data = doc_snapshot.to_dict()

    def on_lobby_snapshot(self, doc_snapshot_list, _changes, _read_time):
        """Updates lobby data when its document changes (player joined, left, etc.)"""
        if not doc_snapshot_list:
            self.connected_to_lobby = False
            return

        doc_snapshot = doc_snapshot_list[0]
        self.connected_lobby_data = doc_snapshot.to_dict()

    def join_lobby(self, lobby_id):
        """Handles player joining a lobby on Firestore side"""
        if not lobby_id in self.lobby_list_data:
            return 0

        lobby_doc_ref = self.lobby_list_data[lobby_id]
        lobby_data = lobby_doc_ref.get().to_dict()

        # if lobby is occupied
        if lobby_data["player_two"] is not None:
            return 0

        lobby_doc_ref.set({"player_two": self.data_manager.username}, merge=True)
        self.connected_lobby_id = lobby_id
        self.watch_lobby(lobby_doc_ref)
        return 1

    def create_lobby(self):
        """Creates a lobby in Firestore"""
        lobby_id = str(uuid4())[:LOBBY_ID_LENGTH]

        # lobby_id collision resolution
        while lobby_id in self.lobby_list_data:
            lobby_id = str(uuid4())[:LOBBY_ID_LENGTH]

        lobby_data = {
            "player_one": self.data_manager.username,
            "player_two": None,
            "start_game": False,
            "game_ref"  : None
        }

        _, new_lobby_doc_ref = self.database.collection("lobbies").add(lobby_data)
        self.lobby_list_doc_ref.set({lobby_id: new_lobby_doc_ref}, merge=True)
        self.connected_lobby_id = lobby_id
        self.watch_lobby(new_lobby_doc_ref)

    def leave_lobby(self):
        """Handles player leaving on Firestore side"""
        if not self.connected_lobby_data:
            if DEBUG:
                print("Not connected to lobby!")
            return

        # player one is the lobby host, if they leave dissolve lobby
        if self.data_manager.username == self.connected_lobby_data["player_one"]:
            self.connected_lobby_doc_watch.unsubscribe()
            self.connected_lobby_doc_ref.delete()
            self.lobby_list_doc_ref.set({self.connected_lobby_id: firestore.DELETE_FIELD},
                                         merge=True)
            return

        self.connected_lobby_doc_ref.set({"player_two": None}, merge=True)

    def start_game(self):
        """Creates game in Firestore and links it to lobby doc"""
        assert self.full_lobby()

        print("Starting game not implemented!")

    def watch_lobby(self, lobby_doc_ref):
        """Starts watching passed lobby_doc_ref and gets lobby data"""
        if self.connected_lobby_doc_watch:
            self.connected_lobby_doc_watch.unsubscribe()

        self.connected_to_lobby = True
        self.connected_lobby_doc_ref = lobby_doc_ref
        self.connected_lobby_doc_watch = lobby_doc_ref.on_snapshot(self.on_lobby_snapshot)
        self.connected_lobby_data = lobby_doc_ref.get().to_dict()

    def is_host(self):
        """Returns whether a user is the host of their lobby, if in one"""
        if not self.connected_lobby_data:
            if DEBUG:
                print("Not connected to lobby!")
            return False

        if self.data_manager.username == self.connected_lobby_data["player_one"]:
            return True
        return False

    def full_lobby(self):
        """Returns whether a lobby is full and ready to start"""
        if not self.connected_lobby_data:
            if DEBUG:
                print("Not connected to lobby!")
            return False

        if (self.connected_lobby_data["player_one"] and
            self.connected_lobby_data["player_two"]):
            return True
        return False

class DataManager:
    """Holds user account, performs authentication, orchestrates saving/loading games"""

    def __init__(self):
        self.database = db

        self.username = None
        self.saved_games = None
        self.game_history = None
        self.authenticated = False
        self.user_doc_ref = None

    def authenticate_user(self, entered_username, entered_password):
        """Authenticates user and loads user data"""
        if len(entered_username) == 0:
            if DEBUG:
                print("Blank username entered")
            return 0

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
        if len(entered_username) == 0:
            if DEBUG:
                print("Blank username entered")
            return 0

        user_doc_ref = self.database.collection("users").document(entered_username)
        user_doc = user_doc_ref.get()

        # if a user doc alreadys exists with username
        if user_doc.exists:
            if DEBUG:
                print(f"Username already used: {entered_username}")
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

    def save_game(self, game_data, save_name=DEFAULT_SAVE_NAME):
        """saves game to firestore document with id save_name"""

        if not self.authenticated:
            if DEBUG:
                print("Cannot save game; not authenticated")
            return 0

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

    def load_game(self, save_name=DEFAULT_SAVE_NAME) -> dict | None:
        """loads game from firestore document with id save_name"""

        if not self.authenticated:
            if DEBUG:
                print("Cannot load game; not authenticated")
            return None

        if not save_name in self.saved_games:
            if DEBUG:
                print(f"Cannot load game; game '{save_name}' not found")
            return None

        doc = self.saved_games[save_name].get()

        if not doc.exists:
            if DEBUG:
                print("No document found for game: {save_name}")
            return None

        game_data = doc.to_dict()

        return game_data


if __name__ == "__main__":
    test_data_manager = DataManager()

    test_data_manager.authenticate_user("jmathies", "password")

    # placeholder data structure
    data = {
        "board": [{"x": 2, "y": 3, "letter": "b"}, \
                  {"x": 3, "y": 3, "letter": "a"}, \
                  {"x": 4, "y": 3, "letter": "d"}],
        "turn": 4,
        "player_score": 6,
        "ai_score": 0
    }

    test_data_manager.save_game(data)
    loaded_data = test_data_manager.load_game()

    assert data == loaded_data
    # ---------------------

    multiplayer_lobby_manager = MultiplayerLobbyManager(test_data_manager)
    multiplayer_lobby_manager.create_lobby()
    multiplayer_lobby_manager.leave_lobby()
