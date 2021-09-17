import os

basic_colors = [
    '#ff0000', '#1ce11c', '#1414e5', '#ddeb00', '#fc6500', '#ca3a76',
    '#01f7f7', '#b58e4b', '#a93814', '#e73ee2'
]


def get_basic_color(index):
    return basic_colors[index % len(basic_colors)]


def get_faction_images():
    """ Returns paths to faction and background images"""
    images = os.listdir(outer("layout/factions"))
    return {
        i.replace(".png", "").replace(".jpg", ""): f"./factions/{i}"
        for i in images
    }


def inner(path):
    return path


def outer(path):
    return path
