import global_variables as gv
from empty_value import EmptyValue

class Gamers(EmptyValue):
    '''
    The Gamers class is designed to solve the tasks of save and return information about gamer:
    1. contain:
        1.1. nickname
        1.2. type of gamer
        1.3. reference to AI if gamer is computer 
        1.4. mark "is computer" identifies it is computer
    2. the actions:    
        2.1. starting fill of class
        2.2. requesting to next move from AI if it is computer 
        2.3. returning importent values for game
        2.4. setting difficulty level for AI

    Fields:
        __nickname - str (string) - this is nickname of gamer
        __type - str (string) - this is gamer type. Available values: user, computer
        __ai - int (integer) - this is reference to AI if gamer is computer
        __is_computer - list - this is mark identifies that it is computer
        __symbol_of_gamer - str (string) - this is symbol of cells of the gamer on field
    '''
    __nickname = ''
    __type = ''
    __ai = None
    __is_computer = None
    __symbol_of_gamer = ''
    def __init__(self, nickname, _type, symbol_of_gamer = None, ai = None):
        self.__nickname = nickname
        self.__type = _type
        self.__symbol_of_gamer = symbol_of_gamer
        self.__ai = ai
        self.__is_computer = self.__type == 'computer'

    def get_ai_move(self, data_dict):
        return self.__ai.get_ai_move(data_dict)

    @property
    def symbol_of_gamer(self):
        return self.__symbol_of_gamer

    @property
    def is_empty_value(self):
        return False

    @property
    def is_computer(self):
        return self.__is_computer

    @property
    def nickname(self):
        return self.__nickname

    @property
    def is_hidden(self):
        return self.__is_computer and gv.interface.current_game.game_in_process

    def set_difficulty_level(self, value):
        if self.__ai is None:
            return self.__ai.set_difficulty_level(value)

    @staticmethod
    def __short_name__():
        return 'GR'