from const import CARDS_IN_HAND, SUITS, RANKS, NUM_OF_PLAYERS, POINT_LIMIT, RankValues, NUM_OF_ROUNDS, NUM_OF_TURNS
from card import Card
from player import Player
from random import shuffle, choice
from operator import attrgetter
from math import floor

STARTER_CARD = Card('C', 4)

# Game --> Dura finchè non si arriva a 41 ( POINT_LIMIT )
# Round --> Dura finchè non si esauriscono le carte (10 turni)
# Turno --> Ogni giocatore gioca una carta (1 turno a giocatore )


class Game():
    def __init__(self, players):
        self.players = players
        print("Giocatori: ", self.players)
        self.hands = {}
        self.team = {'blue': self.players[::2], 'red': self.players[1::2]}
        # GIOCO
        self.blue_total_points = 0
        self.red_total_points = 0
        self.first_game = True
        # ROUND
        # Numero di round
        self.round = 0
        # Briscola
        self.trump = ""
        # Indice del giocatore che ha deciso la briscola
        self.deciding_player_index = 0
        # Struttura dati che raccoglie le carte giocate in un round
        self.round_cards = {}
        # Prese del round
        self.blue_cards = []
        self.red_cards = []
        # Punteggi totali
        self.blue_round_points = 0
        self.red_round_points = 0
        # TURNO
        # Giocatore corrente
        self.current_player = ""
        # Numero carte giocate nel turno
        self.turn_index = 0
        # Indice del giocatore del turno
        self.player_turn_index = 0
        # Carte giocate nel turno
        self.turn_cards = {name: "" for name in players}
        # Briscola che comanda il turno
        self.turn_trump = ""

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
        self.turn_index = self.turn_index + 1

    # Round successivo
    def next_round(self):
        # Incremento l'indice
        self.round = self.round + 1
        # Reset briscola del round
        self.turn_trump = ""
        # Azzero l'indice di turno
        self.turn_index = 0
        # Carte giocate nel round
        played_cards = list(v for (k, v) in self.round_cards.items())
        # Vincitore del round
        winner_player_index = self.set_round_winner(played_cards)
        self.player_turn_index = winner_player_index
        # print("Winner is {}".format(self.players[winner_player_index]))
        # Aggiunto punti alla squadra blu ( divisibile per 2 ) o rossa
        if winner_player_index % 2 == 0:
            for (_, v) in self.round_cards.items():
                self.blue_cards.append(v)
            if self.round == 10:
                self.blue_round_points = self.blue_round_points + 3
        else:
            for (_, v) in self.round_cards.items():
                self.red_cards.append(v)
            if self.round == 10:
                self.red_round_points = self.red_round_points + 3

    # Setter briscola del turno
    def set_turn_trump(self, card):
        self.turn_trump = card.suit

    # Cerco le carte che si posso giocare dato un seme che comanda
    def check_available_cards(self, cards):
        filtered_cards = list(filter(self.filter_cards_by_trump, cards))
        if len(filtered_cards) == 0:
            return cards
        return filtered_cards

    # Per la lista delle carte possibili da giocare
    def filter_cards_by_trump(self, card):
        if self.turn_trump != "":
            return card.check_trump(self.turn_trump)
        return True

    # Per la lista delle carte possibili da giocare
    def filter_cards_by_round_trump(self, card):
        return card.check_trump(self.trump)

    # Ottiene la carta più alta basandosi sul valore di presa
    def highest_card(self, cards):
        return max(cards, key=lambda card: RANKS.index(card.rank))

    # Stabilisco chi ha vinto il round e setto il giocatore successivo
    def set_round_winner(self, played_cards):
        # Lista filtrata se c'è almeno una briscola
        filtered_by_trump = list(
            filter(self.filter_cards_by_round_trump, played_cards))

        if len(filtered_by_trump) == 0:  # Non è stata giocata nessuna carta di briscola
            # Filtro per seme che comanda il round
            filtered_by_round_trump = self.check_available_cards(played_cards)
            # Prendo la carta che ha valore più alto
            winner_card = self.highest_card(filtered_by_round_trump)
            # print("Carte senza briscola", filtered_by_round_trump)
        else:
            # Prendo la carta che ha valore più alto
            self.highest_card(filtered_by_trump)
            winner_card = self.highest_card(filtered_by_trump)
            # print("Carte con briscola {}", filtered_by_trump)

        # print("Winner card {}".format(winner_card))
        # Restituisco l'indice del vincitore
        for key, value in self.round_cards.items():
            if value == winner_card:
                return key

    # Calcolo i punteggi per squadra
    def calculate_team_points(self):
        for card in self.blue_cards:
            if str(card.rank) in RankValues:
                self.blue_round_points = self.blue_round_points + \
                    RankValues[str(card.rank)]
        for card in self.red_cards:
            if str(card.rank) in RankValues:
                self.red_round_points = self.red_round_points + \
                    RankValues[str(card.rank)]
        self.blue_round_points = floor(self.blue_round_points / 3)
        self.red_round_points = floor(self.red_round_points / 3)

    # Resetto i valori della partita
    def reset_game(self):
        self.round = 0
        self.blue_round_points = 0
        self.red_round_points = 0
        self.blue_cards = []
        self.red_cards = []
    # Tiene tutta la logica del gioco

    def start_game(self):
        # Ciclo finchè una delle due squadre non raggiungere o supera il punteggio di vittoria
        while (self.blue_total_points <= POINT_LIMIT and self.red_total_points <= POINT_LIMIT):
            # Distribuisco le carte
            self.setup_game()
            # All'inizio del gioco il giocatore che inizia è quello con il 4 di denara (solo se è la prima partita)
            if self.first_game == True:
                self.deciding_player_index, self.current_player = self.look_for_starting_player()
            # Setto il giocatore che inizia il turno
            self.player_turn_index = self.deciding_player_index

            # TODO: Azione per l'immissione della briscola
            self.trump = choice(SUITS)  # TODO: da rimuovere

            # Primo giocatore sceglie la briscola
            print("{} sceglie la briscola: {}".format(
                self.current_player, self.trump))

            while (self.round < NUM_OF_ROUNDS):
                # print("Numero round: ", self.round)
                self.current_player = self.players[self.player_turn_index]
                # Se è il primo giocatore del turno e non è il primo round posso parlare

                while (self.turn_index < NUM_OF_TURNS):
                    self.current_player = self.players[self.player_turn_index]
                    # Carte disponibili da giocare
                    available_cards = self.check_available_cards(
                        self.hands[self.current_player])
                    # TODO: Azione della carta a random
                    chosen_card = choice(available_cards)
                    # print("{} deve giocare una di queste carte {} e ha scelto {}".format(
                    #     self.current_player, available_cards, chosen_card))
                    # Se è il primo giocatore quando gioco la carta stabilisco il seme della carta del turno
                    if self.turn_index == 0:
                        self.set_turn_trump(chosen_card)
                    # Salvo lo stato del round
                    self.round_cards[self.player_turn_index] = chosen_card
                    # Rimuovo la carta dalla mano del giocatore
                    self.hands[self.current_player].remove(chosen_card)
                    # Turno successivo
                    self.next_turn()

                self.next_round()
            # Calcolo il punteggio
            self.calculate_team_points()

            print("Punteggio parziale squadra blu: {} Punteggio parziale squadra rossa: {}".format(
                self.blue_round_points, self.red_round_points))

            # Aggiungo i valori calcolati a quelli totali
            self.blue_total_points = self.blue_total_points + self.blue_round_points
            self.red_total_points = self.red_total_points + self.red_round_points

            print("Punteggio totale squadra blu: {} Punteggio totale squadra rossa: {}\n".format(
                self.blue_total_points, self.red_total_points))

            # Dopo aver calcolato il punteggio stabilisco il giocatore successivo che mette la briscola e gioca per primo
            self.deciding_player_index = (
                self.deciding_player_index + 1) % NUM_OF_PLAYERS
            self.reset_game()

        # Esco dal ciclo del punteggio, proclamo il vincitore
