import os
import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from .global_variables import *
from .cell import Cell
from .panel import Panel
from .board import Board
from .person import Person