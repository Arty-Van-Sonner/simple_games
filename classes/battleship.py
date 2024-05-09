from games import Games
from gamers import Gamers
import global_variables as gv
from random import randint
from ships import Ships
from ai import AI
from game_fields import GameFields
import copy

class Battleship(Games):
    '''
    
    '''
    __difficulty_level = 1
    __list_of_gamers_and_field_of_gamers = []
    __settings = None
    __game_in_process = True
    __сurrent_index_of_gamer = 0
    __main_commands = {}
    __number_of_move = 0
    def __init__(self):
        self.set_settings()
        self.__main_commands = {}
        self.__list_of_gamers_and_field_of_gamers = []
        self.__game_in_process = True
        self.__number_of_move = 0
        self.__сurrent_index_of_gamer = 0
        user_field = GameFields(self.__settings['size_of_field']['value'])
        computer_field = GameFields(self.__settings['size_of_field']['value'])
        # user_ships = user_field.list_of_ships
        # computer_ships = computer_field.list_of_ships
        self.__list_of_gamers_and_field_of_gamers.append(
            Battleship.get_dict_of_gamers_and_field_of_gamers(
                Gamers('you', 'user'),
                user_field,
                # user_ships,
            )
        )
        ai = AI(self)
        self.__list_of_gamers_and_field_of_gamers.append(
            Battleship.get_dict_of_gamers_and_field_of_gamers(
                Gamers('computer', 'computer', 'X', ai),
                computer_field,
                # computer_ships,
            )
        )
        self.__main_commands = {
            'exit': ['-ex', 'exit', 'exit()'],
            'back': ['-bk', 'back', 'back()']
        }
        
    def __fill_feild_of_ships_automatoc(self):
        for dict_of_gamer in self.__list_of_gamers_and_field_of_gamers:
                dict_of_gamer['gamer_ships'] = self._fill_feild_of_ships(dict_of_gamer['game_field'])

    def start_game(self):
        # self.test_show()
        self.__fill_feild_of_ships_automatoc()
        while self.__game_in_process:
            # self.show()
            try:
                self.show()
            except ValueError as ve:
                pass

    def show(self):
        self.__show_only_for_in_console()

    def __show_only_for_in_console(self):
        gamer_and_gamer_field = self.__list_of_gamers_and_field_of_gamers[self.__сurrent_index_of_gamer]
        gamer = Battleship.get_gamer(gamer_and_gamer_field)
        lang = gv.interface.current_language
        if gamer.is_computer:
            index_of_opponent = self.__index_next_gamer(self.__сurrent_index_of_gamer)
            game_field_of_opponent = self.__list_of_gamers_and_field_of_gamers[index_of_opponent]
            move = gamer.get_ai_move(game_field_of_opponent)
            gv.computer_move = (move[0] + 1, move[1] + 1)
            self.__proccessing_input(move)
        else:
            self.output()
            try:
                gv.interface.messages_storage.show_all()
            except BaseException as be:
                print(be)
            input_string = input(lang.get_string_with_editing('enter_your_move_with_parameters', [gv.computer_move, f'{lang.get_string("exit_commands")} {self.__main_commands["exit"]}']))
            self.__proccessing_input(input_string)
        if self.__announce_winner_and_end_game(self.__get_winner_index()):
            return
        self.__сurrent_index_of_gamer = self.__get_next_gamer_index(self.__сurrent_index_of_gamer)

    def __proccessing_input(self, _input):
        if type(_input) == tuple:
            num_row, num_column = _input
        else:
            lower_input_string = _input.lower()
            if self.__input_main_command(lower_input_string, 'exit'):
                self.__game_in_process = False
                return 'is_end'
            num_row, num_column = self.__check_input(lower_input_string)
        index_of_opponent = self.__index_next_gamer(self.__сurrent_index_of_gamer)
        game_field_of_opponent = self.__list_of_gamers_and_field_of_gamers[index_of_opponent]
        opponent_game_field = game_field_of_opponent['game_field']
        opponent_game_field.reflect_hit(num_row, num_column, game_field_of_opponent['gamer'])

    def __input_main_command(self, command, kind_of_main_command):
        low_command = command
        if not low_command.islower():
            low_command = low_command.lower()
        for _command in self.__main_commands[kind_of_main_command]:
            if low_command == _command:
                return True
        return False

    def __check_input(self, lower_input_string) -> set:
        list_sub_string = lower_input_string.split(' ')
        if len(list_sub_string) != 2:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(Battleship, '__check_input', {
                'error_name': 'error_entering_structure_of_entered_string',
                'end_adding': f'\n{str(self.list_of_options())}',
                }, '01', 3, True))
        num_row = list_sub_string[0]
        num_column = list_sub_string[1]
        list_of_rights = (num_row.isdigit(), num_column.isdigit())
        error_description = Battleship.right_error_description(list_of_rights, 
        [
            'error_the_entered_values_are_not_numbers',
            'error_entered_value_of_first_number_is_not_number',
            'error_entered_value_of_second_number_is_not_number',
        ])
        if error_description != '':
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(Battleship, '__check_input', {
                'error_name': error_description,
                'end_adding': f'\n{str(self.list_of_options())}',
                }, '02', 3, True, True))
        num_row = int(num_row)
        num_column = int(num_column)
        return num_row - 1, num_column - 1

    def _reduce_health_to_opponent(self, ship):
        index_of_opponent = self.__index_next_gamer(self.__сurrent_index_of_gamer)
        game_field_of_opponent = self.__list_of_gamers_and_field_of_gamers[index_of_opponent]
        game_field_of_opponent['life_points'] -= 1 

    def output(self):
        self.test_show()

    def __get_winner_index(self):
        index = 0
        for gamer_and_gamer_field in self.__list_of_gamers_and_field_of_gamers:
            if Battleship.get_life_points(gamer_and_gamer_field) <= 0:
                return self.__index_next_gamer(index)
            index += 1
        return None

    def __announce_winner_and_end_game(self, winner_index):
        if winner_index is None:
            return False
        dict_of_gamer = self.__list_of_gamers_and_field_of_gamers[winner_index]
        winner = dict_of_gamer['gamer']
        result = False
        final_message = ''
        language = gv.interface.current_language
        if winner.is_computer:
            final_message = f'\n{language.get_string("you_lose")}!\n'
            result = True
        else:
            final_message = f'\n{language.get_string("congratulations_you_have_won")}!\n'
            result = True
        if result:
            self.__game_in_process = False
            self.output()
            print(final_message)    
        return result

    def __get_next_gamer_index(self, сurrent_index) -> None:
        self.__number_of_move += 1
        return self.__index_next_gamer(сurrent_index)

    def __index_next_gamer(self, сurrent_index) -> int:
        if сurrent_index >= len(self.__list_of_gamers_and_field_of_gamers) - 1:
            сurrent_index = 0
        else:
            сurrent_index += 1
        return сurrent_index

    def test_show(self): # test output
        from interface import Interface
        language = gv.interface.current_language
        title = language.get_string('battleship')
        text = []
        for dict_of_gamer in self.__list_of_gamers_and_field_of_gamers:
            text.append({
                'title': dict_of_gamer['gamer'].nickname,
                'value': dict_of_gamer['game_field'],
                'hidden': dict_of_gamer['gamer'].is_hidden
            }) 
        string_for_input = language.get_string('select_option')
        answer = gv.interface.ask_question_to_user(title, text, string_for_input, [], [], False, 'column')

    def set_settings(self):
        if self.__settings is None:
            self.__settings = Battleship.get_standart_settings()

    def _fill_feild_of_ships(self, game_field, automatic = True):
        list_of_created_ships = []
        in_progress = True
        countble = 0
        while in_progress:
            life_points = self.__settings['life_points']['value']
            dict_of_access_counts_of_ships = copy.deepcopy(self.__settings['dict_of_access_counts_of_ships']['value'])
            for key in dict_of_access_counts_of_ships:
                if dict_of_access_counts_of_ships[key]['count'] > 0:
                    for i in range(dict_of_access_counts_of_ships[key]['count']):
                        list_of_ships_parameters = game_field._get_access_values_for_location_ship(dict_of_access_counts_of_ships[key], not automatic)
                        # print(f'list_of_ships_parameters: {list_of_ships_parameters}')
                        if len(list_of_ships_parameters) == 0:
                            game_field._fill_temporary_storage()
                            break 
                        try:
                            index_of_element = None
                            if automatic:
                                index_of_element = randint(0, len(list_of_ships_parameters) - 1)
                            else:
                                language = gv.interface.current_language
                                name_of_ship = language.get_string('key')
                                title = language.get_string('select_starting_cell_of_ship', [name_of_ship])
                                string_for_input = language.get_string('select_cell')
                                index_of_element = gv.interface.ask_question_to_user(title, game_field, string_for_input, list_of_ships_parameters, ['start_x', 'start_y'], True)
                            ship = Ships(**list_of_ships_parameters[index_of_element])
                            list_of_created_ships.append(ship)
                            dict_of_access_counts_of_ships[key]['count'] -= 1
                            life_points -= dict_of_access_counts_of_ships[key]['size']
                            
                            #NFC + Тестовый код
                            # test_list = []
                            # for x in game_field.get_field_as():
                            #     sub_test_list = []
                            #     for y in x:
                            #         sub_test_list.append(y.value.is_ship_cell_value)#get_symbol(False))    
                            #     test_list.append(sub_test_list)
                            # print(f'\n{test_list}\n')
                            #NFC -
                        except BaseException():
                            pass
            countble += 1
            if life_points <= 0:
                in_progress = False
                game_field._move_field_from_temporary_storage_for_ships_in_main_storge()
        return list_of_created_ships

    def list_of_options(self) -> str:
        lang = gv.interface.current_language
        min_size = 1
        max_size = self.__settings['size_of_field']['value']
        of_row = lang.get_string('of_row')
        of_column = lang.get_string('of_column')
        str_or = lang.get_string('or')
        result = f'''{lang.get_string('available_options')}:
        1) <{lang.get_string_with_parameters(
            'numer_of_axis_from_min_to_max',
            {
                'axis': of_row,
                'min': min_size,
                'max': max_size,
            }
        )}> <{lang.get_string_with_parameters(
            'numer_of_axis_from_min_to_max',
            {
                'axis': of_column,
                'min': min_size,
                'max': max_size,
            }
        )}>
        2) <exit> {str_or} <exit()> {str_or} <-e> {str_or} <-ex> {lang.get_string('for_exit')}'''
        return result

    @property
    def game_in_process(self):
        return self.__game_in_process

    @staticmethod
    def get_gamer(gamer_and_gamer_field):
        return gamer_and_gamer_field['gamer']

    @staticmethod
    def get_game_field(gamer_and_gamer_field):
        return gamer_and_gamer_field['game_field']

    @staticmethod
    def get_life_points(gamer_and_gamer_field):
        return gamer_and_gamer_field['life_points']

    @staticmethod
    def get_dict_of_gamers_and_field_of_gamers(gamer, game_field, gamer_ships = None, life_points = 3 + 4 + 4):
        return {
            'gamer': gamer,
            'game_field': game_field,
            'gamer_ships': gamer_ships,
            'life_points': life_points,
        }

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
    def get_standart_settings():
        name_value = 'value'
        name_options = 'options'
        name_user_setting = 'user_setting'
        name_dependents = 'dependents'
        size_of_field = 6
        list_of_size_options = list(range(6, 11))
        return {
            'size_of_field': {
                name_value: size_of_field,
                name_options: list_of_size_options,
                name_user_setting: True,
                name_dependents: ['life_points', 'dict_of_access_counts_of_ships'],
            },
            'life_points': {
                name_value: 11,
                name_options: list(range(11, 21)),
                name_user_setting: False,
                name_dependents: [],
            },
            'dict_of_access_counts_of_ships': {
                name_value: Battleship.get_dict_of_access_counts_of_ships(size_of_field),
                name_options: list_of_size_options,
                name_user_setting: False,
                name_dependents: [],
            },
            'field_generation': {
                name_value: 'automatic',
                name_options: [{'manual', 'manual'}, {'-m', 'manual'}, {'-a', 'automatic'}, {'automatic', 'automatic'}],
                name_user_setting: True,
                name_dependents: [],
            },
        }

    @staticmethod
    def get_dict_of_access_counts_of_ships(size):
        '''
        Размещаются 10x10:
            1 корабль — ряд из 4 клеток («четырёхпалубный»; линкор)
            2 корабля — ряд из 3 клеток («трёхпалубные»; крейсера)
            3 корабля — ряд из 2 клеток («двухпалубные»; эсминцы)
            4 корабля — 1 клетка («однопалубные»; торпедные катера)
        Размещаются 6x6:
            1 корабль на 3 клетки;
            2 корабля на 2 клетки;
            4 корабля на одну клетку.

                             4    3    2    1
            10	20	0       4x1, 3x2, 2x3, 1x4
            9	1	19      0x1, 3x3, 2x3, 1x4
            8	3	16      0x1, 3x2, 2x3, 1x4
            7	3	13      0x1, 3x1, 2x3, 1x4
            6	2	11      0x1, 3x1, 2x2, 1x4
        '''
        count_of_battleships = 1 if size == 10 else 0
        count_of_cruisers = 2 if size == 10 else 1 if size == 6 else size - 6
        count_of_destroyers = 2 if size == 6 else 3
        count_of_torpedo_boats = 4
        dict_of_access_counts_of_ships = {
            'battleships': {
                'size': 4,
                'count': count_of_battleships,
            },
            'cruisers': {
                'size': 3,
                'count': count_of_cruisers,
            },
            'submarines': {
                'size': 2,
                'count': count_of_destroyers,
            }, 
            'torpedo_boats': {
                'size': 1,
                'count': count_of_torpedo_boats,
            },
        }
        return dict_of_access_counts_of_ships

    @staticmethod
    def __short_name__():
        return 'BS'