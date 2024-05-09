import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], 'classes'))
import global_variables as gv
from interface import Interface
from console import Console

if __name__ == '__main__':
    gv.interface = Interface(Console(False))
    gv.interface.start_game()