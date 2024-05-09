from random import randint
import pandas as pd
import global_variables as gv
# from tic_tac_toe import TicTacToe

class AI:
    '''
    The AI class is Artificial intelligence. It is designed to slove the tasks of counting the moves of computer:
    1. contain:
        1.1. difficulty level
        1.2. the сurrent game
        1.3. empty value. It contains object that means empty cell (s) of game field
        1.4. list or dict of win combinations
    2. the actions:
        2.1. starting fill of class
        2.2. calculation of the move taking into account the level of difficulty 

    Fields:
        __difficulty_level - int (integer) - difficulty level
        __сurrent_game - Games, TicTacToe (class) - the current game for which moves are calculated based on the difficulty level
        __empty_value - EmptyValue (class) - it contains object that means empty cell (s) of game field
        __win_combinations - dict (dictionary) - it contains list or dick, or another storage of winning combinations
    '''
    __difficulty_level = 0
    __сurrent_game = None
    __empty_value = None
    __win_combinations = None
    def __init__(self, сurrent_game = None, empty_value = None, win_combinations = None, difficulty_level = 0) -> None:
        self.__difficulty_level = difficulty_level
        self.__сurrent_game = сurrent_game
        self.__empty_value = empty_value
        self.__win_combinations = win_combinations

    def get_ai_move(self, data_dict = None):
        from tic_tac_toe import TicTacToe
        from battleship import Battleship
        if type(self.__сurrent_game) == TicTacToe:
            return self.get_tic_tac_toe_move() 
        elif type(self.__сurrent_game) == Battleship:
            return self.get_battleship_move(data_dict) 
        else:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(AI, 'get_ai_move', 'error_when_get_ai_move__сurrent_game_is_not_correct_type', '01', 3, True))

    def get_battleship_move(self, data_dict):
        game_field = data_dict['game_field']
        list_of_options = self.get_ready_list_of_options_of_battleship(game_field)
        size_of_list_of_options = len(list_of_options)
        list_index = randint(0, size_of_list_of_options - 1) if size_of_list_of_options > 1 else 0
        return list_of_options[list_index]

    def get_ready_list_of_options_of_battleship(self, game_field): 
        list_of_game_field = game_field.get_field_as(list)       
        dict_in_df = {
                'cell': [],
                'num_row': [],
                'num_column': [],
                'cost': [],
        }  
        i = 0
        j = 0
        list_cells_for_proccessing = []
        for cells in list_of_game_field:
            j = 0
            for cell in cells:
                if cell.value.is_hit and cell.value.is_ship_cell_value:
                    list_cells_for_proccessing.append(cell)
                elif cell.value.is_free_cell:
                    dict_in_df['cell'].append(cell)
                    dict_in_df['num_row'].append(i)
                    dict_in_df['num_column'].append(j)
                    dict_in_df['cost'].append(0) 
                j += 1
            i += 1  
        try:
            for cell in list_cells_for_proccessing:
                if cell.value.is_hit and cell.value.is_ship_cell_value:     
                    cell_coordinates = cell.coordinates
                    for shift in range(-1, 2):
                        if shift == 0:
                            continue
                        list_of_coordinates = []
                        list_of_coordinates.append((cell_coordinates[0], cell_coordinates[1] + shift))
                        list_of_coordinates.append((cell_coordinates[0] + shift, cell_coordinates[1]))
                        for coordinates in list_of_coordinates:
                            index_of_cell = None
                            x_coor = coordinates[0]
                            y_coor = coordinates[1]
                            for i in range(len(dict_in_df['cell'])):
                                if dict_in_df['num_row'][i] == x_coor and dict_in_df['num_column'][i] == y_coor:
                                    index_of_cell = i
                                    break
                            if not index_of_cell is None:
                                dict_in_df['cost'][index_of_cell] += 10
        except BaseException as be:
            print(be)
        try:
            list_of_plus_minus = [-1, 1]
            for i in range(len(dict_in_df['cell'])):
                cell = dict_in_df['cell'][i]
                cell_coordinates = cell.coordinates
                start_x = cell_coordinates[0]
                start_y = cell_coordinates[1]
                for shift in range(1, 5):
                    no_x_cells = True
                    no_y_cells = True
                    for plus_minus in list_of_plus_minus:
                        x = start_x + (plus_minus * shift)
                        y = start_y + (plus_minus * shift)
                        try:
                            shift_cell = game_field.get_cell(x, start_y)
                            if shift_cell.value.is_hit and shift_cell.valueis_ship_cell_value:
                                no_x_cells = False
                                dict_in_df['cost'][i] += 10
                        except BaseException:
                            pass
                        try:
                            shift_cell = game_field.get_cell(start_x, y)
                            if shift_cell.value.is_hit and shift_cell.valueis_ship_cell_value:
                                no_y_cells = False
                                dict_in_df['cost'][i] += 10
                        except BaseException:
                            pass
                    if no_x_cells and no_y_cells:
                        break
        except BaseException as be:
            print(be)
        no_costs = True
        for cost in dict_in_df['cost']:
            if cost > 0:
                no_costs = False
                break
        list_of_options = []
        if no_costs:
            for i in range(len(dict_in_df['cell'])):
                list_of_options.append((dict_in_df['num_row'][i], dict_in_df['num_column'][i]))
            return list_of_options
        if self.__difficulty_level == 2:  
            for i in range(len(dict_in_df['num_row'])):
                list_of_options.append((dict_in_df['num_row'][i], dict_in_df['num_column'][i])) 
            return list_of_options
        df_of_options = pd.DataFrame(dict_in_df)
        df_of_options.sort_values(['cost'], axis=0, ascending=False, inplace=True)
        if self.__difficulty_level == 0:
            list_of_options.append((df_of_options['num_row'].iloc[0], df_of_options['num_column'].iloc[0]))
        elif self.__difficulty_level == 1:
            n = df_of_options.shape[0]
            useing_n = int(n / 2)
            for i in range(useing_n):
                list_of_options.append((df_of_options['num_row'].iloc[i], df_of_options['num_column'].iloc[i]))
        return list_of_options

    def get_tic_tac_toe_move(self):
        game_data = self.__сurrent_game.get_data_for_ai()
        list_of_options = self.get_ready_list_of_options_of_tic_tac_toe(game_data['game_field'])
        size_of_list_of_options = len(list_of_options)
        list_index = randint(0, size_of_list_of_options - 1) if size_of_list_of_options > 1 else 0
        return list_of_options[list_index]

    def get_ready_list_of_options_of_tic_tac_toe(self, game_field):       
        dict_in_df = {
                'num_row': [],
                'num_column': [],
                'cost': [],
        }  
        i = 0
        j = 0
        for item in game_field:
            j = 0
            for sub_item in item:
                if sub_item.is_empty_value:
                    dict_in_df['num_row'].append(i)
                    dict_in_df['num_column'].append(j)
                    dict_in_df['cost'].append(self.calculate_cost_of_move(i, j, game_field)) 
                j += 1
            i += 1   
        list_of_options = []
        if self.__difficulty_level == 2:  
            for i in range(len(dict_in_df['num_row'])):
                list_of_options.append((dict_in_df['num_row'][i], dict_in_df['num_column'][i])) 
            return list_of_options
        df_of_options = pd.DataFrame(dict_in_df)
        df_of_options.sort_values(['cost'], axis=0, ascending=False, inplace=True)
        if self.__difficulty_level == 0:
            list_of_options.append((df_of_options['num_row'].iloc[0], df_of_options['num_column'].iloc[0]))
        elif self.__difficulty_level == 1:
            n = df_of_options.shape[0]
            useing_n = int(n / 2)
            for i in range(useing_n):
                list_of_options.append((df_of_options['num_row'].iloc[i], df_of_options['num_column'].iloc[i]))
        return list_of_options

    def calculate_cost_of_move(self, num_row, num_column, game_field):
        start_costs = [
            [3, 0, 3],
            [0, 5, 0],
            [3, 0, 3]
        ]
        cost_of_move = start_costs[num_row][num_column]
        if self.check_win_at_one_move_tic_tac_toe(num_row, num_column, game_field):
            cost_of_move += 100
        if self.check_win_at_one_move_of_opponent_tic_tac_toe(num_row, num_column, game_field):
            cost_of_move += 50
        cost_of_move += self.get_cost_priority_move(num_row, num_column, game_field)
        return cost_of_move

    def check_win_at_one_move_tic_tac_toe(self, num_row, num_column, game_field):
        сurrent_gamer = self.__сurrent_game.сurrent_gamer
        for key_of_category_of_win_combinations in self.__win_combinations:
            category_of_win_combinations = self.__win_combinations[key_of_category_of_win_combinations]
            for win_combinations in category_of_win_combinations:
                for i in range(len(win_combinations)):
                    if num_row == win_combinations[i][0] and num_column == win_combinations[i][1]:
                        summ_win_combination = 0
                        for j in range(len(win_combinations)):
                            if j != i and game_field[win_combinations[j][0]][win_combinations[j][1]] is сurrent_gamer:
                                summ_win_combination += 1
                        if summ_win_combination == len(win_combinations) - 1:
                            return True
        return False  

    def check_win_at_one_move_of_opponent_tic_tac_toe(self, num_row, num_column, game_field):
        сurrent_gamer = self.__сurrent_game.сurrent_gamer
        for key_of_category_of_win_combinations in self.__win_combinations:
            category_of_win_combinations = self.__win_combinations[key_of_category_of_win_combinations]
            for win_combinations in category_of_win_combinations:
                for i in range(len(win_combinations)):
                    if num_row == win_combinations[i][0] and num_column == win_combinations[i][1]:
                        summ_win_combination = 0
                        for j in range(len(win_combinations)):
                            if j != i and not (game_field[win_combinations[j][0]][win_combinations[j][1]] is сurrent_gamer) and not (game_field[win_combinations[j][0]][win_combinations[j][1]].is_empty_value):
                                summ_win_combination += 1
                        if summ_win_combination == len(win_combinations) - 1:
                            return True
        return False

    def get_cost_priority_move(self, num_row, num_column, game_field):
        adding_cost = 10
        cost = 0
        сurrent_gamer = self.__сurrent_game.сurrent_gamer
        for key_of_category_of_win_combinations in self.__win_combinations:
            category_of_win_combinations = self.__win_combinations[key_of_category_of_win_combinations]
            for win_combinations in category_of_win_combinations:
                for i in range(len(win_combinations)):
                    if num_row == win_combinations[i][0] and num_column == win_combinations[i][1]:
                        summ_сurrent_gamer_combination = 0
                        summ_empty_field_combination = 0
                        for j in range(len(win_combinations)):
                            if j != i and game_field[win_combinations[j][0]][win_combinations[j][1]] is сurrent_gamer:
                                summ_сurrent_gamer_combination += 1
                            elif j != i and game_field[win_combinations[j][0]][win_combinations[j][1]] is self.__empty_value:
                                summ_empty_field_combination += 1
                        if summ_сurrent_gamer_combination == 1 and summ_empty_field_combination == 2:
                            cost =+ adding_cost
        return cost

    def set_difficulty_level(self, value):
        self.__difficulty_level = value

    @staticmethod
    def __short_name__():
        return 'AI'