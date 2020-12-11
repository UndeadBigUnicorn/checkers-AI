from client import Client
import logging
import string
from game import *
import time

client = Client()


def wait_for_opponent(player):
    my_move = False
    while not my_move:
        my_move = client.game_info()['whose_turn'] == player
        time.sleep(.05)


turns = {
    "RED": 1,
    "BLACK": 2
}

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logging.info(f'Started client for a team {name}')

    logging.debug('Connection to a server...')
    color = client.connect(name)
    logging.debug(f'Connected to a server and got assigned color: {color}')

    # first move
    if color == "RED":
        move = next_move()
        client.move(move)

    while True:
        wait_for_opponent(color)
        game_info = client.game_info()
        # opponent's move
        if game.whose_turn() != turns[game_info['whose_turn']]:
            for move in game_info["last_move"]['last_moves']:
                game.move(move)
        else:
            if game.moves[-1] != game_info["last_move"]:
                for move in game_info["last_move"]['last_moves']:
                    game.move(move)

        move = next_move()
        client.move(move)

    # moves = [9, 13] if color == "RED" else [24, 20]  # make a move 9 -> 13 or 24 -> 20
    # logging.debug(f'Making a move {moves}')
    # client.move(moves)
    # logging.debug(f'Made a move')
    #
    # logging.debug(f'Getting game info...')
    # info = client.game_info()
    # logging.debug(f'Got game info {info}')
    #
    # moves = [10, 14] if color == "RED" else [21, 17]  # make a move 10 -> 14 or 21 -> 17
    # logging.debug(f'Making a move {moves}')
    # client.move(moves)
    # logging.debug(f'Made a move')
