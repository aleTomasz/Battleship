import string
import re


def translate_coordinates(coordinates: str):
    if 2 < len(coordinates) <= 3:
        raise Exception("Invalid coordinates - should have 2 or 3 chars i.e. A1, J10")

    if coordinates[0].lower() not in string.ascii_lowercase:
        raise Exception("Invalid coordinates - should have letter on first place")

    if not coordinates[1:].isdigit():
        raise Exception("Invalid coordinates - should have digit on second and third place")

    # same as 3 ifs above, but shorter using regular expression
    if not re.match(r"^[A-Za-z]{1}[0-9]{1,2}$", coordinates):
        raise Exception("Regular expression check if coordinates are valid - FAIL")

    vertical_coordinate = coordinates[0]
    horizontal_coordinate = coordinates[1:]
    board_vertical_index = string.ascii_lowercase.index(vertical_coordinate.lower())
    board_horizontal_index = int(horizontal_coordinate) - 1

    return board_vertical_index, board_horizontal_index


free_tile_sign = '0'


def generate_board(size):
    return [[free_tile_sign for i in range(size)] for i in range(size)]


def print_board(board):
    cell_width = 5
    print(" " * (cell_width + 1), end="")
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#colors
    # printing colors "{color code} text {reset code}"
    [print(f'\u001b[1m\u001b[31m{i:^{cell_width}}\u001b[0m', end='') for i in range(1, board_size + 1)]
    for i, row in enumerate(board):
        print()
        print(f'\u001b[1m\u001b[31m{string.ascii_uppercase[i]:^{cell_width}}|\u001b[0m', end="")
        for cell in row:
            print(f'{cell:^{cell_width}}', end='')
    print()


def hit_the_ship(board, row, column):
    pass
def check_win(board,board_size):
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j]=='X':
                return 1
    print("You win")
    return 0

def check_sink(board,hit_row,hit_column,board_size):
    if board[hit_row+1][hit_column]=='X' or board[hit_row-1][hit_column]=='X' or board[hit_row][hit_column+1]=='X' or board[hit_row][hit_column-1]=='X':
        return
    if board[hit_row+1][hit_column]=='H' or board[hit_row-1][hit_column]=='H' :
        while board[hit_row][hit_column]=='H' and hit_row!=0:
            hit_row-=1
        while  hit_row<board_size:
            hit_row+=1
            if board[hit_row][hit_column]=='X' or board[hit_row][hit_column]=='0':
                hit_row -= 1
                break
        while board[hit_row][hit_column]=='H' and hit_row>0:
            board[hit_row][hit_column]='S'
            hit_row-=1
    elif board[hit_row][hit_column+1]=='H' or board[hit_row][hit_column-1]=='H':
        while board[hit_row][hit_column]=='H' and hit_column!=0:
            hit_column-=1
        while  hit_column<board_size:
            hit_column+=1
            if board[hit_row][hit_column]=='X' or board[hit_row][hit_column]=='0':
                hit_column-=1
                break
        while board[hit_row][hit_column] == 'H' and hit_column >=0:
            board[hit_row][hit_column]='S'
            hit_column-=1
    else:
        board[hit_row][hit_column] = 'S'


def shot(board):
    shot_coordinates = input("Give shot coordinates")
    shot_coordinates_row, shot_coordinates_column = translate_coordinates(shot_coordinates)
    if board[shot_coordinates_row][shot_coordinates_column ]== 'X':
        print("You  hit the ship\n")
        board[shot_coordinates_row][shot_coordinates_column] = 'H'
        check_sink(board,shot_coordinates_row,shot_coordinates_column,board_size)
    else:
        print('You miss')
        board[shot_coordinates_row][shot_coordinates_column] = 'M'


board_size = 5
board = generate_board(board_size)
print_board(board)
index_row, index_column = translate_coordinates("B1")
board[index_row][index_column] = 'X'
index_row, index_column = translate_coordinates("b2")
board[index_row][index_column] = 'X'
index_row, index_column = translate_coordinates("b3")
board[index_row][index_column] = 'X'
while check_win(board,board_size):
    print_board(board)
    shot(board)
    print_board(board)
