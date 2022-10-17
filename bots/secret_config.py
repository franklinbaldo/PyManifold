API_KEY = None  # Add API key here, None for dry run

BOT_IDS = []  # IDs of known bots (including this one)
CONFIRM_BETS = False  # Ask the user to confirm each set of bets (human-in-the-loop)
RUN_ONCE = True  # Whether to run once or in a loop
SLEEP_TIME = 30  # How long to sleep between loop iterations
MAX_BACKOFF = 4  # Maximum number of loop iterations between retries

GROUPS = {
    # Try to make P(A) = P(B)
    "Brazilian Elections": {
        #                                                    Not required
        #                                                    |  Required
        #                                                    |  |
        "will-lula-da-silva-win-the-2022-bra": [0, 1],
        "will-lula-da-silva-win-the-2022-pre": [0, 1],
        "lula-vai-ser-eleito-presidente-do-b": [0, 1],
        #"will-jair-bolsonaro-be-reelected-pr": [1, 0],
    },
"Inverse Br election":{"lula-vai-ser-eleito-presidente-do-b": [0, 1],
        "will-jair-bolsonaro-be-reelected-pr": [1, 0],
    },
}
