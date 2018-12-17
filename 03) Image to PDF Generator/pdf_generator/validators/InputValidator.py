# Shree KRISHNAya Namaha
# To validate the inputs
# Author: Nagabhushan S N

import os

from data.DataStructures import InputData
from data.Enums import Action
from utils.CommonUtilities import display_message


class InputValidator:
    def __init__(self, input_data: InputData) -> None:
        self.input_data = input_data
        self.bookmarks_filepath = input_data.bookmarks_filepath
        self.metadata_filepath = input_data.metadata_filepath
        self.images_directory_path = input_data.images_directory_path
        self.actions = input_data.actions

    def validate_inputs(self):
        if (Action.RENAME_IMAGES in self.input_data.actions) or (Action.ADD_BOOKMARKS in self.input_data.actions):
            # Check if Bookmarks file exists
            if not os.path.isfile(self.bookmarks_filepath):
                display_message(
                    "The Bookmarks file '" + self.bookmarks_filepath + "' doesn't exist.\nExiting Program...",
                    self.input_data.gui)
                exit()

        # Check if Images directory exists
        if not os.path.isdir(self.images_directory_path):
            display_message("The directory '" + self.images_directory_path + "' doesn't exist.\nExiting Program...",
                            self.input_data.gui)
            exit()
