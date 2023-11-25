import itertools as tool

#Return le pseudo du joueur en fonction de son numéro
def number_to_nickname(player_number):
    return App.player_list[player_number-1]

    #Return le numéro du joueur en fonction de son pseudo
def nickname_to_number(player_nickname):
    if str(player_nickname) == App.player_list[0]:
        return 1
    else:
        return 2

#Return si la colone column_number est libre ou non
def check_column(column_number):
    if App.board[5][column_number] == 0:
        return True
    else:
        return False

#Return le tableau avec le jeton placé à la bonne hauteur dans la colone column_number
def drop_piece(column_number):
    n = 5
    while App.board[n][column_number] == 0 and n !=-1:
        n += -1
    App.board[n+1][column_number] = App.player_turn_number
    return App.board

#Check si il y a 4 jetons alignés horizontalement (-) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_h():
    winner = 0
    for check_x, check_y in tool.product(range(4), range(6)):
        n = 0
        stop = False
        while App.board[check_y][check_x+n] == App.board[check_y][check_x] and stop == False and App.board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = App.board[check_y][check_x]
    return int(winner)

#Check si il y a 4 jetons alignés verticalement (|) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_v():
    winner = 0
    for check_x, check_y in tool.product(range(7), range(3)):
        n = 0
        stop = False
        while App.board[check_y+n][check_x] == App.board[check_y][check_x] and stop == False and App.board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = App.board[check_y][check_x]
    return int(winner)

#Check si il y a 4 jetons alignés diagonalement (/) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.      
def check_victory_dp():
    winner = 0
    for check_x, check_y in tool.product(range(4), range(3)):
        n = 0
        stop = False
        while App.board[check_y+n][check_x+n] == App.board[check_y][check_x] and stop == False and App.board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = App.board[check_y][check_x]
    return int(winner)

#Check si il y a 4 jetons alignés diagonalement (\) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_dm():
    winner = 0
    for check_x, check_y in tool.product([3,4,5,6], range(3)):
        n = 0
        stop = False
        while App.board[check_y+n][check_x-n] == App.board[check_y][check_x] and stop == False and App.board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = App.board[check_y][check_x]
    return int(winner)

#Return True si le plateau est plein ; False si le plateau a toujours des cases libres
def check_tie():
    for column_check_number in range(7):
        if App.board[5][column_check_number] == 0:
            return False
    return True

#Return le numéro du joueur qui doit jouer ne fonction du joueur qui vient de jouer:
def change_player_turn():
    if App.player_turn_number == 1:
        return 2
    else:
        return 1
