from enum import Enum
# Spade, Bastoni, Denara, Coppe
SUITS = ['S', 'B', 'D', 'C']
# Valori ordinati per forza di presa
RANKS = [4, 5, 6, 7, 'F', 'C', 'R', 'A', 2, 3]


WORDS = ['Busso', 'Striscio', 'Volo', '/']

CARDS_IN_HAND = 10
NUM_OF_PLAYERS = 4

# Constanti di gioco
POINT_LIMIT = 41
NUM_OF_ROUNDS = 10
NUM_OF_TURNS = 4

RankValues = {
    'F': 1,
    'C': 1,
    'R': 1,
    'A': 3,
    '2': 1,
    '3': 1
}
