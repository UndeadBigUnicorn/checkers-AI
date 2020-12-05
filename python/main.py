from client import Client
import logging
import random
import string

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = Client()

    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logging.info(f'Started client for a team {name}')

    logging.debug('Connection to a server...')
    color = client.connect(name)
    logging.debug(f'Connected to a server and got assigned color: {color}')

    moves = [9, 13] if color == "RED" else [24, 20]  # make a move 9 -> 13 or 24 -> 20
    logging.debug(f'Making a move {moves}')
    client.move(moves)
    logging.debug(f'Made a move')

    logging.debug(f'Getting game info...')
    info = client.game_info()
    logging.debug(f'Got game info {info}')

    moves = [10, 14] if color == "RED" else [21, 17]  # make a move 10 -> 14 or 21 -> 17
    logging.debug(f'Making a move {moves}')
    client.move(moves)
    logging.debug(f'Made a move')
