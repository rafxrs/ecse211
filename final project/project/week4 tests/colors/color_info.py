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
    "yellow": {"mean": [370, 340, 30]},
    "orange": {"mean": [320, 110, 20]},
    "purple": {"mean": [240, 40, 50]},
    "map_white": {"mean": [300, 260, 170]},
    "map_tape": {"mean": [190, 170, 100]},
    "blue": {"mean": [37,60,60]},
    "map_blue_plus_tape": {"mean": [45,50,52]},
    "red": {"mean": [280,38,18]},
    "map_red_plus_tape": {"mean": [250,45,30]},
    "green": {"mean": [37,100,20]},
    "map_green_plus_tape": {"mean": [50,120,30]},
    }

def get_cd() -> dict: 
    return colors_dictionary

mapred = ["map_red", "map_red_plus_tape"]
mapblue = ["map_blue", "map_blue_plus_tape"]
mapgreen = ["map_green", "map_green_plus_tape"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]
