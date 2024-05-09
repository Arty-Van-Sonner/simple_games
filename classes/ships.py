import global_variables as gv
from ship_values_of_cell import ShipValuesOfCell as ShipValuesOfCell_For_Ships

class Ships:
    '''
    
    '''
    __length = 0
    __axis = 'h/w'
    __start_x = 0
    __start_y = 0
    __health = 0
    __tuple_of_ship = ()
    __tuple_of_ship_occupied_cell = ()
    def __init__(self, start_x, start_y, length, axis, game_field) -> None:
        self.__length = length
        self.__health = self.__length
        self.__start_x = start_x
        self.__start_y = start_y
        self.__axis = axis
        list_of_ship_cells = []
        x = self.__start_x
        y = self.__start_y
        for i in range(self.__length):
            list_of_ship_cells.append((x, y))
            if self.__axis == 'h':
                y += 1
            else:
                x += 1
        self.__tuple_of_ship, self.__tuple_of_ship_occupied_cell = game_field.set_ship_and_return_tuple_of_ship_cells_and_ship_occupied_cell(self, list_of_ship_cells)

    def reflect_hit(self, x, y, gamer):
        self.__health -= 1
        current_game = gv.interface.current_game
        current_game._reduce_health_to_opponent(self)
        self.__ship_is_destroyed(gamer)

    def __ship_is_destroyed(self, gamer):
        if self.is_destroyed:
            for cell in self.__tuple_of_ship_occupied_cell:
                cell.value.set_occupied_cell_in_ship_is_destroyed(self)
            lang = gv.interface.current_language
            ship = self.name_of_ship
            text = lang.get_string_with_parameters('ship_is_destroyed', {'ship': ship, 'nickname': gamer.nickname,})
            gv.interface.add_message(text, True)

    @property
    def name_of_ship(self):
        if self.__length == 1:
            return 'torpedo_boat'
        elif self.__length == 2:
            return 'destroyer'
        elif self.__length == 3:
            return 'cruiser'
        else:
            return 'battleship'

    @property
    def tuple_of_ship(self) -> tuple:
        return self.__tuple_of_ship

    @property
    def tuple_of_ship_occupied_cell(self) -> tuple:
        return self.__tuple_of_ship_occupied_cell

    @property
    def is_destroyed(self):
        return self.__health <= 0

    def __str__(self) -> str:
        # self.__length
        lang = gv.interface.current_language
        list_of_posible_ships = []
        list_of_posible_ships.append((1, 'torpedo_boat'))
        list_of_posible_ships.append((2, 'destroyer'))
        list_of_posible_ships.append((3, 'cruiser'))
        list_of_posible_ships.append((4, 'battleship'))
        for ship in list_of_posible_ships:
            if self.__length == ship[0]:
                return lang.get_string(ship[0], ['all_first_upper'])

    @staticmethod
    def __short_name__():
        return 'Sh'
        
    