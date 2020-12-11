from client import Client
import logging
import string
from game import *
import time

client = Client()


def wait_for_opponent(player):
    while (not client.game_info()['whose_turn'] == player) and (client.game_info()['winner'] is None):
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

    game_info = client.game_info()
    while game_info["winner"] is None:
        wait_for_opponent(color)
        game_info = client.game_info()

        # double check if game is won
        if game_info["winner"] is None:
            # opponent's move
            if game.whose_turn() != turns[game_info['whose_turn']]:
                for move in game_info["last_move"]['last_moves']:
                    game.move(move)

            move = next_move()
            client.move(move)
