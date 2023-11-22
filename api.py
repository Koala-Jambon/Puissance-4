import itertools

def create_board():
    board = [[0 for x in range(7)] for y in range(6)]
    return board

def check_column(column_number):
    if board[5][column_number] == 0:
        return True
    else:
        return False

def place_token(column_number):
    n = 5
    while board[n][column_number] == 0:
        n += -1
    board[n+1][column_number] = color_turn
    return board

def check_victory_h():
    winner = 0
    for check_x, check_y in tool.product(range(4), range(6))
        n = 0
        stop = False
        while board[check_y][check_x+n] == board[check_y][check_x] and stop == False:
            if n != 4:
                n += 1
            else:
                stop = True
                winner = board[check_y][check_x]
    return winner
        
