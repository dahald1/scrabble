# Scrabble Game

By Colin Butera, Jakob Mathieson, Diwas Dahal, Joseph Cancellieri


## Description
Implementation of the classic scrabble game. Users are able to take turns playing against
an AI. Users can create accounts to save their games in the cloud to continue playing later.

## Usage
Note: Make sure the `ServiceAccount.json` file is located one directory above the project folder.

To get started, you need to run `login.py`. Upon doing so, you will be prompted to log in or sign up. If it's your first time, you can sign up for an account. After signing up or logging in, you will be redirected to the start screen.

Within the start screen, you can choose to play against an AI, load the last game you saved (the button will be grayed out if a save doesn't exist), or choose to play online. At this point in time, the only thing you can do in regards to multiplayer is hosting a lobby and sharing the lobby id with other users for them to join it. There is no logic for starting a multiplayer game.

When playing scrabble, you click and drag the pieces on the tile rack at the bottom of the screen to wherever you want to place it on the game board. To finalize your placements and end your turn, you press enter.