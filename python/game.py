from checkers.game import Game
import random
import copy
import math

game = Game()

toilet = [5, 13, 21, 29, 30, 31, 32, 28, 20, 12, 4, 3, 2, 1]
diagonals = [
    [1, 5],
    [2, 6, 9, 13],
    [3, 7, 10, 14, 17, 21],
    [4, 8, 11, 15, 18, 22, 25, 29],
    [12, 16, 19, 23, 26, 30],
    [20, 24, 27, 31],
    [28, 32],
    [4],
    [3, 8, 12],
    [2, 7, 11, 16, 20],
    [1, 6, 10, 15, 19, 24, 28],
    [5, 9, 14, 18, 23, 27, 32],
    [13, 17, 22, 26, 31],
    [21, 25, 30],
    [29]
]

def on_diagonal(move, enemy_move):
    return len([move[1] in diag and enemy_move[0] in diag and enemy_move[1] in diag for diag in diagonals]) > 0

def is_over(move, enemy_move):
    # logic is simple: moves should be on the same diagonal
    # if enemy move starting point is before our checker and end point is after our checker
    # than our checker was beaten
    return on_diagonal(move, enemy_move) and abs(enemy_move[0] - move[1]) >= 3 and abs(enemy_move[1] - move[1]) <= 6

def enemy_beat(game, move):
    game_copy = copy.deepcopy(game)
    game_copy.move(move)
    for m in game_copy.get_possible_moves():
        if is_over(move, m):
            return True

    return False

def evaluate(game, move):

    score = 0

    # if beat enemy's checker
    if abs(move[0] - move[1]) > 6:
        score += 10

    # if in toilet -> nobody could beat you
    if move[-1] in toilet:
        score += 5

    if score != 0:
        return score

    # if move that was made leads to the fact that your checker would be beat in the next move

    if enemy_beat(game, move):
        return -10

    # nobody won
    return score


def next_move():

    game_copy = copy.deepcopy(game)
    best_move = [0, 0]
    best_score = -math.inf
    for move in game_copy.get_possible_moves():
        score = evaluate(game_copy, move)
        if score > best_score:
            best_score = score
            best_move = move

    game.move(best_move)
    return best_move


if __name__ == '__main__':

    def play_test():
        for i in range(25):
            print(game.get_possible_moves())
            print(next_move())

    play_test()
