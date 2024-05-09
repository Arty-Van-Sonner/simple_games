import global_variables as gv
from empty_value import EmptyValue as EmptyValue_For_ShipValuesOfCell

class ShipValuesOfCell(EmptyValue_For_ShipValuesOfCell):
    '''
    Don't Use
    '''
    __ship_owner = None
    __is_check_fill_of_of_ship_owner = True
    def __init__(self, ship_owner, symbol='■'):
        super().__init__(symbol)
        self.__fill_of_of_ship_owner_and_check_filling(ship_owner)

    def __fill_of_of_ship_owner_and_check_filling(self, ship_owner):
        self.__ship_owner = ship_owner
        if self.__is_check_fill_of_of_ship_owner:
            self.__check_filling_of_ship_owner

    def _set_check_fill_of_of_ship_owner(self, is_check_fill_of_of_ship_owner):
        if type(is_check_fill_of_of_ship_owner) is bool:
            self.__is_check_fill_of_of_ship_owner = is_check_fill_of_of_ship_owner
        else:
            gv.interface.add_and_raise_error(text, group, status, error_code, ValueError) #NFC

    def __check_filling_of_ship_owner(self):
        if self.__ship_owner is None:
            gv.interface.add_and_raise_error(text, group, status, error_code, ValueError) #NFC

    @property
    def is_empty_value(self):
        return False

    @property
    def is_ship_cell_value(self):
        return True

    @property
    def occupied_cell(self):
        return False

    @property
    def ship_owners(self):
        return [self.__ship_owner]

    @staticmethod
    def __short_name__():
        return 'SV'