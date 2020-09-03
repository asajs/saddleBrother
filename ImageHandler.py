from os import path, listdir
from os.path import isfile, join
import os
import random
import sys

IMAGE_PREFIX = "Images/"


def get_path(file):
    root = get_root()
    return path.join(root, file)


def get_random_of_type(zone_type, image_type):
    root = get_root()
    path_to_folder = join(root, IMAGE_PREFIX, zone_type.value, image_type.value)
    only_files = [f for f in listdir(path_to_folder) if valid_image(path_to_folder, f)]
    file = random.choice(only_files)
    path_to_file = get_path(join(path_to_folder, file))
    return path_to_file


def get_specific(path_to_item):
    root = get_root()
    path_to_file = get_path(join(root, IMAGE_PREFIX, path_to_item))
    return path_to_file


def valid_image(path_to_folder, file):
    root = get_root()
    valid = isfile(join(root, path_to_folder, file)) and file.endswith(".png")
    return valid


def get_specifc_image( zone_type, image_type, monster_type):
    root = get_root()
    path_to_file = join(root, IMAGE_PREFIX, zone_type.value, image_type.value, monster_type.value)
    path = get_path(path_to_file)
    return path


def get_root():
    root = ""
    if getattr(sys, 'frozen', False):
        root = os.path.dirname(sys.executable)
    elif __file__:
        root = os.path.dirname(__file__)
    return root



