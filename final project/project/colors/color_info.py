"""
This file is for any color recognition related code
"""

colors_dictionary = {
    "black": {"mean": [0, 0, 0]},
    "white": {"mean": [300, 300, 200]},
    #"red": {"mean": [250, 30, 30]},
    #"green": {"mean": [20, 100, 30]},
    #"blue": {"mean": [20, 30, 45]},
    "yellow": {"mean": [300, 200, 20]},
    "orange": {"mean": [240, 80, 50]},
    "purple": {"mean": [185, 35, 35]},
    "map_white": {"mean": [300, 260, 170]},
    "map_tape": {"mean": [190, 170, 100]},
    "blue": {"mean": [37,60,60]},
    "map_blue_plus_tape": {"mean": [45,50,52]},
    "red": {"mean": [245,38,18]},
    "map_red_plus_tape": {"mean": [250,45,30]},
    "green": {"mean": [37,100,20]},
    "map_green_plus_tape": {"mean": [50,120,30]},
    #"red_white_boundary": {"mean": [255,100,75]},
    #"blue_white_boundary": {"mean": [280,255,160]},
    }

def get_cd() -> dict: 
    return colors_dictionary

mapred = ["map_red", "map_red_plus_tape"]
mapblue = ["map_blue", "map_blue_plus_tape"]
mapgreen = ["map_green", "map_green_plus_tape"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_zones = ["red_zone", "orange_zone", "green_zone", "blue_zone", "purple_zone"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]
