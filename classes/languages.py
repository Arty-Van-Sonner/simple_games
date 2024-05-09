import global_variables as gv

class Languages:
    '''
    This class contains ready-made strings in different languages with keyword access
    '''
    __short_name = ''
    __name = ''
    __language_base = {}
    
    def __init__(self, lang) -> None:
        self.__name = self.get_full_name_lang(lang)
        self.__short_name = lang   
        self.__language_base = {}
        for lang_item in Languages.get_languages_base().items():
            self.__language_base.update({lang_item[0]: lang_item[1][self.__short_name]}) 
   
    def get_full_name_lang(self, lang) -> str:
        lang_data = Languages.get_dict_of_access_languages().get(lang)
        if lang_data is None:
            raise ValueError('Error setting the interface language (Ошибка установки языка интерфейса)!!!')
        return lang_data['full_name'][lang]

    def get_string(self, key_str, upper_lower = ['first_upper']):
        item = self.__language_base.get(key_str)
        if item is None:
            raise ValueError('Error The language element is missing (Ошибка элемент языка отсутствует)!!!')
        return self.get_setting_of_output_text(item, upper_lower)

    def get_string_with_parameters(self, key_str, parameters = None, upper_lower = ['first_upper']):
        string = self.get_string(key_str, upper_lower)
        if type(parameters) == dict:
            string = string.format(**parameters)
        return string

    def get_string_with_editing(self, key_str, list_of_editing, parameters = None, upper_lower = ['first_upper']):
        string = self.get_string(key_str, upper_lower) 
        if list_of_editing is None and parameters is None:
            return string
        if type(list_of_editing) == list:
            string = string.format(*list_of_editing)
        if type(parameters) == dict:
            string = string.format(**parameters)
        return string

    def get_setting_of_output_text(self, string, upper_lower):
        for symbol_case in upper_lower:
            if symbol_case == 'first_upper':
                index_of_letter = None
                i = 0
                for letter in string:
                    if letter.isalpha():
                        index_of_letter = i
                        break
                    i += 1
                if not index_of_letter is None:
                    string = string[:index_of_letter + 1].upper() + string[index_of_letter + 1:]
            elif symbol_case == 'all_first_upper':
                string = string.title()
        return string

    def __str__(self):
        return f'class: <Languages>; current_language: "{self.__name}"; current_language_short: "{self.__short_name}"'

    @staticmethod
    def get_name_of_main_lang() -> str:
        dict_of_access_languages = Languages.get_dict_of_access_languages()
        for lang_key in dict_of_access_languages:
            return dict_of_access_languages[lang_key]['main_lang'] 

    @staticmethod
    def get_dict_of_access_languages() -> dict:
        main_lang = 'en'
        dict_of_access_languages = {
            'ru': {
                'full_name': {
                    'en': 'russien',
                    'ru': 'русский',
                },    
                'main_lang': main_lang,
            }, 
            'en': {
                'full_name': {
                    'en': 'english',
                    'ru': 'английский',
                },
                'main_lang': main_lang,
            }
        }
        return dict_of_access_languages 

    @staticmethod
    def get_languages_base():
        return Languages.code_languages_base()

    @staticmethod
    def code_languages_base() -> dict:
        return {
        'key_string_error': {
            'ru': 'ошибка строка с ключом {} не обнаружена в базе языка',
            'en': 'error the string with the key {} was not found in the language database',
        },
        'menu_of_choose_language': {
            'ru': 'выбирите язык',
            'en': 'select a language',
        },
        'start_menu': {
            'ru': 'начальное меню',
            'en': 'start menu',
        },
        'choosing_game': {
            'ru': 'выбор игры',
            'en': 'choosing game',
        },
        'tic_tac_toe': {
            'ru': 'крестики-нолики',
            'en': 'tic tac toe'
        },
        'battleship': {
            'ru': 'морской бой',
            'en': 'battleship',
        },
        'select_option': {
            'ru': 'выберите опцию',
            'en': 'select an option' 
        },
        'difficulty_level': {
            'ru': 'уровень сложности',
            'en': 'difficulty level',
        },
        'hard': {
            'ru': 'сложно',
            'en': 'hard',
        },
        'medium': {
            'ru': 'средне',
            'en': 'medium',
        },
        'easy': {
            'ru': 'легко',
            'en': 'easy',
        },
        'game_settings': {
            'ru': 'настройки игры',
            'en': 'game settings',
        },
        'list': {
            'ru': 'список',
            'en': 'list',
        },
        'list_of_selection_commands': {
            'ru': 'список команд выбора',
            'en': 'list of selection commands',
        },
        'enter_your_move': {
            'ru': 'введите свой ход:',
            'en': 'enter your move:',
        },
        'enter_your_move_with_parameters': {
            'ru': 'ход компьютера: {}\nВведите свой ход ({}):',
            'en': 'computer move: {}\nEnter your move ({}):',
        },
        'commands_back': {
            'ru': 'команды назад',
            'en': 'commands back',
        },
        'exit_commands': {
            'ru': 'команды выхода',
            'en': 'exit commands',
        },
        'error_of_command_input': {
            'ru': 'ошибка ввода команды',
            'en': 'command input error ',
        },
        'is_not_an_available_value': {
            'ru': 'не является доступным значением',
            'en': 'is not an available value',
        },
        'game_is_over': {
            'ru': 'игра окончена',
            'en': 'the game is over',
        },
        'there_are_no_free_cells_left': {
            'ru': 'не осталось свободных клеток',
            'en': 'there are no free cells left',
        },
        'you_lose': {
            'ru': 'вы проиграли',
            'en': 'you lose',
        },
        'congratulations_you_have_won': {
            'ru': 'поздравляю вы выиграли',
            'en': 'congratulations you have won',
        },
         'error_the_entered_values_are_not_numbers': {
            'ru': 'ошибка введённые значения не являются числами',
            'en': 'error the entered values are not numbers',
        },
        'error_entered_value_of_first_number_is_not_number': {
            'ru': 'ошибка введённое значение первого числа не являются числами',
            'en': 'error the entered value of the first number is not a number',
        },
        'error_entered_value_of_second_number_is_not_number': {
            'ru': 'ошибка введённое значение второго числа не являются числами',
            'en': 'error the entered value of the second number is not a number',
        },
        'error_entered_values_num_row_num_column_are_not_included_in_available_values_from_lower_limit_to_upper_limit': {
            'ru': 'ошибка введённые значения {num_row} {num_column} не входят в доступные значения от {lower_limit} до {upper_limit}',
            'en': 'error the entered values {num_row} {num_column} are not included in the available values from {lower_limit} to {upper_limit}',
        },
        'error_entered_value_of_first_number_num_row_num_column_is_not_included_in_available_values_from_lower_limit_to_upper_limit': {
            'ru': 'ошибка введённое значение первого числа {num_row} не входит в доступные значения от {lower_limit} до {upper_limit}',
            'en': 'error the entered value of the first number {num_row} is not included in the available values from {lower_limit} to {upper_limit}',
        },
        'error_entered_value_of_second_number_num_column_is_not_included_in_available_values_from_lower_limit_to_upper_limit': {
            'ru': 'ошибка введённое значение второго числа {num_column} не входит в доступные значения от {lower_limit} до {upper_limit}',
            'en': 'error the entered value of the second number {num_column} is not included in the available values from {lower_limit} to {upper_limit}',
        },
        'error_cell_num_row_num_column_is_already_filled': {
            'ru': 'ошибка, клетка {num_row} {num_column} уже заполнена',
            'en': 'error, the cell {num_row} {num_column} is already filled',
        },
        'available_options': {
            'ru': 'возможные значения',
            'en': 'available options',
        },
        'numer_of_axis_from_min_to_max': {
            'ru': 'номер {axis} от {min} до {max}',
            'en': 'numer {axis} from {min} to {max}',
        },
        'of_row': {
            'ru': 'строки',
            'en': 'of row',
        },
        'of_column': {
            'ru': 'колонки',
            'en': 'of column',
        },
        'or': {
            'ru': 'или',
            'en': 'or',
        },
        'for_exit': {
            'ru': 'для завершения',
            'en': 'for exit',
        },
        'select_starting_cell_of_ship': {
            'ru': 'выберите стартовую клеточку корабля «{}»',
            'en': 'select the starting cell of the ship "{}"',
        },
        'select_cell': {
            'ru': 'выберите клеточку',
            'en': 'select the cell',
        },
        'error_passing_dict_of_options_parameter': {
            'ru': 'ошибка при передаче параметра dict_of_options, обратитесь к администратору',
            'en': 'error passing the dict_of_options parameter, contact the administrator',
        },
        'error_entering_structure_of_entered_string': {
            'ru': 'ошибка ввода структуры введённой строки',
            'en': 'error entering the structure of the entered string',
        },
        'battleship': {
            'ru': '«четырёхпалубный»; линкор',
            'en': 'battleship',
        },
        'cruiser': {
            'ru': '«трёхпалубные»; крейсера',
            'en': 'cruiser',
        },
        'destroyer': {
            'ru': '«двухпалубные»; эсминцы',
            'en': 'destroyer',
        },
        'torpedo_boat': {
            'ru': '«однопалубные»; торпедные катера',
            'en': 'torpedo boat',
        },
        'error_setting_size_by_x_y_axis': {
            'ru': 'ошибка задания размерности поля через оси x и y. Данная функция пока не реализована',
            'en': 'error in setting the dimension of the field through the x and y axes. This feature has not been implemented yet',
        },
        'error_setting_size_size_is_over': {
            'ru': 'ошибка установки размера поля. Размеры поля выходят за стандартно возможных',
            'en': 'error setting size. Size is over',
        },
        'error_when_checking_correct_location_of_ship': {
            'ru': 'ошибка при проверке возможность расположения корабля',
            'en': 'error when checking correct location of ship',
        },
        'error_setting_size_by_x__x_is_below_zero': {
            'ru': 'Ошибка значения x. x меньше нуля',
            'en': 'error setting size by x. x is below zero',
        },
        'error_setting_size_by_y__y_is_below_zero': {
            'ru': 'Ошибка значения y. y меньше нуля',
            'en': 'error setting size by y. y is below zero',
        },
        'error_setting_size_by_x__x_is_over_size': {
            'ru': 'Ошибка значения x. x выходи за границы поля',
            'en': 'error setting size by x. x is over size',
        },
        'error_setting_size_by_y__y_is_over_size': {
            'ru': 'Ошибка значения y. y выходи за границы поля',
            'en': 'error setting size by y. y is over size',
        },
        'was_error_when_check_out_of_field': {
            'ru': 'ошибки при проверке координат x y на попадание в пределы игрового поля',
            'en': 'error when checking out of field',
        },
        'error_setting_value_of_ship_cell__cell_is_occupied_by_another_ship': {
            'ru': 'ошибка установки корабля. Клетка занята другим кораблём',
            'en': 'error setting value of ship cell. The cell is occupied by another ship',
        },
        'error_setting_value_of_ship_cell__cell_is_buffer_by_another_ship': {
            'ru': 'ошибка установки корабля. Клетка буферная с другим кораблём',
            'en': 'error setting value of ship cell. The cell is buffer by another ship',
        },
        'error_when_check_value_of_ship_owner__ship_owner_is_None': {
            'ru': 'ошибка проверки значения владельца корабля. Параметр Ship owner в значение None',
            'en': 'error when check value of ship owner. Ship owner is None',
        },
        'error_when_check_value_of_ship_owner__ship_owner_is_not_correct_type': {
            'ru': 'ошибка проверки значения владельца корабля. Параметр Ship owner передан не корректного типа',
            'en': 'error when check value of ship owner. Ship owner is not correct type',
        },
        'error_when_reflect_hit__cell_is_hit_already': {
            'ru': 'ошибка при попытки выстрела по клетке. Клетка уже была атакована ранее',
            'en': 'error when reflect hit. The cell is hit already',
        },
        'error_when_set_occupied_cell_in_ship_is_destroyed__cell_is_not_buffer_by_another_ship': {
            'ru': 'ошибка при попытке устаноки клетки в значение "корабль уничтожен". Клетка не является буферной клеткой для кораблей',
            'en': 'error when setting occupied cell in ship is destroyed. The cell is not buffer by another ship',
        },
        'error_when_get_ai_move__сurrent_game_is_not_correct_type': {
            'ru': 'ошибка при получение координат хода. Текущая игра имеет не правильный тип',
            'en': 'error when get ai move. Current game is not correct type',
        },
        'error_when_adding_message__message_is_not_correct_type': {
            'ru': 'ошибка при добавление сообщения. Сообщение имеет не правильный тип данных',
            'en': 'error when adding message. Message is not correct type',
        },
        'ship_is_destroyed': {
            'ru': 'сообщение: {ship} игрока {nickname} уничтожен',
            'en': 'message: {ship} of {nickname} is destroyed',
        },
        'error_when_reflect_hit__cell_belongs_destroyed_ship': {
            'ru': 'ошибка при попытки выстрела по клетке. Клетка принадлежит уничтоженному кораблю',
            'en': 'error when reflect hit. The cell to the belongs destroyed ship',
        },
        'or': {
            'ru': 'или',
            'en': 'or',
        },
        'or': {
            'ru': 'или',
            'en': 'or',
        },
    }

    @staticmethod
    def __short_name__():
        return 'LG'