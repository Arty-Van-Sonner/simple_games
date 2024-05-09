import global_variables as gv
from empty_value import EmptyValue as EmptyValue_For_ValueOfCell

class ValueOfCell(EmptyValue_For_ValueOfCell):
    '''
    
    '''
    __is_empty_value = True
    __occupied_cell = False
    __occupied_hit_cell = False
    __ship_owners = []
    __hit = False
    __is_ship_cell_value = False
    __cell = None
    __occupied_cell_ship_is_destroyed = None
    def __init__(self, cell) -> None:
        self.__hit = False
        self.__is_ship_cell_value = False
        self.__occupied_cell = False
        self.__occupied_cell_ship_is_destroyed = False
        self.__occupied_hit_cell = False
        self.__is_empty_value = True
        self.__cell = cell
        self.__ship_owners = []
        self.__set_symbol(self.__get_symbol())

    def set_value_of_ship_cell(self, ship_owner):
        self.__check_value_of_ship_owner_and_add_ship_in_ship_owners(ship_owner)
        self.__is_ship_cell_value = True
        self.__is_empty_value = False
        self.__set_symbol(self.__get_symbol())

    def check_possible_to_set_value_of_ship_cell(self, raise_error = True, show_user = False) -> None:
        if self.__is_ship_cell_value:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, 'check_possible_to_set_value_of_ship_cell', 'error_setting_value_of_ship_cell__cell_is_occupied_by_another_ship', '01', 3, True, show_user = show_user))
        elif self.__occupied_cell:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, 'check_possible_to_set_value_of_ship_cell', 'error_setting_value_of_ship_cell__cell_is_buffer_by_another_ship', '02', 3, True, show_user = show_user))

    def set_value_of_ship_occupied_cell(self, ship_owner):
        self.__check_value_of_ship_owner_and_add_ship_in_ship_owners(ship_owner)
        self.__occupied_cell = True   
        self.__set_symbol(self.__get_symbol())

    def __check_value_of_ship_owner_and_add_ship_in_ship_owners(self, ship_owner) -> bool:
        self.__check_value_of_ship_owner(ship_owner)
        return self.__add_ship_in_ship_owners(ship_owner)

    def __check_value_of_ship_owner(self, ship_owner): 
        from ships import Ships  
        if ship_owner is None:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, '__check_value_of_ship_owner', 'error_when_check_value_of_ship_owner__ship_owner_is_None', '03', 3, True)) 
        if not type(ship_owner) is Ships:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, '__check_value_of_ship_owner', 'error_when_check_value_of_ship_owner__ship_owner_is_not_correct_type', '04', 3, True))

    def __add_ship_in_ship_owners(self, ship_owner) -> bool:
        if not ship_owner in self.__ship_owners:
            self.__ship_owners.append(ship_owner) 
            return True
        return False 

    def __set_symbol(self, symbol):
        super()._set_symbol(symbol)

    def reflect_hit(self, gamer):
        was_error = False
        if self.__occupied_cell_ship_is_destroyed:
            was_error = True
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, 'reflect_hit', 'error_when_reflect_hit__cell_belongs_destroyed_ship', '05', 3, False))
        if self.__hit:
            was_error = True
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, 'reflect_hit', 'error_when_reflect_hit__cell_is_hit_already', '06', 3, False))
        if self.__occupied_hit_cell:
            was_error = True
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, 'reflect_hit', 'error_when_reflect_hit__cell_is_hit_already', '07', 3, False)) 
        if was_error:
            raise ValueError('reflect_hit, was error')
        self.__hit = True
        self.__set_symbol(self.__get_symbol())
        if self.__is_ship_cell_value:
            self.__ship_owners[0].reflect_hit(*self.__cell.coordinates, gamer)

    def __get_symbol(self):
        dict_of_symbols = ValueOfCell.get_dict_of_symbols()
        state = ''
        if self.__occupied_cell_ship_is_destroyed:
            state = 'ship_is_destroyed'
        elif self.__hit:
            state = 'hit'
        else: 
            state = 'unharmed'
        _type = ''
        if self.__is_ship_cell_value:
            _type = 'ship_cell'
        elif self.__occupied_cell:
            if self.__occupied_cell_ship_is_destroyed and self.__hit:
                _type = 'hif_occupied_cell'
            else:
                _type = 'occupied_cell'
        else:
            _type = 'empty_value'
        return dict_of_symbols[state][_type]

    def _add_ship_owner(self, ship_owner):
        self.__ship_owners.append(ship_owner)

    def get_symbol(self, hidden):
        if self.__hit or not hidden or self.__occupied_cell_ship_is_destroyed:
            return super().symbol
        else: 
            return ValueOfCell.get_dict_of_symbols()['unharmed']['empty_value']

    def set_occupied_cell_in_ship_is_destroyed(self, ship):
        if not self.__occupied_cell:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(ValueOfCell, 'set_occupied_cell_in_ship_is_destroyed', 'error_when_set_occupied_cell_in_ship_is_destroyed__cell_is_not_buffer_by_another_ship', '08', 3, True))
        self.__occupied_cell_ship_is_destroyed = True
        self.__set_symbol(self.__get_symbol())

    @property
    def max_len_symbol(self):
        if len(super().symbol) > len(ValueOfCell.get_dict_of_symbols()['unharmed']['empty_value']):
            return super().symbol
        else:
            return ValueOfCell.get_dict_of_symbols()['unharmed']['empty_value']

    @property
    def is_free_cell(self):
        return not self.occupied_cell_ship_is_destroyed and not self.__hit

    @property
    def is_hit(self):
        return self.__hit

    @property
    def is_empty_value(self):
        return self.__is_empty_value

    @property
    def is_ship_cell_value(self):
        return self.__is_ship_cell_value

    @property
    def occupied_cell(self):
        return self.__occupied_cell

    @property
    def occupied_cell_ship_is_destroyed(self):
        return self.__occupied_cell_ship_is_destroyed

    @property
    def ship_owners(self):
        return self.__ship_owners

    @staticmethod
    def get_dict_of_symbols():
        return {
            'hit': {
                'empty_value': 'T',
                'occupied_cell': 'T',
                'ship_cell': 'X',
            },
            'unharmed': {
                'empty_value': '0',
                'occupied_cell': '0',
                'ship_cell': '■',
            },
            'ship_is_destroyed': {
                'empty_value': None,
                'occupied_cell': '+',
                'hif_occupied_cell': '×',
                'ship_cell': 'X',
            },
        }

    @staticmethod
    def __short_name__():
        return 'VC'