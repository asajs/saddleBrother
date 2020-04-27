from os import path, listdir
from os.path import isfile, join
import random

IMAGE_PREFIX = "Images/"


def get_path(file):
    return path.abspath(file)


def get_random_of_type(zone_type, image_type):
    path_to_folder = join(IMAGE_PREFIX, zone_type.value, image_type.value)
    only_files = [f for f in listdir(path_to_folder) if valid_image(path_to_folder, f)]
    file = random.choice(only_files)
    return get_path(join(path_to_folder, file))


def get_specific(path_to_item):
    return get_path(join(IMAGE_PREFIX, path_to_item))


def valid_image(path_to_folder, file):
    return isfile(join(path_to_folder, file)) and file.endswith(".png")


def get_specifc_image( zone_type, image_type, monster_type):
    path_to_file = join(IMAGE_PREFIX, zone_type.value, image_type.value, monster_type.value)
    return get_path(path_to_file)



