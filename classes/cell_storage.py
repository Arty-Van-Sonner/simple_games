import global_variables as gv

class CellStorage:
    '''
    
    '''
    __x_size = 0
    __y_size = 0
    def __init__(self, x_size, y_size) -> None:
        from cells import Cells 
        self.__x_size = x_size
        self.__y_size = y_size
        sample_of_universal_name_of_cell = CellStorage._sample_of_universal_name_of_cell()
        for _x in range(self.__x_size):
            for _y in range(self.__y_size):
                setattr(self, sample_of_universal_name_of_cell.format(x = _x, y = _y), Cells(_x, _y))

    def get_cell(self, _x, _y, show_user = False):
        self.__check_out_of_field(_x, _y, show_user)
        return getattr(self, CellStorage._sample_of_universal_name_of_cell().format(x = _x, y = _y))
        
    def get_access_cells_for_ship(self, data_of_ship, show_user) -> list:
        list_of_ships_parameters = []
        for x in range(self.__x_size):
            for y in range(self.__y_size):
                cell = self.get_cell(x, y)
                sub_list_of_ships_parameters = self.__check_access_cell_for_start_to_creat_ship(cell, data_of_ship, show_user)
                list_of_ships_parameters.extend(sub_list_of_ships_parameters)
        return list_of_ships_parameters

    def reflect_hit(self, x, y, gamer):  
        self.__check_out_of_field(x, y, True)
        cell = self.get_cell(x, y)
        cell.value.reflect_hit(gamer)

    def __check_access_cell_for_start_to_creat_ship(self, cell, data_of_ship, show_user) -> list:
        returning_list = []
        start_x, start_y = cell.coordinates
        self.__check_access_axis_for_start_to_creat_ship('w', returning_list, start_x, start_y, data_of_ship, show_user)
        self.__check_access_axis_for_start_to_creat_ship('h', returning_list, start_x, start_y, data_of_ship, show_user)
        return returning_list

    def __check_access_axis_for_start_to_creat_ship(self, axis, returning_list, start_x, start_y, data_of_ship, show_user):
        length = data_of_ship['size']
        game_field = data_of_ship['game_field']
        add_it = True
        x = start_x 
        y = start_y
        for i in range(length):
            if axis == 'h':
                y += i
            else:
                x += i
            try:
                cell_buff = self.get_cell(x, y, show_user)
                # print(f'x: {x}; y: {y}; length: {length}, axis: {axis}')
                cell_buff.value.check_possible_to_set_value_of_ship_cell(show_user = show_user)
            except ValueError as ve:
                add_it = False
        if add_it:
            # print(f'x: {start_x}; y: {start_y}; length: {length}, axis: {axis}')
            returning_list.append(self.__get_dict_of_parameters_for_creat_ship(start_x, start_y, length, axis, game_field))

    def __get_dict_of_parameters_for_creat_ship(self, start_x, start_y, length, axis, game_field) -> dict:
        return {
            'start_x': start_x,
            'start_y': start_y,
            'length': length,
            'axis': axis,
            'game_field': game_field,
        }

    def __check_out_of_field(self, x, y, show_user = True):
        raise_error = False
        if x < 0:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(CellStorage, '__check_out_of_field', 'error_setting_size_by_x__x_is_below_zero', '01', 3, False, show_user = show_user))
            raise_error = True
        if y < 0:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(CellStorage, '__check_out_of_field', 'error_setting_size_by_y__y_is_below_zero', '02', 3, False, show_user = show_user))
            raise_error = True
        if x >= self.__x_size:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(CellStorage, '__check_out_of_field', 'error_setting_size_by_x__x_is_over_size', '03', 3, False, show_user = show_user))
            raise_error = True
        if y >= self.__y_size: 
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(CellStorage, '__check_out_of_field', 'error_setting_size_by_y__y_is_over_size', '04', 3, False, show_user = show_user))
            raise_error = True

        if raise_error:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(CellStorage, '__check_out_of_field', 'was_error_when_check_out_of_field', '05', 0, True, show_user = show_user))

    @staticmethod
    def _sample_of_universal_name_of_cell() -> str:
        return '__cell_{x}_{y}'

    @staticmethod
    def __short_name__():
        return 'CS'