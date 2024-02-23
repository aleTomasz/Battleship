import re
import string

free_tile_sign = '0'


def generate_board(size):
    return [[free_tile_sign for i in range(size)] for i in range(size)]


def logo_read():
    file = open('logo.txt', 'rt')
    logo = file.read()
    print(logo)


def print_board(board, board_size):
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


# def choose_game_mode():
#     game_mode = ['1', '2']
#     print('Welcome to Battleship!')
#     while True:
#         print('Please choose game mode:')
#         print('\t1. Single player \n\t2. Multiplayer')
#         game_mode_selection = input('Whats your decision captain? ')
#         if game_mode_selection in game_mode:
#             return game_mode_selection
#         else:
#             print('Invalid choice. Please try again.')


def get_name(player_number, used_names=None):
    while True:
        player = input(f'{player_number} player name: ').strip().upper()
        if player == '' or player.isspace():
            print(f'Incorrect input! Please share your name')
        elif player in used_names:
            print("This name has already been chosen. Please choose a different one.")
        else:
            return player


def get_board_size():
    board_size_options = [str(i) for i in range(5, 11)]
    while True:
        board_size_choice = input('Please share board size number for row & column from 5 to 10: ')
        if board_size_choice in board_size_options:
            return int(board_size_choice)
        else:
            print('Please try again! Pick a size from 5 to 10')


def get_turn_limit():
    turn_options = [str(i) for i in range(5, 51)]
    while True:
        turn_option_choice = input('Please share turn limit from 5 to 50: ')
        if turn_option_choice in turn_options:
            return int(turn_option_choice)
        else:
            print('Invalid input! (must be between 5-50)')


def display_board(board_size_choice, player, ship_positions=None):
    board_size = [int(size) for size in range(1, int(board_size_choice) + 1)]
    alphabet = [chr(letter) for letter in range(ord('A'), ord('A') + board_size_choice)]
    header = '   ' + '  '.join(str(size) for size in board_size) + '  ||'
    max_size_length = len(header)
    print(player.center(max_size_length, '='))
    print(header)
    for row_index, row_letter in enumerate(alphabet[:board_size_choice]):
        row_display = []
        for col_index in range(1, board_size_choice + 1):
            position = f"{row_letter}{col_index}"
            if position in ship_positions:
                row_display.append(f'\u001b[1m\u001b[32m X \u001b[0m')
            else:
                row_display.append(" 0 ")
        print(f"{row_letter} " + "".join(row_display) + " ||")


def assigning_ship_types(board_size_choice):
    ship_quantities = {
        5: {'one-masted': 3, 'two-masted': 2, 'three-masted': 1, 'four-masted': 0},
        6: {'one-masted': 4, 'two-masted': 3, 'three-masted': 1, 'four-masted': 0},
        7: {'one-masted': 4, 'two-masted': 2, 'three-masted': 2, 'four-masted': 0},
        8: {'one-masted': 4, 'two-masted': 3, 'three-masted': 2, 'four-masted': 0},
        9: {'one-masted': 4, 'two-masted': 3, 'three-masted': 1, 'four-masted': 1},
        10: {'one-masted': 4, 'two-masted': 3, 'three-masted': 2, 'four-masted': 1}
    }
    return ship_quantities[board_size_choice]


def generate_board_choices(board_size_choice):
    alphabet = [chr(letter) for letter in range(ord('A'), ord('Z') + 1)]
    board_choices = []
    for letter in alphabet[:board_size_choice]:
        for number in range(1, board_size_choice + 1):
            board_choices.append(letter + str(number))
    return board_choices


def get_valid_input(board_choices, ship_positions):
    while True:
        ship_place = input('Ship starting position placement: ').upper()
        if ship_place in board_choices and ship_place not in ship_positions:
            return ship_place
        elif ship_place in ship_positions:
            print('Place already occupied! Please try again!')
        else:
            print('Out of range! Please try again!')


def determining_ship_length(ship_type):
    ship_length = 0
    if ship_type == 'one-masted':
        ship_length = 1
    if ship_type == 'two-masted':
        ship_length = 2
    if ship_type == 'three-masted':
        ship_length = 3
    if ship_type == 'four-masted':
        ship_length = 4
    return ship_length


def check_surroundings(position, ship_positions):
    row, col = position[0], int(position[1])
    surrounding_positions = [(row, col - 1), (row, col + 1), (chr(ord(row) - 1), col), (chr(ord(row) + 1), col)]
    for r, c in surrounding_positions:
        if f'{r}{c}' in ship_positions:
            return False
    return True


def place_multi_masted_ship(board_choices, ship_length, ship_positions, board_size_choice,player_board):
    while True:
        multi_ship_coordinates = []
        start_place = get_valid_input(board_choices, ship_positions)
        if ship_length == 1:
            if check_surroundings(start_place, ship_positions):
                coordinates_row, coordinates_column = translate_coordinates(start_place)
                player_board[coordinates_row][coordinates_column] = 'X'
                return [start_place]
            else:
                print("Ships are too close! Choose a different starting place.")
                continue
        elif (int(start_place[1]) + ship_length > board_size_choice + 1
              and ord(start_place[0]) + ship_length - 1 > ord('A') + board_size_choice):
            print("Ship doesn't fit in this direction. Choose a different starting place.")
            continue
        else:
            direction = input("Enter direction (H for horizontal, V for vertical, B to go back): ").upper()
            if direction == 'H':
                if int(start_place[1]) + ship_length > board_size_choice:
                    print("Ship doesn't fit in this direction. Choose a different starting place.")
                    continue
                for i in range(ship_length):
                    new_position = start_place[0] + str(int(start_place[1]) + i)
                    multi_ship_coordinates.append(new_position)
                    coordinates_row, coordinates_column = translate_coordinates(new_position)
                    player_board[coordinates_row][coordinates_column] = 'X'
            elif direction == 'V':
                if ord(start_place[0]) + ship_length - 1 > ord('A') + board_size_choice:
                    print("Ship doesn't fit in this direction. Choose a different starting place.")
                    continue
                end_row = chr(ord(start_place[0]) + ship_length - 1)
                for i in range(ord(start_place[0]), ord(end_row) + 1):
                    new_position = chr(i) + start_place[1]
                    multi_ship_coordinates.append(new_position)
                    coordinates_row, coordinates_column = translate_coordinates(new_position)
                    player_board[coordinates_row][coordinates_column]='X'
            elif direction == 'B':
                continue
            else:
                print('Invalid choice. Try again.')
            if all(check_surroundings(position, ship_positions) for position in multi_ship_coordinates):
                return multi_ship_coordinates
            else:
                print("Ships are too close! Choose a different starting place.")


def ship_placement(board_size_choice, ship_quantities, player, player_board):
    board_choices = generate_board_choices(board_size_choice)
    ship_types_and_quantities = {'one-masted': ship_quantities['one-masted'],
                                 'two-masted': ship_quantities['two-masted'],
                                 'three-masted': ship_quantities['three-masted'],
                                 'four-masted': ship_quantities['four-masted']}
    ship_positions = []
    for ship_type, ship_type_quantity in ship_types_and_quantities.items().__reversed__():
        while ship_type_quantity > 0:
            for _ in range(ship_type_quantity):
                #display_board(board_size_choice, player, ship_positions)
                print_board(player_board,board_size_choice)
                print(f'Remaining {ship_type} ship(s) to allocate: {ship_type_quantity}')
                ship_length = determining_ship_length(ship_type)
                ship_positions.extend(place_multi_masted_ship(board_choices, ship_length, ship_positions,
                                                              board_size_choice,player_board))
                ship_type_quantity -= 1
   # display_board(board_size_choice, player, ship_positions)
    print_board(player_board,board_size_choice)

    print(f'\nAll ships placed for {player}.')
    return ship_positions


def waiting_message(player):
    while True:
        waiting_message = input(f'\n{player}, it\'s time to place your ships. \nPress ENTER')
        if not waiting_message.strip() == '':
            print(f'\nOops! Something else was added by mistake. \nOnce {player} is ready, please only press ENTER')
        else:
            break


def clear_console():
    print('\n' * 100)


def convert_board(ship_positions, board_size_choice):
    board = generate_board(board_size_choice)
    for position in ship_positions:
        index_row, index_column = translate_coordinates(position)
        board[index_row][index_column] = 'X'
    return board


def check_win(board, board_size):
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 'X':
                return 0
    print("You win")
    return 1


def check_sink(player_board, opponent_board, hit_row, hit_column, board_size):
    if hit_row < board_size - 1 and opponent_board[hit_row + 1][hit_column] == 'X':
        return
    if hit_row > 0 and opponent_board[hit_row - 1][hit_column] == 'X':
        return
    if hit_column < board_size - 1 and opponent_board[hit_row][hit_column + 1] == 'X':
        return
    if hit_column > 0 and opponent_board[hit_row][hit_column - 1] == 'X':
        return

    if hit_row < board_size - 1 and opponent_board[hit_row + 1][hit_column] == 'H':
        while hit_row < board_size and opponent_board[hit_row][hit_column] == 'H':
            opponent_board[hit_row][hit_column] = 'S'
            player_board[hit_row][hit_column] = 'S'
            hit_row += 1
        return
    if hit_row > 0 and opponent_board[hit_row - 1][hit_column] == 'H':
        while hit_row >= 0 and opponent_board[hit_row][hit_column] == 'H':
            opponent_board[hit_row][hit_column] = 'S'
            player_board[hit_row][hit_column] = 'S'
            hit_row -= 1
        return
    if hit_column < board_size - 1 and opponent_board[hit_row][hit_column + 1] == 'H':
        while hit_column < board_size and opponent_board[hit_row][hit_column] == 'H':
            opponent_board[hit_row][hit_column] = 'S'
            player_board[hit_row][hit_column] = 'S'
            hit_column += 1
        return
    if hit_column > 0 and opponent_board[hit_row][hit_column - 1] == 'H':
        while hit_column >= 0 and opponent_board[hit_row][hit_column] == 'H':
            opponent_board[hit_row][hit_column] = 'S'
            player_board[hit_row][hit_column] = 'S'
            hit_column -= 1
        return

    opponent_board[hit_row][hit_column] = 'S'
    player_board[hit_row][hit_column] = 'S'


def shot(player_board, opponent_board, board_size):
    shot_coordinates = input("Give shot coordinates: ")
    shot_coordinates_row, shot_coordinates_column = translate_coordinates(shot_coordinates)
    if opponent_board[shot_coordinates_row][shot_coordinates_column] == 'X':
        print("You hit the ship\n")
        player_board[shot_coordinates_row][shot_coordinates_column] = 'H'
        opponent_board[shot_coordinates_row][shot_coordinates_column] = 'H'
        check_sink(player_board, opponent_board, shot_coordinates_row, shot_coordinates_column, board_size)
    else:
        print('You miss')
        player_board[shot_coordinates_row][shot_coordinates_column] = 'M'
        opponent_board[shot_coordinates_row][shot_coordinates_column] = 'M'


def changing_player(player_name):
    input("Press Enter to change player")
    clear_console()
    input(f"{player_name} press Enter to continue game")


def battle(player_one_name, player_two_name, player1_board, player2_board, board_size, turn_limit):
    player1_shoot = generate_board(board_size)
    player2_shoot = generate_board(board_size)
    turn_conut = 0
    while turn_conut < turn_limit:
        changing_player(player_one_name)
        print(f'{player_one_name} turn\n')
        print(f'{player_one_name} sea')
        print_board(player1_board, board_size)
        print(f'{player_two_name} sea')
        print_board(player1_shoot, board_size)
        shot(player1_shoot, player2_board, board_size)
        if check_win(player2_board, board_size):
            break
        changing_player(player_two_name)
        print(f'{player_two_name} turn\n')
        print(f'{player_one_name} sea')
        print_board(player2_board, board_size)
        print(f'{player_two_name} sea')
        print_board(player2_shoot, board_size)
        shot(player2_shoot, player1_board, board_size)
        if check_win(player1_board, board_size):
            break
        if turn_limit == turn_conut + 1:
            print("No one won, it's a draw")


def generate_computer_shot(board_size):
    row = random.choice(range(board_size))
    col = random.choice(range(board_size))
    return row, col


def play_game():
    logo_read()
    print('Welcome to Battleship!')
    print('Game Mode is Multiplayer')


    used_names = []
    player_one = get_name('First', used_names)
    used_names.append(player_one)
    player_two = get_name('Second', used_names)

    board_size_choice = get_board_size()
    turn_limit = get_turn_limit()
    board_choices = generate_board_choices(board_size_choice)
    ship_quantities = assigning_ship_types(board_size_choice)

    player = player_one
    waiting_message(player)
    player_one_board=generate_board(board_size_choice)
    ship_placement(board_size_choice, ship_quantities, player,player_one_board)
   # converted_player_one_board = convert_board(player_one_board, board_size_choice)
    clear_console()

    player = player_two
    waiting_message(player)
    player_two_board=generate_board(board_size_choice)
    ship_placement(board_size_choice, ship_quantities, player,player_two_board)
    #converted_player_two_board = convert_board(player_two_board, board_size_choice)

    battle(player_one, player_two, player_one_board, player_two_board, board_size_choice,
           turn_limit)


play_game()
