import global_variables as gv

class Cells:
    '''
    
    '''
    __x = 0
    __y = 0
    __value = None
    def __init__(self, x, y, value = None) -> None:
        global interface
        from value_of_cell import ValueOfCell
        list_of_available_types = []
        list_of_available_types.append(ValueOfCell)
        self.__x = x
        self.__y = y
        if value is None:
            self.__value = ValueOfCell(self)
        else:
            self.__value = value

    @property
    def value(self):
        return self.__value

    @property
    def coordinates(self):
        return self.__x, self.__y

    def __len__(self):
        return len(self.__value.max_len_symbol)

    @staticmethod
    def __short_name__():
        return 'Ce'