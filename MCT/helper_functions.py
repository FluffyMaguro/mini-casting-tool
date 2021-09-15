import os

basic_colors = [
    "#FF0000", "#1CE11C", "#1414E5", "#DDEB00", "#FC6500", "#CA3A76",
    "#01F7F7", "#B58E4B", "#A93814", "#E73EE2"
]


def get_basic_color(index):
    return basic_colors[index % len(basic_colors)]


def get_factions_backgrounds():
    """ Returns paths to faction and background images"""
    bg = os.listdir("src/backgrounds")
    bg = {i: os.path.abspath(os.path.join(os.getcwd(), i)) for i in bg}
    fc = os.listdir("src/factions")
    fc = {i: os.path.abspath(os.path.join(os.getcwd(), i)) for i in fc}

    return fc, bg
