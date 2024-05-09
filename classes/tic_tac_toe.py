import global_variables as gv
from ai import AI
from games import Games
from gamers import Gamers
from empty_value import EmptyValue

class TicTacToe(Games):
    '''
    The TicTacToe class is designed to slove tasks of game Tic tak toe:
    1. contain:
        1.1. setting of game
        1.2. list of gamers
        1.3. the current state of the game 
        1.4. win combinations
    2. the actions:    
        2.1. starting fill of class
        2.2. returning current state of end of the game "__is_end"
        2.3. seting of the settings
        2.4. outputting dialogs with gamer
        2.5. receiving and processing responses from the user
        2.6. identifying and installing the current user
        2.7. identifying winer and end of game if someone wins or runs out of free cells

    Fields:
        __is_end - bool (boolean) - it identifies the end of game
        __empty_value - EmptyValue (class) - it contains object that means empty cell (s) of game field
        __number_of_move - int (integer) - this is count of move
        __game_field - list - this is matrix of cells of game field
        __сurrent_gamer - Gamers (class) - this is a link to the current gamer
        __сurrent_index_of_gamer - int (integer) - this is the index of the current gamer
        __win_combinations - dict (dictionary) - it contains fields of rows, columns and diagonals of winning combinations
        __settings_is_set - bool (boolean) - it identifies the end of the setting settings
        __label_of_current_settings - str (string) - this is mark about current chapter of settings
        __main_commands - dict (dictionary) - this is the dict of lists main commands
        __list_of_gamers - list - this is a list of participating players
        __difficulty_level - int (integer) - difficulty level from 0 (hard) to 2 (easy)
    '''
    __is_end = False
    __empty_value = None
    __number_of_move = 0
    __game_field = []
    __сurrent_gamer = None
    __сurrent_index_of_gamer = 0
    __win_combinations = None
    __settings_is_set = False
    __label_of_current_settings = 'kind_of_settings'
    __main_commands = {
        'exit': ['-ex', 'exit', 'exit()'],
        'back': ['-bk', 'back', 'back()']
    }
    __list_of_gamers = []
    __difficulty_level = 2
    __language = None
    def __init__(self):
        self.__list_of_gamers = []
        self.__empty_value = EmptyValue()
        self.__win_combinations = {
            'rows': (
                ((0, 0), (0, 1), (0, 2)),
                ((1, 0), (1, 1), (1, 2)),
                ((2, 0), (2, 1), (2, 2)),
            ),
            'columns': (
                ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)),
                ((0, 2), (1, 2), (2, 2)),
            ),
            'diagonals': (
                ((0, 0), (1, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)),
            ),
        }
        self.__difficulty_level = 2
        self.__list_of_gamers.append(Gamers('you', 'user', 'O'))
        self.__list_of_gamers.append(Gamers('computer', 'computer', 'X', AI(self, self.__empty_value, self.__win_combinations, self.__difficulty_level)))
        self.__сurrent_gamer = self.__list_of_gamers[0]
        for i in range(3):
            inner_list = []
            for j in range(3):
                inner_list.append(self.__empty_value)
            self.__game_field.append(inner_list)
        self.__settings_is_set = False
        self.__label_of_current_settings = 'kind_of_settings'
        self.__settings = {
            'kind_of_settings': {
                'difficulty_level': {
                    'number': 1,
                    'value': self.__difficulty_level,
                    'name_of_class_field': '__difficulty_level',
                    'title': 'Уровень сложности (Difficulty level)',
                    'commands': ['1', '-dl', 'difficulty_level', 'difficulty level'],
                    },
                },
            'kind_of_options': {
                'difficulty_level': {
                    'hard': {
                        'number': 1,
                        'title': 'Сложно (Hard)',
                        'commands': ['1', '-h', 'hard'],
                        'value': 0,
                    },
                    'medium': {
                        'number': 2,
                        'title': 'Средне (Medium)',
                        'commands': ['2', '-m', 'medium'],
                        'value': 1,
                    },
                    'easy': {
                        'number': 3,
                        'title': 'Легко (Easy)',
                        'commands': ['3', '-e', 'easy'],
                        'value': 2,
                    },
                },
            }
        }

    @property
    def is_end(self) -> bool:
        return self.__is_end

    def setting(self):
        data_dict = {
            'title': 'Настройки игры (Game Settings)',
            'сurrent_value': None,
        }
        while not self.__is_end and not self.__settings_is_set: 
            try:
                if self.__label_of_current_settings == 'kind_of_settings':
                    data_dict['title'] = 'Настройки игры (Game Settings)' 
                    data_dict['сurrent_value'] = None
                self.__show_settings(data_dict) 
            except ValueError as ve:
                print(f'\n{ve}\n') 
        print(self.__difficulty_level)
        

    def __show_settings(self, data_dict):
        print('\n' + data_dict['title'])
        pattern_settings = self.__get_current_settings()
        for item in pattern_settings:
            item_value = pattern_settings[item]
            string_is_сurrent = ''
            if not data_dict['сurrent_value'] is None:
                if data_dict['сurrent_value'] == item_value['value']:
                    string_is_сurrent = 'is сurrent'.upper()
            print(f'{item_value["number"]}) {item_value["title"]} | список команд выбора: {item_value["commands"]} {"| " + string_is_сurrent if string_is_сurrent != "" else ""}')
        print()
        self.processing_input_settings_string(data_dict)

    def processing_input_settings_string(self, data_dict):
        input_string = input(f'Введите свой ход (команды назад {self.__main_commands["back"]}) (команды выхода {self.__main_commands["exit"]}): ')
        low_input_string = input_string.lower()
        if self.__input_main_command(low_input_string, 'exit'):
            self.__is_end = True
            return
        if self.__input_main_command(low_input_string, 'back'):
            if self.__label_of_current_settings == 'kind_of_settings':
                self.__settings_is_set = True
            else:
                self.__label_of_current_settings = 'kind_of_settings'
            return    
        choose_value = None
        list_of_keys = []
        pattern_settings = self.__get_current_settings(list_of_keys)
        is_done = False
        for item in pattern_settings:  
            item_value = pattern_settings[item]
            for sub_item in item_value['commands']:
                if sub_item == low_input_string:
                    choose_value = item_value
                    is_done = True
                    break
            if is_done:
                break
        if choose_value is None:
            raise ValueError(f'Ошибка ввода команды. "{low_input_string}" не является доступным значением (Command input error. "{low_input_string}" is not an available value)')
        else:
            if self.__label_of_current_settings == 'kind_of_settings':
                self.__label_of_current_settings = 'kind_of_options.' + item
                data_dict['сurrent_value'] = choose_value['value']
                data_dict['title'] = choose_value['title']
            else:
                self.__set_value_of_setting(list_of_keys[1], choose_value['value'])
                self.__label_of_current_settings = 'kind_of_settings'

    def __set_value_of_setting(self, key, value):
        self.__settings['kind_of_settings'][key]['value'] = value
        name_of_class_field = self.__settings['kind_of_settings'][key].get('name_of_class_field')
        if not name_of_class_field is None and name_of_class_field != '':
            if name_of_class_field == '__difficulty_level':
                self.__set_difficulty_level(value)

    def __set_difficulty_level(self, value):
        for gamer in self.__list_of_gamers:
            gamer.set_difficulty_level(value)
                        
    def __get_current_settings(self, _list_of_keys = []):
        list_of_keys = self.__label_of_current_settings.split('.')
        result_value = self.__settings
        for item in list_of_keys:
            result_value = result_value[item]
            _list_of_keys.append(item)
        return result_value

    def show(self):
        if self.__сurrent_gamer.is_computer:
            self.proccessing_input(self.__сurrent_gamer.get_ai_move())      
        else:
            self.output()
            input_string = input(f'Введите свой ход (команды выхода {self.__main_commands["exit"]}): ')
            self.proccessing_input(input_string)     
        if self.announce_winner_and_end_game(self.get_winner()):
            return
        if self.annonce_drawn_game_if_fill_all_field_cells():
            return
        self.__set_next_gamer()
            
    def __set_next_gamer(self) -> None:
        self.__number_of_move += 1
        if self.__сurrent_gamer is None:
            self.__сurrent_gamer = self.__list_of_gamers[0]
            self.__сurrent_index_of_gamer = 0
            return
        self.__сurrent_gamer = self.__list_of_gamers[self.__index_next_gamer]

    def get_data_for_ai(self):
        return {
           'list_of_gamers': self.__list_of_gamers.copy(),
           'game_field': self.__game_field.copy(), 
        }

    def annonce_drawn_game_if_fill_all_field_cells(self):
        there_are_free_cells = False
        for item in self.__game_field:
            for sub_item in item:
                if sub_item.is_empty_value:
                    there_are_free_cells = True
        if not there_are_free_cells:
            self.output()
            print('\nИгра окончена! Не осталось свободных клеток! (The game is over! There are no free cells left!)\n')
            self.__is_end = True
        return not there_are_free_cells

    def announce_winner_and_end_game(self, winner):
        if winner is None or winner.is_empty_value:
            return False
        result = False
        final_message = ''
        if winner.is_computer:
            final_message = '\nВы проиграли (You lose)!\n'
            result = True
        else:
            final_message = '\nПоздравляю Вы выиграли (Congratulations You have won)!\n'
            result = True
        if result:
            self.output()
            print(final_message)
            self.__is_end = True    
        return result

    def get_winner(self):
        winner = None
        for key_of_category_of_win_combinations in self.__win_combinations:
            category_of_win_combinations = self.__win_combinations[key_of_category_of_win_combinations]
            for win_combinations in category_of_win_combinations:
                first_field_cell = self.__game_field[win_combinations[0][0]][win_combinations[0][1]]
                second_field_cell = self.__game_field[win_combinations[1][0]][win_combinations[1][1]]
                third_field_cell = self.__game_field[win_combinations[2][0]][win_combinations[2][1]]
                if first_field_cell is second_field_cell and first_field_cell is third_field_cell:
                    winner = first_field_cell
        return winner

    @property
    def __index_next_gamer(self) -> int:
        if self.__сurrent_index_of_gamer >= len(self.__list_of_gamers) - 1:
            self.__сurrent_index_of_gamer = 0
        else:
            self.__сurrent_index_of_gamer += 1
        return self.__сurrent_index_of_gamer

    def output(self):
        if self.__number_of_move > 0:
            print()
        print('|   | 1 | 2 | 3 |')
        print('|---------------|')
        i = 0
        for item in self.__game_field:
            print(f'| {i + 1} | {item[0].symbol_of_gamer} | {item[1].symbol_of_gamer} | {item[2].symbol_of_gamer} |')
            i += 1
        print()

    def __input_main_command(self, command, kind_of_main_command):
        low_command = command
        if not low_command.islower():
            low_command = low_command.lower()
        for _command in self.__main_commands[kind_of_main_command]:
            if low_command == _command:
                return True
        return False   

    def proccessing_input(self, _input):
        if type(_input) == tuple:
            num_row, num_column = _input
        else:
            lower_input_string = _input.lower()
            if self.__input_main_command(lower_input_string, 'exit'):
                self.__is_end = True
                return 'is_end'
            num_row, num_column = self.check_input(lower_input_string)
        self.__game_field[num_row][num_column] = self.__сurrent_gamer
            
    def check_input(self, lower_input_string) -> set:
        list_sub_string = lower_input_string.split(' ')
        if len(list_sub_string) != 2:
            raise ValueError('Ошибка ввода структуры введённой строки (Error entering the structure of the entered string)\n' + TicTacToe.list_of_options())
        num_row = list_sub_string[0]
        num_column = list_sub_string[1]
        list_of_rights = (num_row.isdigit(), num_column.isdigit())
        error_description = TicTacToe.right_error_description(list_of_rights, 
        [
            'Ошибка введённые значения не являются числами (Error the entered values are not numbers)',
            'Ошибка введённое значение первого числа не являются числами (Error the entered value of the first number is not a number)',
            'Ошибка введённое значение второго числа не являются числами (Error the entered value of the second number is not a number)',
        ])    
        
        if error_description != '':
            raise ValueError(error_description + '\n' + TicTacToe.list_of_options())
        num_row = int(num_row)
        num_column = int(num_column)
        lower_limit = 1
        upper_limit = 3
        list_of_rights = (TicTacToe.check_restrictions(num_row, lower_limit, upper_limit), TicTacToe.check_restrictions(num_column, lower_limit, upper_limit))
        error_description = TicTacToe.right_error_description(list_of_rights, 
        [
            f'Ошибка введённые значения {num_row} {num_column} не входят в доступные значения от {lower_limit} до {upper_limit} (Error the entered values {num_row} {num_column} are not included in the available values from {lower_limit} to {upper_limit})',
            f'Ошибка введённое значение первого числа {num_row} не входит в доступные значения от {lower_limit} до {upper_limit} (Error the entered value of the first number {num_row} is not included in the available values from {lower_limit} to {upper_limit})',
            f'Ошибка введённое значение второго числа {num_column} не входит в доступные значения от {lower_limit} до {upper_limit} (Error the entered value of the second number {num_column} is not included in the available values from {lower_limit} to {upper_limit})',
        ])
        if error_description != '':
            raise ValueError(error_description + '\n' + TicTacToe.list_of_options())

        if not self.check_for_hit_in_filled_cell(num_row, num_column):
            raise ValueError(f'Ошибка, клетка {num_row} {num_column} уже заполнена (Error, the cell {num_row} {num_column} is already filled)')
        return num_row - 1, num_column - 1
 
    def check_for_hit_in_filled_cell(self, num_row, num_column):
        return self.__game_field[num_row-1][num_column-1].is_empty_value

    def list_of_options(self) -> str:
        result = '''Возможные значения (Available options):
        1) <номер строки от 1 до 3 (numer of row from 1 to 3)> <номер колонки от 1 до 3 (numer of column from 1 to 3)>
        2) <exit> или (or) <exit()> или (or) <-e> или (or) <-ex> для завершения (for exit)'''
        if not self.__language is None:
            str_or = self.__language.get_string('or')
            result = f'''
            {self.__language.get_string("available_options")}
            1) <{self.__language.get_string("numer_of__from_1_to_3", [self.__language.get_string("of_row")])}> <{self.__language.get_string("numer_of__from_1_to_3", [self.__language.get_string("of_column")])}>
            2) <exit> {str_or} <exit()> {str_or} <-e> {str_or} <-ex> {self.__language.get_string('for_exit')}
            '''
        return result

    @staticmethod
    def right_error_description(list_of_rights, list_errors):
        error_description = ''
        if not list_of_rights[0] and not list_of_rights[1]:
            error_description = list_errors[0]
        elif not list_of_rights[0]:
            error_description = list_errors[1] 
        elif not list_of_rights[1]:
            error_description = list_errors[3]
        return error_description

    @staticmethod
    def check_restrictions(num, lower_limit = 1, upper_limit = 3):
        return num >= lower_limit and num <= upper_limit
 

    @property
    def win_combinations(self):
        return self.__win_combinations

    @property
    def сurrent_gamer(self):
        return self.__сurrent_gamer

    @staticmethod
    def __short_name__():
        return 'TT'