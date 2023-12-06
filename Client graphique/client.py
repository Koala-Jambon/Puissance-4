# Modules to import
import pyxel
import os
import itertools as tool
import json
import socket
import rich

# Files to import
from utils import api

#Size of the screen, can be wathever you want ; 1.5 is recommended
size = 1.5

class App:

    def __init__(self): 
        self.state = 3 # State of the game ; Determines what the game has to draw/check
        self.party_choice_number = 0 # Number of the party you are trying to join 
        self.nickname = "" # Nickname chosen by the user ; By default empty
        self.button = 1 # The number of the button the user is hovering over
        self.delay_to_draw = 0 # Used to make delay so Pyxel can draw before getting stuck in an infinite loop
        self.update_list = ("update_main_menu", "update_choose_party", "update_in_game", "update_get_username", "update_waiting_other_player")
        self.draw_list = ("draw_main_menu", "draw_choose_party", "draw_in_game", "draw_get_username", "draw_waiting_other_player")
        pyxel.init(int(1920 / size), int(1080 / size), title=f"Koala-4")
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
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for letter in range(26):
            if pyxel.btnp(pyxel_key_letters[letter]):
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
            
            '''
            print("Liste des joueurs :")
            rich.print_json(data)
            print("-------------------")

            client.send(b"/partylist")
            data = client.recv(4096).decode("utf-8")
            print("Liste des parties :")
            rich.print_json(data)
            print("-------------------")
            '''
            
            self.state = 0

    # Draws the username chosen by the user
    def draw_get_username(self):
        self.draw_text(self.nickname, (0/size, 440/size))#Coords have to be changed in order to put the text in the center of the screen

    # Waits for another player to connect
    def update_waiting_other_player(self):
        if self.delay_to_draw == 2:
            client.send(f"/wait".encode("utf-8"))
            data = client.recv(4096).decode("utf-8")
            print("Debug :", data)
            data = json.loads(data)
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
        self.draw_text("Waiting...", (0, 0))

    # Gets the party the user wants to join and then calls self.party_interactions
    def update_choose_party(self):
        self.delay_to_draw = 0
        if pyxel.btnp(pyxel.KEY_UP) and self.party_choice_number != 0:
            self.party_choice_number += -1
        elif pyxel.btnp(pyxel.KEY_DOWN) and self.party_choice_number != self.number_of_parties()-1:
            self.party_choice_number += 1
        elif pyxel.btnp(pyxel.KEY_RETURN) and self.party_choice_number in self.check_free_parties():
            action = f"/join {self.party_choice_number+1}"
            self.party_interactions(action)
    
    # Draws the menu of selection of a party
    def draw_choose_party(self):
        buttons_coords = {
                          "x" : (500/size, 500/size, 500/size),
                          "y" : (83/size, 416/size, 748/size),
                          "w" : (int(920/size), int(920/size), int(920/size)),
                          "h" : (int(250/size), int(250/size), int(250/size))
                         }
        for draw_button in range(len(buttons_coords["x"])):
            if (draw_button+(self.party_choice_number//3)*3)+1 in self.check_empty_parties():
                self.draw_text(f"{self.party_choice_number} Empty", (int(600/size), int(buttons_coords["y"][draw_button]+50/size)))
            elif (draw_button+(self.party_choice_number//3)*3)+1 in self.check_free_parties():
                self.draw_text(f"{self.party_choice_number} Player", (int(600/size), int(buttons_coords["y"][draw_button]+50/size)))
            elif (draw_button+(self.party_choice_number//3)*3)+1 <= self.number_of_parties():
                self.draw_text(f"{self.party_choice_number} Full", (int(600/size), int(buttons_coords["y"][draw_button]+50/size)))
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
        self.draw_text("join", (750/size, int(450/size)))
        self.draw_text("create", (600/size, int(800/size)))

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
                elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2, 3, 4, 5, 6, 7]:
                    self.choice_position += -1
                elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and self.game.check_column(
                        self.choice_position - 1) == True:
                    self.game.drop_piece(self.choice_position - 1)
                    client.send(f"/play {self.choice_position - 1}".encode("utf-8"))
                    # Waiting for the answer of the server
                    data = client.recv(4096).decode("utf-8")
                    data = json.loads(data)
                    print(f'{data} quand on joue')
                    # Updates the board
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
        if self.game.player_turn_number == self.player_number:
            pyxel.circ((150 * (self.choice_position - 1) + 510) / size, 75 / size, 70 / size,
                       2 * (self.player_number - 1) + 8)
        else:
            self.draw_text("Waiting...", (0, 0))

    # Returns a list of all the parties with less than 2 players in them
    def check_free_parties(self):
        client.send(b"/partylist")
        data = client.recv(4096).decode("utf-8")
        data = json.loads(data)
        #print("Debug :", data)
        free_party_list = []
        for game_id in range(len(data)):
            if len(data[str(game_id+1)]["joueurs"]) < 2:
                free_party_list.append(int(game_id+1))
        return free_party_list
    
    def check_empty_parties(self):
        client.send(b"/partylist")
        data = client.recv(4096).decode("utf-8")
        data = json.loads(data)
        #print("Debug :", data)
        empty_party_list = []
        for game_id in range(len(data)):
            if len(data[str(game_id+1)]["joueurs"]) == 0:
                empty_party_list.append(int(game_id+1))
        return empty_party_list

    def number_of_parties(self):
        client.send(b"/partylist")
        data = client.recv(4096).decode("utf-8")
        data = json.loads(data)
        #print("Debug :", data)
        return len(data)
    
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
            exit()

    
    def draw_text(self, text : str, coords : tuple):
        coords = list(coords)
        text = text.lower()
        letters_coords = {
            "exemple" : (
                'file',
                'image',
                'width',
                'height',
                'from-x',
                'from-y',
                'width2'
            ),
            "futur a" : ("letter1", 0, 10, 15, 0, 0),
            

            "a" : (10, 15, 0, 0, 88, 0, 1),
            "b" : (9, 15, 80, 0, 80, 0, 1),
            "c" : (10, 15, 152, 0, 88, 0, 1),
            "d" : (9, 15, 0, 120, 80, 0, 1),
            "e" : (10, 15, 88, 120, 96, 0, 1),
            "f" : (6, 15, 172, 120, 56, 0, 1),
            "g" : (9, 15, 0, 0, 80, 1, 1),
            "h" : (9, 15, 88, 0, 80, 1, 1),
            "i" : (2, 15, 184, 0, 24, 1, 1),
            "j" : (4, 15, 0, 120, 40, 1, 1),
            "k" : (10, 15, 48, 120, 88, 1, 1),
            "l" : (3, 15, 128, 120, 32, 1, 1),
            "m" : (14, 15, 0, 0, 120, 2, 1),
            "n" : (10, 15, 128, 0, 96, 2, 1),
            "o" : (10, 15, 0, 128, 96, 2, 1),
            "p" : (10, 15, 88, 128, 88, 2, 1),
            "q" : (9, 15, 176, 128, 80, 2, 1),
            "r" : (6, 15, 0, 0, 56, 0, 2),
            "s" : (9, 15, 48, 0, 80, 0, 2),
            "t" : (5, 15, 120, 0, 48, 0, 2)
        }
        for letter in text:
            try:
                pyxel.load(f"letter{letters_coords[letter][6]}.pyxres")
                for w, h in tool.product(range(letters_coords[letter][0]), range(letters_coords[letter][1])):
                    pyxel.blt(coords[0]+w*8, coords[1]+h*8, letters_coords[letter][5], letters_coords[letter][2]+w*8, letters_coords[letter][3]+h*8, 8, 8)
                coords[0] += letters_coords[letter][4]
            except KeyError:
                pass
            
# Connects to the lobby and then starts the game
if __name__ == "__main__":
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("Debug : Connexion au serveur...")
    try:
        client.connect(("172.16.50.253", 62222))
    except OSError:
        print("Cannot connect to the server ; Try updating ; Try later")
        exit()
    
    #print("Debug : Connexion au lobby...")

    App()
