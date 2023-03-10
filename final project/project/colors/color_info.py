"""
This file is for any color recognition related code
"""

colors_dictionary = {
    "black": {"mean": [0, 0, 0]},
    "white": {"mean": [300, 300, 200]},
    "red": {"mean": [250, 30, 30]},
    "green": {"mean": [20, 100, 30]},
    "blue": {"mean": [20, 30, 45]},
    "yellow": {"mean": [300, 200, 20]},
    "orange": {"mean": [240, 70, 50]},
    #"orange_zone": {"mean": [240, 70, 50],
    "purple": {"mean": [70, 50, 70]},
    "map_white": {"mean": [300, 260, 170]},
    "map_tape": {"mean": [190, 170, 100]},
    "map_blue": {"mean": [37,60,60]},
    "map_blue_plus_tape": {"mean": [45,50,52]},
    "map_red": {"mean": [245,38,18]},
    "map_red_plus_tape": {"mean": [250,50,30]},
    "map_green": {"mean": [37,100,20]},
    "map_green_plus_tape": {"mean": [50,120,30]},
    #"red_white_boundary": {"mean": [255,100,75]},
    #"blue_white_boundary": {"mean": [280,255,160]},
    "pink": {"mean": [255, 192, 203]},
    }

def get_cd() -> dict: 
    return colors_dictionary

mapred = ["map_red", "map_red_plus_tape", "red"]
mapblue = ["map_blue", "map_blue_plus_tape", "blue"]
mapgreen = ["map_green", "map_green_plus_tape", "green"]
mapwhite = ["map_white", "white", "map_tape"]
delivery_zones = ["red_zone", "orange_zone", "green_zone", "blue_zone", "purple_zone"]
delivery_cubes = ["red", "orange", "yellow", "green", "blue", "purple"]
