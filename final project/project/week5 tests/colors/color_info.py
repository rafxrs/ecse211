"""
This file is for any color data related code
"""

colors_dictionary = {
    "black": {"mean": [0, 0, 0]},
    "white": {"mean": [300, 300, 200]},
    "border": {"mean": [150, 140, 90]},
    # "yellowside": {"mean": [230, 200, 20]},
    "yellow": {"mean": [330, 310, 30]},
    "yellowfront": {"mean": [190, 165, 15]},
    "orange": {"mean": [320, 110, 20]},
    "purple": {"mean": [240, 40, 50]},
    "map_white": {"mean": [300, 260, 170]},
    "map_tape": {"mean": [190, 170, 100]},
    "blue": {"mean": [40,60,60]},
    "bluefront": {"mean": [27,45,60]},
    "map_blue_plus_tape": {"mean": [45,50,52]},
    "red": {"mean": [280,38,18]},
    "redfront": {"mean": [205,30,10]},
    "map_red_plus_tape": {"mean": [250,45,30]},
    "green": {"mean": [50,150,25]},
    "map_green_plus_tape": {"mean": [50,120,30]},
    }

def get_cd() -> dict: 
    return colors_dictionary

