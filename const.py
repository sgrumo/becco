from enum import Enum
# Spade, Bastoni, Denara, Coppe
SUITS = ['S', 'B', 'D', 'C']
RANKS = [2, 3, 4, 5, 6, 7, 'F', 'C', 'R', 'A']


WORDS = ['Busso', 'Striscio', 'Volo', '/']

CARDS_IN_HAND = 10
NUM_OF_PLAYERS = 4


POINT_LIMIT = 41


class RankValues(Enum):
    F = 1 / 3
    C = 1 / 3
    R = 1 / 3
    A = 1
