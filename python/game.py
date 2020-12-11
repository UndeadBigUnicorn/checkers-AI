from checkers.game import Game
import random

game = Game()


def next_move():
    possible_moves = game.get_possible_moves()
    move = random.choice(possible_moves)
    game.move(move)
    return move
