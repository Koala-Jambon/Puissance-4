import itertools as tool

#Return le teableau de jeu
def board():
    return [[0 for _ in range(7)] for _ in range(6)]

class Game:
    def __init__(self, player_ip_list, board, player_turn_ip):
        self.player_ip_list = player_ip_list
        self.player_turn_number = self.ip_to_number(player_turn_ip)
        self.board = board


    def actual_board(self):
        return self.board

    def player_turn(self):
        return self.number_to_ip(self.player_turn_number)


    # Return le numéro du joueur en fonction de son IP
    def ip_to_number(self, player_ip):
        if player_ip == self.player_ip_list[0]:
            return 1
        else:
            return 2
            
    #Return l'IP du joueur en fonction de son numéro
    def number_to_ip(self, player_number):
        return self.player_ip_list[player_number-1]
    
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
        self.change_player_turn(self.player_turn_number)
        return self.board
    
    #Check si il y a 4 jetons alignés horizontalement (-) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
    def check_victory_h(self):
        winner = 0
        for check_x, check_y in tool.product(range(4), range(6)):
            n = 0
            while self.board[check_y][check_x+n] == self.board[check_y][check_x] and stop == False and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    winner = self.board[check_y][check_x]
                    return int(winner)
    
    #Check si il y a 4 jetons alignés verticalement (|) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
    def check_victory_v(self):
        winner = 0
        for check_x, check_y in tool.product(range(7), range(3)):
            n = 0
            while self.board[check_y+n][check_x] == self.board[check_y][check_x] and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    winner = self.board[check_y][check_x]
                    return int(winner)
    
    #Check si il y a 4 jetons alignés diagonalement (/) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.      
    def check_victory_dp(self):
        winner = 0
        for check_x, check_y in tool.product(range(4), range(3)):
            n = 0
            while self.board[check_y+n][check_x+n] == self.board[check_y][check_x] and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    winner = self.board[check_y][check_x]
                    return int(winner)
    
    #Check si il y a 4 jetons alignés diagonalement (\) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
    def check_victory_dm(self):
        winner = 0
        for check_x, check_y in tool.product([3,4,5,6], range(3)):
            n = 0
            while self.board[check_y+n][check_x-n] == self.board[check_y][check_x] and self.board[check_y][check_x] != 0:
                if n != 3:
                    n += 1
                else:
                    winner = self.board[check_y][check_x]
                    return int(winner)
    
    #Check si la game doit s'arrêter, soit à cause d'une win ou d'une tie ; Return True si la game doit s'arrêter ; Return False si la Game doit continuer 
    def check_endgame(self):
        for func in ["check_victory_h", "check_victory_v", "check_victory_dp", "check_victory_dm"]:
            if getattr(func)() != 0:
                return True
        if check_tie() == True:
            return True
                
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

