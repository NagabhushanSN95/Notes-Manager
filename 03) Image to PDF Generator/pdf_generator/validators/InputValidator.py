# Shree KRISHNAya Namaha
# To validate the inputs
# Author: Nagabhushan S N

import os

from data.DataStructures import InputData


class InputValidator:
    def __init__(self, input_data: InputData) -> None:
        self.input_data = input_data
        self.bookmarks_filepath = input_data.bookmarks_filepath
        self.metadata_filepath = input_data.metadata_filepath
        self.images_directory_path = input_data.images_directory_path
        self.actions = input_data.actions

    def validate_inputs(self):
        # Check if Bookmarks file exists
        if not os.path.isfile(self.bookmarks_filepath):
            print("The Bookmarks file '" + self.bookmarks_filepath + "' doesn't exist.\n")
            print("Exiting Program...")
            exit()

        # Check if Meta-Data file exists
        if not os.path.isfile(self.metadata_filepath):
            print("The Meta-Data file '" + self.metadata_filepath + "' doesn't exist.\n")
            print("Exiting Program...")
            exit()

        # Check if Images directory exists
        if not os.path.isdir(self.images_directory_path):
            print("The directory '" + self.images_directory_path + "' doesn't exist.\n")
            print("Exiting Program...")
            exit()
