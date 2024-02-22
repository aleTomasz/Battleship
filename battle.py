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



def check_win(board,board_size):
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j]=='X':
                return 0
    print("You win")
    return 1

def check_sink(player_board,opponent_board, hit_row, hit_column, board_size):
    if opponent_board[hit_row + 1][hit_column]== 'X' or opponent_board[hit_row - 1][hit_column]== 'X' or opponent_board[hit_row][hit_column + 1]== 'X' or opponent_board[hit_row][hit_column - 1]== 'X':
        return
    if opponent_board[hit_row + 1][hit_column]== 'H' or opponent_board[hit_row - 1][hit_column]== 'H' :
        while opponent_board[hit_row][hit_column]== 'H' and hit_row!=0:
            hit_row-=1
        while  hit_row<board_size:
            hit_row+=1
            if opponent_board[hit_row][hit_column]== 'X' or opponent_board[hit_row][hit_column]== '0':
                hit_row -= 1
                break
        while opponent_board[hit_row][hit_column]== 'H' and hit_row>0:
            opponent_board[hit_row][hit_column]= 'S'
            player_board[hit_row][hit_column] = 'S'
            hit_row-=1
    elif opponent_board[hit_row][hit_column + 1]== 'H' or opponent_board[hit_row][hit_column - 1]== 'H':
        while opponent_board[hit_row][hit_column]== 'H' and hit_column!=0:
            hit_column-=1
        while  hit_column<board_size:
            hit_column+=1
            if opponent_board[hit_row][hit_column]== 'X' or opponent_board[hit_row][hit_column]== '0':
                hit_column-=1
                break
        while opponent_board[hit_row][hit_column] == 'H' and hit_column >=0:
            opponent_board[hit_row][hit_column]= 'S'
            player_board[hit_row][hit_column] = 'S'
            hit_column-=1
    else:
        opponent_board[hit_row][hit_column] = 'S'
        player_board[hit_row][hit_column] = 'S'


def shot(player_board,opponent_board,board_size):
    shot_coordinates = input("Give shot coordinates")
    shot_coordinates_row, shot_coordinates_column = translate_coordinates(shot_coordinates)
    if opponent_board[shot_coordinates_row][shot_coordinates_column]== 'X':
        print("You  hit the ship\n")
        player_board[shot_coordinates_row][shot_coordinates_column] = 'H'
        opponent_board[shot_coordinates_row][shot_coordinates_column] = 'H'
        check_sink(player_board,opponent_board, shot_coordinates_row, shot_coordinates_column, board_size)
    else:
        print('You miss')
        player_board[shot_coordinates_row][shot_coordinates_column] = 'M'
        opponent_board[shot_coordinates_row][shot_coordinates_column] = 'M'

def battle(player1_board, player2_board, board_size, turn_limit):
    player1_shoot=generate_board(board_size)
    player2_shoot=generate_board(board_size)
    turn_conut=0
    while turn_conut<turn_limit:
        print('Player_one turn\n')
        print('Your sea')
        print_board(player1_board)
        print('Opponent sea')
        print_board(player1_shoot)
        shot(player1_shoot,player2_board,board_size)
        if check_win(player2_board,board_size):
            break
        print('Player_two turn\n')
        print('Your sea')
        print_board(player2_board)
        print('Opponent sea')
        print_board(player2_shoot)
        shot(player2_shoot, player1_board, board_size)
        if check_win(player1_board,board_size):
            break



board_size = 5
player1_board = generate_board(board_size)
player2_board = generate_board(board_size)
turn_limit=5

index_row, index_column = translate_coordinates("B1")
player2_board[index_row][index_column] = 'X'
index_row, index_column = translate_coordinates("b2")
player1_board[index_row][index_column] = 'X'
index_row, index_column = translate_coordinates("b3")
player2_board[index_row][index_column] = 'X'

battle(player1_board,player2_board,board_size,turn_limit)