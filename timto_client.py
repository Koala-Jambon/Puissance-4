import time

import pyxel
import os
import itertools as tool
import json
import socket
from colorama import Fore, Style, Back
import rich
from InquirerPy import inquirer, get_style
import utils

import api

size = 1.5


def welcome():
    print(Fore.RED + """
 ____  __.           .__                      _____  
|    |/ _|_________  |  | _____              /  |  | 
|      < /  _ \__  \ |  | \__  \    ______  /   |  |_
|    |  (  <_> ) __ \|  |__/ __ \_ /_____/ /    ^   /
|____|__ \____(____  /____(____  /         \____   | 
        \/         \/          \/               |__|
""")
    print(Style.RESET_ALL, end="")


def server_connect(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        utils.info_log("Connexion au serveur de la NASA...", 2)
        time.sleep(1)
        client.connect((ip, port))
        utils.successful_log("Vous êtes connecté")
    except OSError:
        utils.error_log("Le serveur a empêché notre ATTAQUE")
        exit_game()
    time.sleep(1)
    return client


def lobby_connection(client):
    utils.info_log("Préparation du PAYLOAD", 1)
    pseudo = inquirer.text("Identifiant de connexion : ", qmark="?>", amark="?>").execute()
    client.send(f"/lobby {pseudo}".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    if data["message"] == "connected":
        utils.successful_log("Vous avez réussi à vous introduire sans être repéré")
        time.sleep(0.7)


def get_player(client):
    utils.info_log("Récupérations des données utilisateurs...", 1)
    client.send("/lobbylist".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    print(Fore.RESET + "<------JOUEURS------>"
                       "|                   |")
    for ip in data:
        print(Fore.BLUE + data[ip]['pseudo'] + Fore.BLACK + " | ", end="")
        if data[ip]["status"] == "ingame":
            print(Fore.RED + data[ip]["status"] + " n°" + data[ip]["partie_id"])
        else:
            print(Fore.GREEN + data[ip]["status"])

    print(Fore.RESET + "<------------------->", end="\n\n")


def get_party(client):
    utils.info_log("Récupérations des parties", 1)
    client.send("/partylist".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    print(Fore.RESET + "<------PARTIES------>"
                       "|                   |")
    for p_id in data:
        print(Fore.BLUE + "| Partie n°" + p_id)
        print(Fore.BLUE + "| Joueurs : " + Fore.BLACK + data[p_id]["joueurs"])
    print(Fore.RESET + "<------------------->")


def question(client):
    action = inquirer.select("Que voulez-vous faire ?", [{"name": "Créer une partie", "value": "/create"},
                                                         {"name": "Rejoindre une partie", "value": "/join"}]).execute()
    if action == "/join":
        party_id = inquirer.number("Quelle partie voulez-vous rejoindre ?").execute()
        action = f"{action} {party_id}"

    print("je veux faire " + action)

    client.send(f"{action}".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")

    print(data)

def exit_game():
    utils.error_log("VOUS ALLEZ QUITTER")
    os.system("shutdown -h now")
    pass

class App:
    def __init__(self, player_ip_list, player_ip, board, player_turn_ip):
        self.game = api.Game(player_ip_list, board, player_turn_ip)
        self.player_number = self.game.ip_to_number(player_ip)
        self.choice_position = 0
        pyxel.init(int(1920 / size), int(1080 / size), title=f"{player_ip}")
        pyxel.run(self.in_game_update, self.draw)

    def update(self):
        self.in_game_update()

    def draw(self):
        pyxel.cls(0)
        self.draw_board()

    def calculate_endgame(self, data: dict):
        if "/endgame" == data["message"]:
            print('Debug : /endgame')
            if self.game.check_tie():
                print("Draw")
            for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
                if getattr(self.game, func)():
                    print(f'{self.game.number_to_ip(getattr(self.game, func)())} a gagné !')
            exit()


    # Checks if the player has played/received a moove
    def in_game_update(self):
        if (self.game.player_turn_number == self.player_number):
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.choice_position in [0, 1, 2, 3, 4, 5, 6]:
                self.choice_position += 1
                # Envoie (self.choice_position-1) au serveur
            elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2, 3, 4, 5, 6, 7]:
                self.choice_position += -1
                # Envoie (self.choice_position-1) au serveur
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and self.game.check_column(
                    self.choice_position - 1) == True:
                self.game.drop_piece(self.choice_position - 1)
                # Envoie (self.choice_position-1) au serveur et récupère toute les infos du serv
                client.send(f"/play {self.choice_position - 1}".encode("utf-8"))
                # On attend la réponse du serveur
                data = client.recv(4096).decode("utf-8")
                data = json.loads(data)
                print(f'{data} quand on joue')
                # Mise à jour du plateau
                self.game.board = data["board"]
                if "/wait" in data["message"]:
                    print('/wait')
                    self.wait = True
                else:
                    self.game.change_player_turn()
                    self.calculate_endgame(data)
                self.choice_position = 0
        else:
            # On attend le coup de l'autre joueur
            client.send(f"/wait {json.dumps({'board': self.game.board})}".encode("utf-8"))
            data = client.recv(4096).decode("utf-8")
            data = json.loads(data)
            print(f"Debug : |On attend le coup de l'autre| {data} ")
            # On update le board
            self.game.board = data["board"]
            # On regarde si la partie doit s'arrêter
            self.calculate_endgame(data)
            # On change le joueur qui doit jouer
            self.game.change_player_turn()

    # Draws the board
    def draw_board(self):
        for draw_x, draw_y in tool.product(range(7), range(6)):
            pyxel.rect((150 * draw_x + 435) / size, (930 - 150 * draw_y) / size, 150 / size, 150 / size, 1)
            if self.game.board[draw_y][draw_x] == 0:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 0)
            if self.game.board[draw_y][draw_x] == 1:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 8)
            if self.game.board[draw_y][draw_x] == 2:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 10)
        if self.game.player_turn_number == self.player_number:
            pyxel.circ((150 * (self.choice_position - 1) + 510) / size, 75 / size, 70 / size,
                       2 * (self.player_number - 1) + 8)


class EcranFin:
    def __init__(self, winner, board):
        pass

if __name__ == "__main__":
    os.system('clear')
    welcome()
    client = server_connect("127.0.0.1", 62222)
    lobby_connection(client)
    get_player(client)
    get_party(client)
    question(client)

    client.send(f"/wait".encode("utf-8"))
    data = client.recv(4096).decode("utf-8")
    data = json.loads(data)
    print(data)

    App(data["joueurs"],  # Ip List
        data["you"],  # Ip of the computer which is running this code
        data["board"],  # Current state of the board(normally it's blank)
        data["tour"])  # Ip of the player who has to play