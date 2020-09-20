from game import Game
from player import Player
from const import RankValues


names = ['Bartolomeo', 'Pierugo', 'Ivana', 'Ritardenzio']
team = [names[::2], names[1::2]]


def main():
    game = Game([Player(name) for name in names])
    game.look_for_starting_player()


if __name__ == "__main__":
    main()
