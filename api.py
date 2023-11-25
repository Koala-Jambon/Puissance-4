import itertools as tool


# Return le pseudo du joueur en fonction de son numéro
def number_to_nickname(player_number, player_list):
    return player_list[player_number-1]

    # Return le numéro du joueur en fonction de son pseudo


def nickname_to_number(player_nickname, player_list):
    if str(player_nickname) == player_list[0]:
        return 1
    else:
        return 2

    # Return si la colone column_number est libre ou non


def board():
    # Retourne le tableau de jeu
    return [[0 for _ in range(7)] for _ in range(6)]

def check_column(column_number, board):
    if board[5][column_number] == 0:
        return True
    else:
        return False

# Return le tableau avec le jeton placé à la bonne hauteur dans la colone column_number


def drop_piece(column_number, board, player_turn_number):
    n = 5
    while board[n][column_number] == 0 and n !=-1:
        n += -1
    board[n+1][column_number] = player_turn_number
    return board

# Check si il y a 4 jetons alignés horizontalement (-) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_h(board):
    winner = 0
    for check_x, check_y in tool.product(range(4), range(6)):
        n = 0
        stop = False
        while board[check_y][check_x+n] == board[check_y][check_x] and stop == False and board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return int(winner)

#Check si il y a 4 jetons alignés verticalement (|) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_v(board):
    winner = 0
    for check_x, check_y in tool.product(range(7), range(3)):
        n = 0
        stop = False
        while board[check_y+n][check_x] == board[check_y][check_x] and stop == False and board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return int(winner)

#Check si il y a 4 jetons alignés diagonalement (/) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.      
def check_victory_dp(board):
    winner = 0
    for check_x, check_y in tool.product(range(4), range(3)):
        n = 0
        stop = False
        while board[check_y+n][check_x+n] == board[check_y][check_x] and stop == False and board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return int(winner)

#Check si il y a 4 jetons alignés diagonalement (\) : Ne Return pas si il n'y a aucun gagnant pour le moment ; 1 Si le 1 a gagné ; 2 Si le 2 a gagné.
def check_victory_dm(board):
    winner = 0
    for check_x, check_y in tool.product([3,4,5,6], range(3)):
        n = 0
        stop = False
        while board[check_y+n][check_x-n] == board[check_y][check_x] and stop == False and board[check_y][check_x] != 0:
            if n != 3:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return int(winner)

#Return True si le plateau est plein ; False si le plateau a toujours des cases libres
def check_tie(board):
    for column_check_number in range(7):
        if board[5][column_check_number] == 0:
            return False
    return True

#Return le numéro du joueur qui doit jouer ne fonction du joueur qui vient de jouer:
def change_player_turn(player_turn_number):
    if player_turn_number == 1:
        return 2
    else:
        return 1
