def create_board():
    board = [[0 for x in range(7)] for y in range(6)]
    return board

def check_column(column_number):
    if board[5][column_number] == 0:
        n = 5
        while board[n][column_number] == 0:
            n += -1
        board[n+1][column_number] = color_turn
        return board
    else:
        return False
