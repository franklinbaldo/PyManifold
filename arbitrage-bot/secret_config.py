API_KEY = None                              # Add API key here, None for dry run
USER_ID = "EBGhoFSxRtVBu4617SLZUe1FeJt1"    # Bot's user ID
BOT_IDS = [USER_ID]                         # IDs of known bots (including this one)
CONFIRM_BETS = False                        # Ask the user to confirm each set of bets (human-in-the-loop)
RUN_ONCE = True                             # Whether to run once or in a loop
SLEEP_TIME = 30                             # How long to sleep between loop iterations
MAX_BACKOFF = 4                             # Maximum number of loop iterations between retries

GROUPS = {
    # Try to make P(A) = P(B)
    'Brazilian Elections': {
        #                                                    Not required
        #                                                    |  Required
        #                                                    |  |
        'will-lula-da-silva-win-the-2022-bra':              [0, 1],
        'will-lula-da-silva-win-the-2022-pre':              [0, 1],
        'lula-vai-ser-eleito-presidente-do-b':              [0, 1],
        'will-jair-bolsonaro-be-reelected-pr':              [1,0],
    },

    # Try to make P(A) + P(B) = 1
    'Putin': {
        #                                      😢 🎉
        'will-putin-be-the-leader-of-russia': [1, 0],
        'will-putin-no-longer-be-the-leader': [0, 1],
    },

    # Try to make P(A) >= P(B)
    'Annexation': {
        #                                       No
        #                                       |  Only occupied
        #                                       |  |  Some unoccupied
        #                                       |  |  |
        'will-russia-annex-any-part-of-ukrai': [0, 1, 1],
        'will-russia-annex-unoccupied-parts':  [0, 0, 1],
    },
}
# There are more groups in `secret_config.py` which I'm not publishing to github :3