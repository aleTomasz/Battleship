import re
import string

free_tile_sign = '0'


def generate_board(size):
    return [[free_tile_sign for i in range(size)] for i in range(size)]


def generate_board_simple(size):
    board = []
    for _ in range(size):
        row = []
        for __ in range(size):
            row.append(free_tile_sign)
    return board


def print_board(board):
    cell_width = 5
    print(" " * (cell_width + 1), end="")
    # https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html#colors
    # printing colors "{color code} text {reset code}"
    [print(f'\u001b[1m\u001b[31m{i:^{cell_width}}\u001b[0m', end='') for i in range(1, 11)]
    for i, row in enumerate(board):
        print()
        print(f'\u001b[1m\u001b[31m{string.ascii_uppercase[i]:^{cell_width}}|\u001b[0m', end="")
        for cell in row:
            print(f'{cell:^{cell_width}}', end='')
    print()

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


def is_coordinate_on_board(game_board: list, board_vertical_index: int, board_horizontal_index: int):
    max_vertical = len(game_board) - 1
    max_horizontal = len(game_board[0]) - 1

    return 0 <= board_vertical_index <= max_vertical \
        and 0 <= board_horizontal_index <= max_horizontal


def is_position_safe_to_place_ship(game_board: list, coordinate: tuple):
    vertical_coordinate, horizontal_coordinate = coordinate

    if not is_coordinate_on_board(game_board, coordinate[0], coordinate[1]):
        raise Exception("coordinate not on board")

    # exist = not outside board
    # direction OK = cell is free if on board, if not in scope of the board, we can assume that also safe (no ship outside board)
    is_up_exist = is_coordinate_on_board(game_board, vertical_coordinate - 1, horizontal_coordinate)
    is_down_exist = is_coordinate_on_board(game_board, vertical_coordinate + 1, horizontal_coordinate)
    is_left_exist = is_coordinate_on_board(game_board, vertical_coordinate, horizontal_coordinate - 1)
    is_right_exist = is_coordinate_on_board(game_board, vertical_coordinate, horizontal_coordinate + 1)

    is_up_ok = game_board[vertical_coordinate - 1][horizontal_coordinate] == free_tile_sign if is_up_exist else True
    is_down_ok = game_board[vertical_coordinate + 1][horizontal_coordinate] == free_tile_sign if is_down_exist else True
    is_left_ok = game_board[vertical_coordinate][horizontal_coordinate-1] == free_tile_sign if is_left_exist else True
    is_right_ok = game_board[vertical_coordinate][horizontal_coordinate+1] == free_tile_sign if is_right_exist else True

    return is_up_ok and is_down_ok and is_left_ok and is_right_ok

    # tuple (vertical, horizontal)
    # up = (vertical_coordinate - 1, horizontal_coordinate)
    # down = (vertical_coordinate + 1, horizontal_coordinate)
    # right = (vertical_coordinate, horizontal_coordinate + 1)
    # left = (vertical_coordinate, horizontal_coordinate - 1)


if __name__ == "__main__":
    board_size = 10
    board = generate_board(board_size)
    print_board(board)
    print()
    print("=" * 40)
    index_row, index_column = translate_coordinates("D6")
    # D=down, U=up, L=left, R=right
    board[index_row][index_column] = "X"
    board[index_row - 1][index_column] = "U"
    board[index_row + 1][index_column] = "D"
    board[index_row][index_column - 1] = "L"
    board[index_row][index_column + 1] = "R"
    board[index_row - 1][index_column - 1] = "UL"
    board[index_row + 1][index_column + 1] = "DR"
    board[index_row - 1][index_column + 1] = "UR"
    board[index_row + 1][index_column - 1] = "DL"
    print_board(board)

    print(f'-->> D6 can place ship: {is_position_safe_to_place_ship(board, translate_coordinates("D6"))}')
    print(f'//// A1 can place ship: {is_position_safe_to_place_ship(board, translate_coordinates("A1"))}')
    try:
        print(f'||||  are coordinates on board: {is_coordinate_on_board(board, *translate_coordinates("Z1"))}')
        print(f'|||| Z1 can place ship: {is_position_safe_to_place_ship(board, translate_coordinates("Z1"))}')
    except Exception as e:
        print(f"|||| Z1 raise exception [{e}]")

    try:
        print(f'^^^^ AA is {translate_coordinates("AA")}')
    except Exception as e:
        print(f"|||| AA rise exception {e}")

    try:
        print(f'^^^^ 111 is {translate_coordinates("111")}')
    except Exception as e:
        print(f"|||| 111 rise exception {e}")

    try:
        print(f'^^^^ 1A is {translate_coordinates("111")}')
    except Exception as e:
        print(f"|||| 1A rise exception {e}")

    try:
        print(f'^^^^ 111111A is {translate_coordinates("111111A")}')
    except Exception as e:
        print(f"|||| A112 rise exception {e}")

    print(f'^^^^ D6 is {translate_coordinates("D6")}')
    print(f'^^^^ d6 is {translate_coordinates("D6")}')

    print()
    print("=" * 40)
