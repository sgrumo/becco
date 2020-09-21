from const import RankValues


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        # self.value = RankValues[self.rank]

    def check_trump(self, trump):
        return self.suit == trump

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __str__(self):
        return "({},{})".format(self.suit, self.rank)

    def __repr__(self):
        return str(self)
