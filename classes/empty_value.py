import global_variables as gv

class EmptyValue:
    '''
    The EmptyValue class is designed to slove indicate empty cells of game field:
    1. contain:
        1.1. symbol of the empty cells of game field
    2. the actions:
        2.1. starting fill of class
        2.2. returning symbol of the empty cell(s) and is empty value as True

    Fields:
        __symbol - str (string) - this is empty symbol of cells of game field
    '''
    __symbol = '-'
    def __init__(self, __symbol = '-'):
        self._set_symbol(__symbol)

    def _set_symbol(self, symbol):
        self.__symbol = symbol
    
    @property
    def symbol_of_gamer(self):
        return self.__symbol
    @property
    def is_empty_value(self):
        return True
    @property
    def symbol(self):
        return self.__symbol

    @staticmethod
    def __short_name__():
        return 'EV'