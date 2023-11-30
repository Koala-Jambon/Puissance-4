import pyxel
import time
import itertools as tool
import api
import json

import socket
from InquirerPy import inquirer

size = 1.5

class App:
    
    def __init__(self, player_ip_list, player_ip, board, player_turn_ip):
        self.game = api.Game(player_ip_list, board, player_turn_ip)
        self.player_number = self.game.ip_to_number(player_ip)
        self.choice_position = 0
        pyxel.init(int(1920/size), int(1080/size), title = f"{player_ip}")
        self.draw()
        pyxel.run(self.update, self.draw)

    # Check if the player has played/received a moove
    def update(self):
        if (self.game.player_turn_number == self.player_number):
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.choice_position in [0, 1, 2, 3, 4, 5, 6]:
                self.choice_position += 1
                #Envoie (self.choice_position-1) au serveur
            elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2, 3, 4, 5, 6, 7]:
                self.choice_position += -1
                #Envoie (self.choice_position-1) au serveur
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and self.game.check_column(self.choice_position - 1) == True:
                self.game.drop_piece(self.choice_position - 1)
                #Envoie (self.choice_position-1) au serveur et récupère toute les infos du serv
                client.send(f"/play {self.choice_position-1}".encode("utf-8"))
                # On attend la réponse du serveur
                data = client.recv(4096).decode("utf-8")
                data = json.loads(data)
                print(f'{data} quand on joue')
                self.game.board = data["board"]
                if "/wait" in data["message"]:
                    print('/wait')
                    self.wait = True
                else:
                    self.game.change_player_turn()
                if "/endgame" in data["message"]:
                    print('/endgame')
                    if self.game.check_tie == True:
                        print("Draw")
                    else:
                        for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
                            if getattr(self.game, func)():
                                print(f'{self.game.number_to_ip(getattr(self.game, func)())} a gagné !')
                                pyxel.quit()
                                exit()
                self.choice_position = 0
        else:
            # On attend que l'autre joueur joue
            print("J'attends le coup de l'autre joueur")
            client.send(f"/wait {json.dumps({'board': self.game.board})}".encode("utf-8"))
            data = client.recv(4096).decode("utf-8")
            data = json.loads(data)
            print(f'{data} quand on attends')
            # On update le board
            self.game.board = data["board"]
            if "/endgame" in data["message"]:
                print("/endgame")
                if self.game.check_tie == True:
                    print("Draw")
                else:
                    for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
                        if getattr(self.game, func)():
                            print(f'{self.game.number_to_ip(getattr(self.game, func)())} a gagné !')
            self.game.change_player_turn()

    # Draws the board
    def draw(self):
        pyxel.cls(0)
        for draw_x, draw_y in tool.product(range(7), range(6)):
            pyxel.rect((150 * draw_x + 435)/size, (930 - 150 * draw_y)/size, 150/size, 150/size, 1)
            if self.game.board[draw_y][draw_x] == 0:
                pyxel.circ((150 * draw_x + 510)/size, (1005 - 150 * draw_y)/size, 70/size, 0)
            if self.game.board[draw_y][draw_x] == 1:
                pyxel.circ((150 * draw_x + 510)/size, (1005 - 150 * draw_y)/size, 70/size, 8)
            if self.game.board[draw_y][draw_x] == 2:
                pyxel.circ((150 * draw_x + 510)/size, (1005 - 150 * draw_y)/size, 70/size, 10)
            if self.game.player_turn_number == 1:
                pyxel.circ((150 * (self.choice_position - 1) + 510)/size, 75/size, 70/size, 8)
            else:
                pyxel.circ((150 * (self.choice_position - 1) + 510)/size, 75/size, 70/size, 10)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connexion au serveur...")
client.connect(("172.16.122.1", 62222))

print("Connexion au lobby...")
pseudo = inquirer.text("Quel est votre pseudo : ").execute()
client.send(f"/lobby {pseudo}".encode("utf-8"))
data = client.recv(4096).decode("utf-8")

print(data)
if data == f"{pseudo} is connected to the lobby":
    print("Connexion établie !")

client.send(f"/party".encode("utf-8"))
data = client.recv(4096).decode("utf-8")

print(data)

client.send(f"/wait".encode("utf-8"))
data = client.recv(4096).decode("utf-8")
print(data)
data = json.loads(data)

App(data["joueurs"],# Ip List
    data["you"],# Ip of the computer which is running this code
    data["board"],# Current state of the board(normally it's blank)
    data["tour"])# Ip of the player who has to play
