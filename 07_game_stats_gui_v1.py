from tkinter import *
from functools import partial # to prevent unwanted windows

import random


class Game:
    def __init__(self):

        # formatting variables
        self.game_stats_list = [50, 6]

        # in actual program this is blank and is populated with user calculations
        self.round_stats_list = ['silver ($4) | silver ($4) | lead ($0) - Cost: $10' 'lead ($0) | silver ($4) | gold ($10) - Cost: $10' 
        'lead ($0) | lead ($0) | copper ($2) - Cost: $10' 
        'copper ($2) | lead ($0) | copper ($2) - Cost: $10' 
        'lead ($0) | lead ($0) | lead ($0) - Cost: $10' 
        'lead ($0) | silver ($0) | silver ($4) - Cost: $10' 
        'silver ($4) | silver ($4) | silver ($4) - Cost: $10' 
        'copper ($2) | silver ($4) | lead ($0) - Cost: $10' 
        'lead ($0) | lead ($0) | copper ($2) - Cost: $10' 
        'copper ($2) | copper ($2) | silver ($4) - Cost: $10' 
        'copper ($2) | silver ($4) | silver ($4) - Cost: $10' 
        'copper ($2) | lead ($0) | silver ($4) - Cost: $10']