from os import path, listdir
from os.path import isfile, join
import random


class ImageHandler:
    def __init__(self):
        self.image_prefix = "Images/"

    @staticmethod
    def get_path(file):
        return path.abspath(file)

    def get_random_of_type(self, zone_type, image_type):
        path_to_folder = join(self.image_prefix, zone_type.value, image_type.value)
        only_files = [f for f in listdir(path_to_folder) if self.valid_image(path_to_folder, f)]
        file = random.choice(only_files)
        return self.get_path(join(path_to_folder, file))

    def get_specific(self, path_to_item):
        return self.get_path(join(self.image_prefix, path_to_item))

    def valid_image(self, path_to_folder, file):
        return isfile(join(path_to_folder, file)) and file.endswith(".png")


