import global_variables as gv

class Interface:
    '''
    
    '''
    __current_environment = None
    __current_language = None
    __error_list = []
    __current_game = None
    __messages_storage = None
    def __init__(self, current_environment) -> None:
        from message_storage import MessageStorage
        self.__current_environment = current_environment
        self.__messages_storage = MessageStorage()
        self.__set_language() 
        self.__set_game()

    def start_game(self):
        self.__current_game.set_settings()
        self.__current_game.start_game()      

    def __set_language(self):
        from languages import Languages
        main_lang = Languages.get_name_of_main_lang()
        self.__current_language = Languages(main_lang)

    def __set_game(self):
        from battleship import Battleship
        self.__current_game = Battleship() #NFC

    def add_and_raise_error(self, text, group, status, error_code, error_type, raise_error = True, show_user = True, show_right_now = False):
        self.__add_error_to_messages_storage(self.__create_error(text, group, status, error_code, error_type, show_user, show_right_now))
        if raise_error:
            raise error_type(text)
        
    def add_message(self, text, show_user):
        self.__add_message_to_messages_storage(self.__create_message(text, show_user))
    
    def __add_message_to_messages_storage(self, messages):
        # self.__error_list.append(error)
        self.messages_storage.add_message(messages)

    def __add_error_to_messages_storage(self, error):
        # self.__error_list.append(error)
        self.messages_storage.add_error(error)

    def __create_message(self, text, show_user):
        from messages import Messages
        return Messages(self.messages_storage, '', text, show_user)

    def __create_error(self, text, group, status, error_code, error_type, show_user, show_right_now):
        # return {
        #     'text': text,
        #     'group': group,
        #     'status': self.__get_error_status(status),
        #     'error_code': error_code,
        #     'error_type': error_type,
        #     'show_user': show_user,
        #     'show_right_now': show_right_now,
        # }
        from messages import Messages
        return Messages(self.messages_storage, '', text, show_user, show_right_now, group = group, status = status, error_code = error_code, _type = error_type, is_error = True)

    def __get_error_status(self, status_code) -> str:
        '''
        
        '''
        list_of_statuses = []
        list_of_statuses.append('information')
        list_of_statuses.append('note')
        list_of_statuses.append('warning')
        list_of_statuses.append('error')
        status_code = 0 if status_code < 0 else len(list_of_statuses) - 1 if status_code >= len(list_of_statuses) else status_code
        return list_of_statuses[status_code]

    def __fill_feild_of_ships_automatic(self):
        self.__current_game._fill_feild_of_ships_automatic()

    def output_message(self, message):
        self.__current_environment.output_message(message)

    def ask_question_to_user(self, title, value, string_for_input, list_of_parametrs, list_of_use_parametrs, return_index, row_column = 'row'):
        text = None
        list_of_options = []
        if type(value) == list:
            text = []
            for element in value:
                text.append(self.get_text_from_value(element, hidden = element['hidden']))
        return self.__current_environment.ask_question_to_user(self.get_standart_message(title, text, string_for_input, list_of_options, row_column))

    def get_text_from_value(self, value, title = '', row_column = 'row', hidden = False):
        from game_fields import GameFields
        if type(value) == GameFields:
            return self.get_standart_table_in_message(title, value.get_field_as(), value.column_titles, value.row_titles, hidden)
        elif type(value) == dict:
            return self.get_text_from_value(value['value'], value['title'], hidden = hidden) 
        elif type(value) == list:
            return self.get_standart_list_in_message(title)

    def __get_ready_tabel_for_output(self):
        pass

    def get_standard_dict_of_error(self, _class, method_name, error, error_code, status, raise_error = True, show_user = True, show_right_now = False, error_type = ValueError):
        lang = gv.interface.current_language 
        text = '' 
        error_name = ''
        if type(error) == str:
            error_name = error
            text = lang.get_string(error_name)
        elif type(error) == dict:
            error_name = error['error_name']
            error_parameters = error.get('error_parameters')
            upper_lower = error.get('upper_lower')
            if upper_lower is None:
                upper_lower = ['first_upper']
            if error_parameters is None:
                text = lang.get_string(error_name) 
            else:
                if type(error_parameters) == dict:
                    text = lang.get_string_with_parameters(error_name, error_parameters, upper_lower)
                else:
                    text = lang.get_string_with_parameters(error_name, error_parameters, upper_lower = upper_lower)
            begin_adding = error.get('begin_adding', '')
            end_adding = error.get('end_adding', '')
            text = begin_adding + text + end_adding
        group = f'{_class.__name__}.{method_name}.{error_name}'
        status = status
        error_code = f'err{_class.__short_name__()}{error_code}'
        return {
            'text': text,
            'group': group,
            'status': status,
            'error_code': error_code,
            'error_type': error_type,
            'raise_error': raise_error,
            'show_user': show_user,
            'show_right_now': show_right_now,
        }

    def get_standart_message(self, title, value, string_for_input, list_of_options, row_column = 'row'):
        dict_of_message= {
            'type': 'message',
            'title': title,
            'value': value,
            'list_of_options': list_of_options,
            'string_for_input': string_for_input,
            'row_column': row_column,
        }
        return dict_of_message

    def get_standart_table_in_message(self, title, table_as_list, title_of_columns = None, title_of_rows = None, hidden = False):
        dict_of_table= {
            'type': 'table',
            'title': title,
            'value': table_as_list,
            'title_of_columns': title_of_columns,
            'title_of_rows': title_of_rows,
            'hidden': hidden,
        }
        return dict_of_table

    def get_standart_list_in_message(self, title, standart_list, title_of_columns = None, title_of_rows = None, start_number = None, hidden = True):
        dict_of_list= {
            'type': 'list',
            'title': title,
            'value': standart_list,
            'title_of_columns': title_of_columns,
            'title_of_rows': title_of_rows,
            'start_number': start_number,
            'hidden': hidden,
        }
        return dict_of_list

    def get_standart_text_in_message(self, title, standart_text, title_of_columns = None, title_of_rows = None, start_number = None, hidden = True):
        dict_of_list= {
            'type': 'text',
            'title': title,
            'value': standart_text,
            'title_of_columns': title_of_columns,
            'title_of_rows': title_of_rows,
            'start_number': start_number,
            'hidden': hidden,
        }
        return dict_of_list

    @property
    def current_language(self):
        return self.__current_language

    @property
    def current_game(self):
        return self.__current_game

    @property
    def messages_storage(self):
        return self.__messages_storage

    @property
    def current_environment(self):
        return self.__current_environment

    @staticmethod
    def get_code_of_error():
        return Interface.get_code_of_error_from_code()

    @staticmethod
    def get_code_of_error_from_code(_class, inner_code):
        from ai import AI
        from battleship import Battleship
        from cell_storage import AI
        return '0000'

    @staticmethod
    def __short_name__():
        return 'IF'