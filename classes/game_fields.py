import global_variables as gv

class GameFields:
    '''
    
    '''
    __x_size = 6
    __y_size = 6
    __cell_storage = None
    __size = 0
    __use_column_titles = True
    __use_row_titles = True
    __column_titles = []
    __row_titles = []
    __temporary_storage_for_ships = None
    __is_arrangement_of_ships = True
    def __init__(self, size = 6, use_column_titles = True, use_row_titles = True, column_titles = None, row_titles = None, x_size = None, y_size = None) -> None:
        if x_size is None or y_size is None:
            self.__set_size(size)
        else:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(GameFields, '__init__', 'error_setting_size_by_x_y_axis', '01', 3)) 
        self.__temporary_storage_for_ships = self.__get_cell_storage_with_empty_cells()
        self.__use_column_titles = use_column_titles
        self.__use_row_titles = use_row_titles
        self.__set_column_row_titles('__column_titles', self.__use_column_titles, column_titles, self.__x_size)
        self.__set_column_row_titles('__row_titles', self.__use_row_titles, row_titles, self.__y_size)
        self.__is_arrangement_of_ships = True

    def transfer_of_ships_to_the_main_storage(self):
        # trasfer this
        self.__is_arrangement_of_ships = False

    def reflect_hit(self, x, y, gamer):  
        self.__cell_storage.reflect_hit(x, y, gamer)

    def __set_column_row_titles(self, type_of_class_field, use_column_row_titles, titles, size):
        if use_column_row_titles:
            if titles is None:
                titles = [str(i) for i in range(1, size + 1)]
            else:
                if len(titles) > size:
                    titles = titles[:size]
                elif len(titles) < size:
                    for i in range(size):
                        titles.append('')
        if type_of_class_field == '__column_titles':
            self.__column_titles = titles
        elif type_of_class_field == '__row_titles':
            self.__row_titles = titles
        
    def get_cell(self, _x, _y, show_user = False):
        return self.__cell_storage.get_cell(_x, _y, show_user)

    def get_field_as(self, _type = list):
        cell_storage = self.__temporary_storage_for_ships if self.__is_arrangement_of_ships else self.__cell_storage
        if _type is list:
            list_of_field = []
            for x in range(self.__x_size):
                list_of_y = []
                for y in range(self.__y_size):
                    list_of_y.append(cell_storage.get_cell(x, y))
                list_of_field.append(list_of_y)
            return list_of_field

    def __get_cell_storage_with_empty_cells(self):
        from cell_storage import CellStorage
        cell_storage = CellStorage(self.__x_size, self.__y_size)
        return cell_storage

    def __set_size(self, size):
        size_restrictions = GameFields.get_size_restrictions()
        if not size in range(size_restrictions[0], size_restrictions[1] + 1):
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(GameFields, '__set_size', 'error_setting_size_size_is_over', '02', 3))
        self.__x_size = size
        self.__y_size = size
        self.__size = self.__x_size * self.__y_size

    def _get_access_values_for_location_ship(self, data_of_ship, show_user):
        if self.__temporary_storage_for_ships is None:
            self._fill_temporary_storage()
        data_of_ship.update({
            'game_field': self,
        })
        return self.__temporary_storage_for_ships.get_access_cells_for_ship(data_of_ship, show_user)

    def _fill_temporary_storage(self):
        self.__temporary_storage_for_ships = self.__get_cell_storage_with_empty_cells()

    def _move_field_from_temporary_storage_for_ships_in_main_storge(self):
        self.__cell_storage = self.__temporary_storage_for_ships
        self.__temporary_storage_for_ships = None
        self.__is_arrangement_of_ships = False

    def set_ship_and_return_tuple_of_ship_cells_and_ship_occupied_cell(self, ship, list_of_ship_cells) -> tuple:
        self.__check_correct_location_of_ship_on_field(list_of_ship_cells)
        ship_cells = []
        for coordinates in list_of_ship_cells:
            cell = self.__temporary_storage_for_ships.get_cell(*coordinates)
            cell.value.set_value_of_ship_cell(ship)
            ship_cells.append(cell)
        return tuple(ship_cells), self.__get_tuple_of_ship_occupied_cell(ship, ship_cells)

    def __get_tuple_of_ship_occupied_cell(self, ship, ship_cells):
        set_of_occupied_cells = set()
        list_of_offsets = []
        list_of_offsets.append((-1, -1))
        list_of_offsets.append((0, -1))
        list_of_offsets.append((1, -1))
        list_of_offsets.append((1, 0))
        list_of_offsets.append((1, 1))
        list_of_offsets.append((0, 1))
        list_of_offsets.append((-1, 1))
        list_of_offsets.append((-1, 0))
        for cell in ship_cells:
            for offset in list_of_offsets:
                try:
                    x, y = cell.coordinates
                    offseting_cell = self.__temporary_storage_for_ships.get_cell(x + offset[0], y + offset[1])
                    if offseting_cell.value.is_empty_value:
                        offseting_cell.value.set_value_of_ship_occupied_cell(ship)
                        set_of_occupied_cells.add(offseting_cell)  
                except ValueError:
                    pass  
        return tuple(set_of_occupied_cells)
         

    def __check_correct_location_of_ship_on_field(self, list_of_ship_cells):
        was_errors = False
        for coordinates in list_of_ship_cells:
            try:
                cell = self.__temporary_storage_for_ships.get_cell(*coordinates)
                cell.value.check_possible_to_set_value_of_ship_cell()
            except ValueError as key_string_error:
                was_errors = True
        if was_errors:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(GameFields, '__check_correct_location_of_ship_on_field', 'error_when_checking_correct_location_of_ship', '03', 1, True))

    def auto_set_location_of_ships(self):
        from random import randint

    @property
    def column_titles(self):
        return self.__column_titles if self.__use_column_titles else None

    @property
    def row_titles(self):
        return self.__row_titles if self.__use_row_titles else None

    @property
    def dict_of_access_counts_of_ships(self):
        return self.__dict_of_access_counts_of_ships

    @property
    def temporary_storage_for_ships(self):
        return self.__temporary_storage_for_ships

    @staticmethod
    def get_size_restrictions():
        return (6, 10) 

    @staticmethod
    def __short_name__():
        return 'GF'