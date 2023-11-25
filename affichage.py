import pyxel
import time
import itertools as tool

class App:
    def __init__(self, player_list, player_number):
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.player_turn_number = 1
        self.player_list = player_list        
        self.player_number = self.nickname_to_number(player_number)
        self.choice_position = 0 
        self.pause = False
        pyxel.init(1920, 1080, title = "Online Power 4")
        pyxel.run(self.update, self.draw)

    #Return le pseudo du joueur en fonction de son numéro
    def number_to_nickname(self, player_number):
        return self.player_list[player_number-1]

    #Return le numéro du joueur en fonction de son pseudo
    def nickname_to_number(self, player_nickname):
        if str(player_nickname) == self.player_list[0]:
            return 1
        else:
            return 2

    #Return si la colone column_number est libre ou non
    def check_column(self, column_number):
        if self.board[5][column_number] == 0:
            return True
        else:
            return False

    #Return le tableau avec le jeton placé à la bonne hauteur dans la colone column_number
    def drop_piece(self, column_number):
        n = 5
        while self.board[n][column_number] == 0 and n !=-1:
            n += -1
        self.board[n+1][column_number] = self.player_turn_number
        return self.board

    #Check si il y a 4 jetons alignés horizontalement (-) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
    def check_victory_h(self):
        winner = 0
        for check_x, check_y in tool.product(range(4), range(6)):
            n = 0
            stop = False
            while self.board[check_y][check_x+n] == self.board[check_y][check_x] and stop == False and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    stop = True
                    winner = self.board[check_y][check_x]
        return int(winner)

    #Check si il y a 4 jetons alignés verticalement (|) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
    def check_victory_v(self):
        winner = 0
        for check_x, check_y in tool.product(range(7), range(3)):
            n = 0
            stop = False
            while self.board[check_y+n][check_x] == self.board[check_y][check_x] and stop == False and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    stop = True
                    winner = self.board[check_y][check_x]
        return int(winner)

    #Check si il y a 4 jetons alignés diagonalement (/) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.      
    def check_victory_dp(self):
        winner = 0
        for check_x, check_y in tool.product(range(4), range(3)):
            n = 0
            stop = False
            while self.board[check_y+n][check_x+n] == self.board[check_y][check_x] and stop == False and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    stop = True
                    winner = self.board[check_y][check_x]
        return int(winner)

    #Check si il y a 4 jetons alignés diagonalement (\) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
    def check_victory_dm(self):
        winner = 0
        for check_x, check_y in tool.product([3,4,5,6], range(3)):
            n = 0
            stop = False
            while self.board[check_y+n][check_x-n] == self.board[check_y][check_x] and stop == False and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    stop = True
                    winner = self.board[check_y][check_x]
        return int(winner)

    #Return True si le plateau est plein ; False si le plateau a toujours des cases libres
    def check_tie(self):
        for column_check_number in range(7):
            if self.board[5][column_check_number] == 0:
                return False
        return True

    #Return le numéro du joueur qui doit jouer ne fonction du joueur qui vient de jouer:
    def change_player_turn(self):
        if self.player_turn_number == 1:
            return 2
        else:
            return 1
        
    #Si le joueur qui doit jouer correspond au joueur sur ce client, alors il joue sinon il attends que l'autre joueur face une quelquonque action
    def update(self):
        if self.player_turn_number == self.player_number:
            if pyxel.btnp(pyxel.KEY_RIGHT) and self.choice_position in [0,1,2,3,4,5,6]:
                self.choice_position += 1
            elif pyxel.btnp(pyxel.KEY_LEFT) and self.choice_position in [2,3,4,5,6,7]:
                self.choice_position += -1
            elif pyxel.btnp(pyxel.KEY_DOWN) and self.choice_position != 0 and self.check_column(self.choice_position-1) == True:
                self.drop_piece(self.choice_position-1)
                self.player_turn_number = self.change_player_turn()
                self.choice_position = 0
                #Send self.board to the other player

        else:
            #Waiting for the other player to send a message then self.draw()
            pass
    #Peut importe si le joueur doit jouer ou non, il dessine le tableau de jeu et vérifie si il y a un gagnant
    def draw(self):
        pyxel.cls(0)
        for draw_x, draw_y in tool.product(range(7), range(6)):
            if self.board[draw_y][draw_x] == 0:
                pyxel.rect(150*draw_x+435, 930-150*draw_y, 150, 150, 1)
            if self.board[draw_y][draw_x] == 1:
                pyxel.rect(150*draw_x+435, 930-150*draw_y, 150, 150, 8)
            if self.board[draw_y][draw_x] == 2:
                pyxel.rect(150*draw_x+435, 930-150*draw_y, 150, 150, 10)
        pyxel.rect(150*(self.choice_position-1)+435, 0, 150, 150, 9)
        if self.check_victory_h() != 0:
            winner = self.check_victory_h()
            winner = self.number_to_nickname(winner)
            pyxel.text(0, 0, f"{winner} has won!", 7)
            time.sleep(1)
            exit()
        elif self.check_victory_v() != 0:
            winner = self.check_victory_h()
            winner = self.number_to_nickname(winner)
            pyxel.text(0, 0, f"{winner} has won!", 7)
            time.sleep(1)
            exit()
        elif self.check_victory_dp() != 0:
            winner = self.check_victory_h()
            winner = self.number_to_nickname(winner)
            pyxel.text(0, 0, f"{winner} has won!", 7)
            time.sleep(1)
            exit()
        elif self.check_victory_dm() != 0:
            winner = self.check_victory_h()
            winner = self.number_to_nickname(winner)
            pyxel.text(0, 0, f"{winner} has won!", 7)
            time.sleep(1)
            exit()
        elif self.check_tie() == True:
            pyxel.text(0, 0, "This game ended on a tie!", 7)
            time.sleep(1)
            exit()

#Ici tu te connecte au serveur(tu te demerde) et je veux juste que la liste des joueurs et le pseudo du joueur sur ce client ressortent.
App(["Freud", "Karl"], "Freud")#Ici la ligne représente la liste des joueurs, donnée par le serveur ; le "Freud" lui représente le pseudo du joueur sur lequel tourne ce code.
