import pyxel
import os
import itertools as tool
import json
import socket
import rich

import api

size = 1.5

class App:

    def __init__(self): 
        self.state = 3
        self.party_choice_number = 0
        self.nickname = ""
        self.update_list = ["update_main_menu", "update_choose_party", "update_in_game", "update_get_username"]
        self.draw_list = ["draw_main_menu", "draw_choose_party", "draw_in_game", "draw_get_username"]
        self.button = 1
        pyxel.init(int(1920 / size), int(1080 / size), title=f"Power 4")

        pyxel.run(self.update, self.draw)

    def game_init(self, player_ip_list, player_ip, board, player_turn_ip):
        self.game = api.Game(player_ip_list, board, player_turn_ip)
        self.player_number = self.game.ip_to_number(player_ip)
        self.choice_position = 0

    def calculate_endgame(self, data: dict):
        if "/endgame" == data["message"]:
            print('Debug : /endgame')
            if self.game.check_tie():
                print("Draw")
            for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
                if getattr(self.game, func)():
                    print(f'{self.game.number_to_ip(getattr(self.game, func)())} a gagné !')
            exit()

    def update(self):
        getattr(self, self.update_list[self.state])()
    
    def draw(self):
        pyxel.cls(0)
        getattr(self, self.draw_list[self.state])()

    def update_get_username(self):
        pyxel_key_letters = [pyxel.KEY_A,pyxel.KEY_B,pyxel.KEY_C,pyxel.KEY_D,pyxel.KEY_E,pyxel.KEY_F,pyxel.KEY_G,pyxel.KEY_H,pyxel.KEY_I,pyxel.KEY_J,pyxel.KEY_K,pyxel.KEY_L,pyxel.KEY_M,
                   pyxel.KEY_N,pyxel.KEY_O,pyxel.KEY_P,pyxel.KEY_Q,pyxel.KEY_R,pyxel.KEY_S,pyxel.KEY_T,pyxel.KEY_U,pyxel.KEY_V,pyxel.KEY_W,pyxel.KEY_X,pyxel.KEY_Y,pyxel.KEY_Z]
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for letter in range(len(pyxel_key_letters)):
            if pyxel.btnp(pyxel_key_letters[letter]) and pyxel.btn(pyxel.KEY_SHIFT):
                self.nickname = self.nickname + alphabet[letter].upper()
            elif pyxel.btnp(pyxel_key_letters[letter]):
                self.nickname = self.nickname + alphabet[letter]
        os.system("cls")
        print(self.nickname)
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.nickname = self.nickname[:-1]
        if pyxel.btnp(pyxel.KEY_RETURN):
            client.send(f"/lobby {self.nickname}".encode("utf-8"))
            data = client.recv(4096).decode("utf-8")

            print(data)
            if data == f"{self.nickname} is connected to the lobby":
                print("Connexion établie !")

            # On récupère la liste des parties et des joueurs
            client.send(b"/lobbylist")
            data = client.recv(4096).decode("utf-8")
            print("Liste des joueurs :")
            rich.print_json(data)
            print("-------------------")

            client.send(b"/partylist")
            data = client.recv(4096).decode("utf-8")
            print("Liste des parties :")
            rich.print_json(data)
            print("-------------------")
        
            self.state = 0

    def draw_get_username(self):
        pass

    def update_choose_party(self):
        free_party_list = self.check_free_parties()
        if pyxel.btnp(pyxel.KEY_UP):
            self.party_choice_number += 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.party_choice_number += -1
        elif pyxel.btnp(pyxel.KEY_RETURN) and self.party_choice_number in free_party_list:
            action = f"/join {self.party_choice_number}"
            self.party_interactions(action)
            self.state = 2
    
    def draw_choose_party(self):
        pass

    def party_interactions(self, action):
        print("je veux faire " + action)
        client.send(f"{action}".encode("utf-8"))
        data = client.recv(4096).decode("utf-8")

        print(data)

        client.send(f"/wait".encode("utf-8"))
        data = client.recv(4096).decode("utf-8")
        print(data)
        data = json.loads(data)
        print(action)

        self.game_init(data["joueurs"],  # Ip List
                        data["you"],  # Ip of the computer which is running this code
                        data["board"],  # Current state of the board(normally it's blank)
                        data["tour"])  # Ip of the player who has to play
        self.state = 2

    def update_main_menu(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.button in [1, 2]:
            self.button += -1
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.button in [0, 1]:
            self.button += 1
        elif pyxel.btnp(pyxel.KEY_RETURN):
            if self.button == 0:
                pyxel.quit()
            elif self.button == 1:
                self.state = 1
            elif self.button == 2:
                action = "/create"
                self.party_interactions(action)


    def draw_main_menu(self):
        buttons_coords = {
                          "x" : [20/size, 500/size, 500/size],
                          "y" : [20/size, 400/size, 750/size],
                          "w" : [100/size, 920/size, 920/size],
                          "h" : [100/size, 250/size, 250/size]
                         }
        for draw_button in range(len(buttons_coords["x"])):
            if draw_button == self.button:
                pyxel.rect(buttons_coords["x"][draw_button], buttons_coords["y"][draw_button], buttons_coords["w"][draw_button], buttons_coords["h"][draw_button], 1)
            else:
                pyxel.rect(buttons_coords["x"][draw_button], buttons_coords["y"][draw_button], buttons_coords["w"][draw_button], buttons_coords["h"][draw_button], 2)

    def check_free_parties(self):
        client.send(b"/partylist")
        data = client.recv(4096).decode("utf-8")
        data = json.loads(data)
        free_party_list = []
        for game_id in range(len(data)):
            if len(data[str(game_id+1)]["joueurs"]) < 2:
                free_party_list.append(game_id)
        return free_party_list
                

    def update_choose_game(self):
        if pyxel.btnp(pyxel.KEY_UP) and self.button in range():
            self.selected_game += 1
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.button in [0, 1]:
            self.selected_game += -1

    # Checks if the player has played/received a moove
    def update_in_game(self):
        if (self.game.player_turn_number == self.player_number):
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.choice_position in [0, 1, 2, 3, 4, 5, 6]:
                self.choice_position += 1
            elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2, 3, 4, 5, 6, 7]:
                self.choice_position += -1
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and self.game.check_column(
                    self.choice_position - 1) == True:
                self.game.drop_piece(self.choice_position - 1)
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

    # Draws the board in game
    def draw_in_game(self):
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

if __name__ == "__main__":
    os.system('cls')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connexion au serveur...")
    client.connect(("192.168.1.16", 62222))
    
    print("Connexion au lobby...")

    App()
