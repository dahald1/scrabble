"""Auth file used to get reference to Firestore database"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def auth():
    """returns reference to database"""
    # NOTE: do not push the scrabble_SDK.json to the GitHub repository!
    # Leave it one directory above the project folder!
    cred = credentials.Certificate('../serviceAccount.json')
    _ = firebase_admin.initialize_app(cred)
    database = firestore.client()
    return database


if __name__ == "__main__":
    auth()
