from const import CARDS_IN_HAND, SUITS, RANKS, NUM_OF_PLAYERS
from card import Card
from player import Player
from random import shuffle

STARTER_CARD = Card('C', 4)


class Game():
    def __init__(self, players):
        self.players = players
        self.hands = {}
        self.team = [self.players[::2], self.players[1::2]]
        self.round = 0
        # Prese
        self.blue_cards = []
        self.red_cards = []
        # Punteggi totali
        self.blue_team_points = 0
        self.red_team_points = 0
        # Briscola
        self.trump = ""
        self.setup_game()

    # Inizializza il mazzo di carte
    def setup_game(self):
        deck = list(Card(suit, rank) for suit in SUITS for rank in RANKS)
        shuffle(deck)
        # Dividiamo la mano in 4
        distributed_hands = [deck[i:i + CARDS_IN_HAND]
                             for i in range(0, len(deck), CARDS_IN_HAND)]
        # Assegnamento delle mani
        for x in range(NUM_OF_PLAYERS):
            self.hands[self.players[x]] = distributed_hands[x]
    # Funzione che cerca chi ha il 4 di denara

    # Ritorna il nome della persona che deve iniziare il gioco
    def look_for_starting_player(self):
        for key in self.hands:
            if STARTER_CARD in self.hands[key]:
                return key

    def __str__(self):
        return "({})".format(self.hands)

    def __repr__(self):
        return str(self)
