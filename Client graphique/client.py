#Version : La meilleure de toute (qsdfqsfdfsqfmathsmathsmathsokdqsjk:mfjklmqsjdklfj)
# Modules to import
import pyxel
import os
import itertools as tool
import json
import socket
import rich

# Files to import
from utils import api
from utils.utils import *

# Size of the screen, can be wathever you want ; 1.5 is recommended
size = 1.5

class App:

    def __init__(self): 
        self.delay_to_draw = 0
        self.delay = 0
        self.state = 3 # State of the game ; Determines what the game has to draw/check
        self.party_choice_number = 0 # Number of the party you are trying to join 
        self.nickname = "" # Nickname chosen by the user ; By default empty
        self.button = 1 # The number of the button the user is hovering over
        self.update_list = ["update_main_menu", "update_choose_party", "update_in_game", "update_get_username", "update_waiting_other_player", "update_end_game"]
        self.draw_list = ["draw_main_menu", "draw_choose_party", "draw_in_game", "draw_get_username", "draw_waiting_other_player", "draw_end_game"]
        pyxel.init(int(1920 / size), int(1080 / size), title=f"Koala-4", fps = 30)
        pyxel.run(self.update, self.draw)

    def update(self):
        getattr(self, self.update_list[self.state])()
    
    def draw(self):
        pyxel.cls(0)
        getattr(self, self.draw_list[self.state])()

    # Gets the username that the user chooses and sends it to the server
    def update_get_username(self):
        pyxel_key_letters = [pyxel.KEY_A,pyxel.KEY_B,pyxel.KEY_C,pyxel.KEY_D,pyxel.KEY_E,pyxel.KEY_F,pyxel.KEY_G,pyxel.KEY_H,pyxel.KEY_I,pyxel.KEY_J,pyxel.KEY_K,pyxel.KEY_L,pyxel.KEY_M,
                   pyxel.KEY_N,pyxel.KEY_O,pyxel.KEY_P,pyxel.KEY_Q,pyxel.KEY_R,pyxel.KEY_S,pyxel.KEY_T,pyxel.KEY_U,pyxel.KEY_V,pyxel.KEY_W,pyxel.KEY_X,pyxel.KEY_Y,pyxel.KEY_Z]
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for letter in range(26):
            if pyxel.btnp(pyxel_key_letters[letter]) and pyxel.btn(pyxel.KEY_SHIFT) and len(self.nickname) < 12:
                self.nickname = self.nickname + alphabet[letter].upper()
            elif pyxel.btnp(pyxel_key_letters[letter]) and len(self.nickname) < 12:
                self.nickname = self.nickname + alphabet[letter]

        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            self.nickname = self.nickname[:-1]
        if pyxel.btnp(pyxel.KEY_RETURN):
            client.send(f"/lobby {self.nickname}".encode("utf-8"))
            data = client.recv(4096).decode("utf-8")

            print("Debug :", data)
            if data == f"{self.nickname} is connected to the lobby":
                print("Connexion établie !")

            # We get the list of parties and players
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

    # Draws the username chosen by the user
    def draw_get_username(self):
        self.draw_text("Enter nickname:", ("center", 10))
        self.draw_text(self.nickname, ("center", 440/size))

    # Waits for another player to connect
    def update_waiting_other_player(self):
        print("Debug : Je suis passé par le state 4")
        if self.delay_to_draw == 2:
            data = {"message" : "/waitpeople"}
            while data["message"] == "/waitpeople":
                client.send(f"/waitpeople".encode("utf-8"))
                data = recv_json(client)
                print("Debug :", data)

            self.game__init__(data["joueurs"],  # Ip List
                              data["you"],  # Ip of the computer which is running this code
                              data["board"],  # Current state of the board(normally it's empty)
                              data["tour"])  # Ip of the player who has to play
            self.state = 2
            self.delay_to_draw = 0
        else:
            self.delay_to_draw += 1

    # Draws a text telling the user to wait for another player
    def draw_waiting_other_player(self):
        self.draw_text("Waiting...", ("center", 0))

    # Gets the party the user wants to join and then calls self.party_interactions
    def update_choose_party(self):
        self.delay_to_draw = 0
        if pyxel.btnp(pyxel.KEY_UP) and self.party_choice_number != 0:
            self.party_choice_number += -1
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.party_choice_number != self.party_infos()["number"]-1:
            self.party_choice_number += 1
        elif pyxel.btnp(pyxel.KEY_RETURN) and self.party_choice_number+1 in self.party_infos()["free"]:
            print("Debug : La partie est free & tu a appuyé sur entré")
            action = f"/join {self.party_choice_number+1}"
            self.party_interactions(action)
        elif pyxel.btnp(pyxel.KEY_RETURN):
            print("Debug : La partie est full :", self.party_choice_number)
    
    # Draws the menu of selection of a party
    def draw_choose_party(self):
        buttons_coords = {
                          "x" : (500/size, 500/size, 500/size),
                          "y" : (50/size, 400/size, 750/size),
                          "w" : (int(920/size), int(920/size), int(920/size)),
                          "h" : (int(250/size), int(250/size), int(250/size))
                         }
        for draw_button in range(len(buttons_coords["x"])):
            button_constant = (draw_button+(self.party_choice_number//3)*3)+1
            if button_constant in self.party_infos()["empty"]:
                self.draw_text(f"{button_constant}-Empty", (int(510/size), int(buttons_coords["y"][draw_button]+50/size)))
            elif button_constant in self.party_infos()["free"]:
                try:    
                    self.draw_text(f"{button_constant}-{self.party_infos()['players_list'][button_constant-1]}", (int(510/size), int(buttons_coords["y"][draw_button]+50/size)))
                except:
                    self.draw_text(f"{button_constant}-Error", (int(510/size), int(buttons_coords["y"][draw_button]+50/size)))
            elif button_constant <= self.party_infos()["number"]:
                self.draw_text(f"{button_constant}-Full", (int(510/size), int(buttons_coords["y"][draw_button]+50/size)))
            if draw_button == self.party_choice_number%3:
                for draw_w, draw_h in tool.product(range(buttons_coords["w"][draw_button]), range(buttons_coords["h"][draw_button])):
                    if pyxel.pget(buttons_coords["x"][draw_button]+draw_w, buttons_coords["y"][draw_button]+draw_h) == 0:
                        pyxel.pset(buttons_coords["x"][draw_button]+draw_w, buttons_coords["y"][draw_button]+draw_h, 5)

    # Sends to the server what the user wants to do (Create/Join) a party
    def party_interactions(self, action : str):
        print("Debug : Je veux faire " + action)
        client.send(f"{action}".encode("utf-8"))
        data = client.recv(4096).decode("utf-8")

        print("Debug :", data)
        self.state = 4
        self.delay_to_draw = 0

    # Watches the interactions beetween the user and the buttons of the main menu
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

    # Draws the main menu
    def draw_main_menu(self):
        self.draw_text("Join", (750/size, int(450/size)))
        self.draw_text("Create", (600/size, int(800/size)))

        buttons_coords = {
                          "x" : (20/size, 500/size, 500/size),
                          "y" : (20/size, 400/size, 750/size),
                          "w" : (int(100/size), int(920/size), int(920/size)),
                          "h" : (int(100/size), int(250/size), int(250/size))
                         }
        for draw_button in range(len(buttons_coords["x"])):
            if draw_button == self.button:
                for draw_w, draw_h in tool.product(range(buttons_coords["w"][draw_button]), range(buttons_coords["h"][draw_button])):
                    if pyxel.pget(buttons_coords["x"][draw_button]+draw_w, buttons_coords["y"][draw_button]+draw_h) == 0:
                        pyxel.pset(buttons_coords["x"][draw_button]+draw_w, buttons_coords["y"][draw_button]+draw_h, 5)
            else:
                for draw_w, draw_h in tool.product(range(buttons_coords["w"][draw_button]), range(buttons_coords["h"][draw_button])):
                    if pyxel.pget(buttons_coords["x"][draw_button]+draw_w, buttons_coords["y"][draw_button]+draw_h) == 0:
                        pyxel.pset(buttons_coords["x"][draw_button]+draw_w, buttons_coords["y"][draw_button]+draw_h, 2)


    # Checks if the player has played/received a moove
    def update_in_game(self):
        if self.delay_to_draw == 2:
            if (self.game.player_turn_number == self.player_number):
                if pyxel.btnp(pyxel.KEY_RIGHT) and self.choice_position in [0, 1, 2, 3, 4, 5, 6]:
                    self.choice_position += 1
                    send_json(client=client, data_dict={"message": "/position", "position" : self.choice_position-1})
                elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2, 3, 4, 5, 6, 7]:
                    self.choice_position += -1
                    send_json(client=client, data_dict={"message": "/position", "position" : self.choice_position-1})
                elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and self.game.check_column(
                        self.choice_position - 1) == True:
                    self.game.drop_piece(self.choice_position - 1)
                    send_json(client, {"message": "/play", "coup": self.choice_position -1})
                    # Waiting for the answer of the server
                    data = client.recv(4096).decode("utf-8")
                    data = json.loads(data)
                    print(f'{data} quand on joue')
                    # Updates the board
                    self.game.board = data["board"]
                    if "/waitgame" in data["message"]:
                        print('Debug : /waitgame')
                    else:
                        self.game.change_player_turn()
                        self.calculate_endgame(data)
                    self.choice_position = 0
            else:
                # On attend le coup de l'autre joueur
                send_json(client=client, data_dict={"message": "/waitgame", "board": self.game.board})
                print("j'ai envoyé le message")
                data = client.recv(4096).decode("utf-8")
                data = json.loads(data)
                print(f"Debug : |On attend le coup de l'autre| {data} ")
                if "/waitgame" == data["message"]:
                    self.choice_position = data["position"]+1
                else:
                    self.choice_position = 0
                    # Updates the board
                    self.game.board = data["board"]
                    # Checks the game has ended ; If yes then tells the user why
                    self.calculate_endgame(data)
                    # Changes the player who has to play
                    self.game.change_player_turn()
        else:
            self.delay_to_draw += 1

    # Draws the board in game
    def draw_in_game(self):
        pyxel.cls(0)
        for draw_x, draw_y in tool.product(range(7), range(6)):
            pyxel.rect((150 * draw_x + 435) / size, (930 - 150 * draw_y) / size, 150 / size, 150 / size, 1)
            if self.game.board[draw_y][draw_x] == 0:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 0)
            if self.game.board[draw_y][draw_x] == 1:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 8)
            if self.game.board[draw_y][draw_x] == 2:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 10)
        pyxel.circ((150 * (self.choice_position - 1) + 510) / size, 75 / size, 70 / size, 2 * (self.game.player_turn_number - 1) + 8)

    # Returns a list of all the parties with less than 2 players in them
    def party_infos(self):
        client.send(b"/partylist")
        data = client.recv(4096).decode("utf-8")
        data = json.loads(data)
        #print("Debug :", data)
        free_party_list = []
        empty_party_list = []
        for game_id in range(len(data)):
            if len(data[str(game_id+1)]["joueurs"]) == 0:
                empty_party_list.append(game_id+1)
                free_party_list.append(game_id+1)
            elif len(data[str(game_id+1)]["joueurs"]) == 1:
                free_party_list.append(game_id+1)

        party_number = len(data)
        client.send(b"/lobbylist")
        data = client.recv(4096).decode("utf-8")
        data = json.loads(data)
        players_alone_list = ["" for loop in range(len(data))]
        for ip in data:
            try:
                players_alone_list[int(data[ip]["partie_id"])-1] = str(data[ip]["pseudo"])
            except:
                pass
        party_infos = {
                        "empty" : empty_party_list,
                        "free" : free_party_list,
                        "number" : party_number,
                        "players_list" : players_alone_list
                      }
        
        return party_infos
    
    # Starts the game with the expected values
    def game__init__(self, player_ip_list : list, player_ip, board : list, player_turn_ip):
        self.game = api.Game(player_ip_list, board, player_turn_ip)
        self.player_number = self.game.ip_to_number(player_ip)
        self.choice_position = 0

    # Tells to the user the result of the game
    def calculate_endgame(self, data: dict):
        if "/endgame" == data["message"]:
            print('Debug : /endgame')
            if self.game.check_tie():
                print("Draw")
            for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
                if getattr(self.game, func)():
                    print(f'{self.game.number_to_ip(getattr(self.game, func)())} a gagné !')
                    print(self.game.victory_reason)
                    self.delay_to_draw = 0
                    self.state = 5

    def update_end_game(self):
        if self.delay != 120:
            self.delay += 1
        else:
            self.delay_to_draw = 0
            self.delay = 0
            self.state = 0 # State of the game ; Determines what the game has to draw/check
            self.party_choice_number = 0 # Number of the party you are trying to join 
            self.button = 1 # The number of the button the user is hovering over

    def draw_end_game(self):
        for draw_x, draw_y in tool.product(range(7), range(6)):
            pyxel.rect((150 * draw_x + 435) / size, (930 - 150 * draw_y) / size, 150 / size, 150 / size, 1)
            if self.game.board[draw_y][draw_x] == 0:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 0)
            if self.game.board[draw_y][draw_x] == 1:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 8)
            if self.game.board[draw_y][draw_x] == 2:
                pyxel.circ((150 * draw_x + 510) / size, (1005 - 150 * draw_y) / size, 70 / size, 10)
        for draw_coords in self.game.victory_reason:
            pyxel.circ((150 * draw_coords[0] + 510) / size, (1005 - 150 * draw_coords[1]) / size, 60 / size, 11)

    def draw_text(self, text : str, coords : tuple):
        coords = list(coords)
        text = text.lower()
        letters_coords = {
            "exemple" : ('file','image','width','height','from-x','from-y'),
            "a" : ("letter1", 0, 85, 99, 0, 0),
            "b" : ("letter1", 0, 72, 100, 85, 0),
            "c" : ("letter1", 0, 77, 100, 157, 0),
            "d" : ("letter1", 0, 82, 101, 0, 100),
            "e" : ("letter1", 0, 62, 99, 82, 102),
            "f" : ("letter1", 0, 62, 98, 144, 102),
            "g" : ("letter1", 1, 82, 101, 0, 0),
            "h" : ("letter1", 1, 76, 99, 82, 0),
            "i" : ("letter1", 1, 13, 99, 158, 0),
            "j" : ("letter1", 1, 43, 100, 171, 0),
            "k" : ("letter1", 1, 70, 99, 0, 101),
            "l" : ("letter1", 1, 61, 98, 70, 101),
            "m" : ("letter1", 1, 100, 99, 131, 100),
            "n" : ("letter1", 2, 77, 99, 0, 0),
            "o" : ("letter1", 2, 92, 101, 77, 0),
            "p" : ("letter1", 2, 69, 100, 169, 0),
            "q" : ("letter1", 2, 97, 124, 0, 99),
            "r" : ("letter1", 2, 74, 100, 98, 101),
            "s" : ("letter1", 2, 67, 101, 172, 101),
            "t" : ("letter2", 0, 76, 98, 0, 0),
            "u" : ("letter2", 0, 76, 100, 76, 0),
            "v" : ("letter2", 0, 83, 99, 152, 0),
            "w" : ("letter2", 0, 115, 98, 0, 108),
            "x" : ("letter2", 0, 79, 99, 115, 108),
            "y" : ("letter2", 1, 80, 99, 0, 0),
            "z" : ("letter2", 1, 73, 97, 80, 0),
            "1" : ("letter2", 1, 39, 98, 153, 0),
            "2" : ("letter2", 1, 65, 99, 192, 0),
            "3" : ("letter2", 1, 67, 101, 0, 99),
            "4" : ("letter2", 1, 79, 100, 67, 99),
            "5" : ("letter2", 1, 67, 101, 146, 99),
            "6" : ("letter2", 2, 71, 100, 0, 0),
            "7" : ("letter2", 2, 66, 98, 71, 0),
            "8" : ("letter2", 2, 73, 100, 137, 0),
            "9" : ("letter2", 2, 72, 101, 0, 102),
            "0" : ("letter2", 2, 76, 101, 72, 102),
            "-" : ("letter2", 2, 45, 63, 148, 102),
            "." : ("letter2", 2, 17, 84, 193, 102)
        }
        if coords[0] == "center":
            save_coords = 0
            for letter in text:
                try:
                    save_coords += letters_coords[letter][2] + 8
                except KeyError:
                    if letter == " ":
                        save_coords += 32
            coords[0] = (1920/size-save_coords)/2
        for letter in text:
            try:
                pyxel.load(f"{letters_coords[letter][0]}.pyxres")
                pyxel.blt(coords[0], coords[1], letters_coords[letter][1], letters_coords[letter][4], letters_coords[letter][5], letters_coords[letter][2], letters_coords[letter][3])
                coords[0] += letters_coords[letter][2] + 8
            except KeyError:
                if letter == " ":
                    coords[0] += 32      
            
# Connects to the lobby and then starts the game
if __name__ == "__main__":
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("Debug : Connexion au serveur...")
    try:
        client.connect(("172.16.122.1", 62222))
    except OSError:
        print("Cannot connect to the server ; Try updating ; Try later")
        exit()
    
    #print("Debug : Connexion au lobby...")

    App()
