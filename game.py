from const import CARDS_IN_HAND, SUITS, RANKS, NUM_OF_PLAYERS, POINT_LIMIT
from card import Card
from player import Player
from random import shuffle

STARTER_CARD = Card('C', 4)

# Game --> Dura finchè non si arriva a 41 ( POINT_LIMIT )
# Round --> Dura finchè non si esauriscono le carte (10 turni)
# Turno --> Ogni giocatore gioca una carta (1 turno a giocatore )


class Game():
    def __init__(self, players):
        self.players = players
        self.hands = {}
        self.team = [self.players[::2], self.players[1::2]]
        # GIOCO
        # Punteggi totali
        self.blue_team_points = 0
        self.red_team_points = 0

        # ROUND
        # Numero di round
        self.round = 0
        # Briscola
        self.trump = ""
        # Indice del giocatore che ha deciso la briscola
        self.deciding_player_index = 0
        # Prese del round
        self.blue_cards = []
        self.red_cards = []

        # TURNO
        # Giocatore corrente
        self.current_player = ""
        # Numero carte giocate nel turno
        self.turn_index = 0
        # Indice del giocatore del turno
        self.player_turn_index = 0
        # Carte giocate nel turno
        self.turn_cards = {name: "" for name in players}

    # Inizializza il gioco
    def setup_game(self):
        deck = list(Card(suit, rank) for suit in SUITS for rank in RANKS)
        shuffle(deck)
        # Dividiamo la mano in 4
        distributed_hands = [deck[i:i + CARDS_IN_HAND]
                             for i in range(0, len(deck), CARDS_IN_HAND)]
        # Assegnamento delle mani
        for x in range(NUM_OF_PLAYERS):
            self.hands[self.players[x]] = distributed_hands[x]

    # Ritorna il nome della persona che deve iniziare il gioco ( cercando il 4 di denara )
    def look_for_starting_player(self):
        for index, (key, value) in enumerate(self.hands.items()):
            if STARTER_CARD in value:
                return index, key

    # Passo al turno successivo
    def next_turn(self):
        self.player_turn_index = (self.player_turn_index + 1) % NUM_OF_PLAYERS
        self.current_player = self.players[self.player_turn_index]

    # Tiene tutta la logica del gioco
    def start_game(self):
        self.deciding_player_index, self.current_player = self.look_for_starting_player()
        # Il giocatore che inizia a mettere la briscola è quello che gioca la prima carte
        self.player_turn_index = self.deciding_player_index

        # Ciclo finchè una delle due squadre non raggiungere o supera il punteggio di vittoria
        # while (self.blue_team_points <= POINT_LIMIT or self.red_team_points <= POINT_LIMIT):
        #     # Reset valori della partita
        #     self.round = 0
        #     # Distribuisco le carte
        #     self.setup_game()
        #     # Primo giocatore sceglie la briscola
        #     print("Giocatore {} immette la briscola", self.current_player)

        #     # Ciclo finché non si finiscono le dieci carte
        # while (self.round < 10):

        while (self.turn_index < 4):
            print("Giocatore {} deve giocare", )
            # Aumento l'indice del giocatore di uno
            self.next_turn()

        # Stabilisco chi ha fatto la presa ( blue o red team)

    def __str__(self):
        return "({})".format(self.hands)

    def __repr__(self):
        return str(self)
