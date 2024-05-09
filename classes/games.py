import global_variables as gv

class Games:
    '''
    It is like an abstract class for games
    '''
    __difficulty_level = 1
    __list_of_gamers = []
    __сurrent_gamer = None
    __settings = {}

    def __init__(self):
        pass 

    @staticmethod
    def __short_name__():
        return 'GM'