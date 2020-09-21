from game import Game
from player import Player
from const import RankValues


names = ['Bartolomeo', 'Pierugo', 'Ivana', 'Ritardenzio']


def main():
    game = Game([Player(name) for name in names])
    game.start_game()


if __name__ == "__main__":
    main()
