import itertools

#Return un tableau de 7x6 0s
def create_board():
    board = [[0 for x in range(7)] for y in range(6)]
    return board

#Return si la colone column_number est libre ou non
def check_column(column_number):
    if board[5][column_number] == 0:
        return True
    else:
        return False

#Return le tableau avec le jeton placé à la bonne hauteur dans la colone column_number
def place_token(column_number):
    n = 5
    while board[n][column_number] == 0:
        n += -1
    board[n+1][column_number] = color_turn
    return board

#Check si il y a 4 jetons alignés horizontalement (-) : Return 0 si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_h():
    winner = 0
    for check_x, check_y in tool.product(range(4), range(6))
        n = 0
        stop = False
        while board[check_y][check_x+n] == board[check_y][check_x] and stop == False:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return winner

#Check si il y a 4 jetons alignés verticalement (|) : Return 0 si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_v():
    winner = 0
    for check_x, check_y in tool.product(range(7), range(3))
        n = 0
        stop = False
        while board[check_y+n][check_x] == board[check_y][check_x] and stop == False:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return winner

#Check si il y a 4 jetons alignés diagonalement (/) : Return 0 si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.      
def check_victory_dp():
    winner = 0
    for check_x, check_y in tool.product(range(4), range(3))
        n = 0
        stop = False
        while board[check_y+n][check_x+n] == board[check_y][check_x] and stop == False:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return winner

#Check si il y a 4 jetons alignés diagonalement (\) : Return 0 si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_dm():
    winner = 0
    for check_x, check_y in tool.product([3,4,5,6], range(3))
        n = 0
        stop = False
        while board[check_y+n][check_x-n] == board[check_y][check_x] and stop == False:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return winner

#Return True si le plateau est plein ; False si le plateau a toujours des cases libres
def check_tie():
    number_completed_columns = 0
    for column_check_number in range(7):
        if board[5][column_check_number] == 0:
            return False
    return True

#Return le numéro du joueur qui doit jouer ne fonction du joueur qui vient de jouer:
def change_player_turn(player_who_just_played):
    if player_who_just_played == 1:
        return 2
    else:
        return 1