"""
This file is for any color data related code
"""

# colors_dictionary = {
#     "black": {"mean": [0, 0, 0]},
#     "white": {"mean": [300, 300, 200]},
#     "yellow": {"mean": [150, 150, 10]},
#     "orange": {"mean": [150, 55, 13]},
#     "purple": {"mean": [114, 20, 25]},
#     "map_white": {"mean": [300, 260, 170]},
#     "map_tape": {"mean": [190, 170, 100]},
#     "blue": {"mean": [20,40,50]},
#     "map_blue_plus_tape": {"mean": [45,50,52]},
#     "red": {"mean": [150,25,10]},
#     "map_red_plus_tape": {"mean": [250,45,30]},
#     "green": {"mean": [30,90,15]},
#     "map_green_plus_tape": {"mean": [50,120,30]},
#     }

colors_dictionary = {
    "black": {"mean": [0, 0, 0]},
    "white": {"mean": [300, 300, 200]},
    "border": {"mean": [170, 170, 70]},
    # "yellowside": {"mean": [230, 200, 20]},
    "yellow": {"mean": [330, 310, 30]},
    "yellowfront": {"mean": [235, 200, 20]},
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

