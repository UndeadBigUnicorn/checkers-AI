import requests

class Client:
    def __init__(self, host="localhost", port="8081"):
        self.host = host
        self.port = port
        self.token = None

    def game_info(self):
        """
        Get current game state
        :return: Game info json as python dict
        """
        return requests.get(f"http://{self.host}:{self.port}/game").json()["data"]

    def connect(self, name):
        """
        Connect to a checker server and start a game
        :param name: team name
        :return: color of the side that was assigned to this client
        """
        r = requests.post(f"http://{self.host}:{self.port}/game?team_name={name}")
        if r.status_code == requests.codes.ok:
            data = r.json()["data"]
            self.token = data["token"]
            return data["color"]
        else:
            raise BaseException(r.text)


    def move(self, moves):
        """
        Make a move on the board
        :param moves: list of moves to make
        Could rise an error if server response is not OK
        """
        r = requests.post(f"http://{self.host}:{self.port}/move",
                          headers={"Authorization": f"Token {self.token}"},
                          json={"move": moves})
        if r.status_code == requests.codes.bad_request:
            raise BaseException(r.text)
