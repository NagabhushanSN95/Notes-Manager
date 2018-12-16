# Shree KRISHNAya Namaha
# Starting point
# Author: Nagabhushan S N

import argparse
import os
import shutil

from backend import Helper
from data.DataStructures import InputData
from data.Enums import Action
from frontend import CLI, GUI
from utils.CommonUtilities import display_message, yes_no_prompt
from validators.InputValidator import InputValidator

META_DATA_TITLE_KEY = 'Title'
META_DATA_AUTHOR_KEY = 'Author'
NUM_PAGES_CONST = 'NumPages'
OFFSET_CONST = 'Offset'
PAGE_NOS_CONST = 'PageNos'


def delete_temp_dir(gui: bool):
    # Remove temporary directory ./temp if it exists
    if os.path.exists("./temp"):
        if (yes_no_prompt("Directory temp already exists. It needs to be removed to proceed. "
                          "Do you want to remove it now?", gui)):
            shutil.rmtree("./temp")
        else:
            display_message("Exiting program...", gui)
            exit()


def setup_args():
    parser = argparse.ArgumentParser(description='Create PDF from images')
    parser.add_argument('--bookmarks', '-b', help="Bookmarks file (default: ./Bookmarks.txt",
                        type=str, default='./Bookmarks.txt')
    parser.add_argument('--meta-data', '-md', help="Meta-Data file (default: ./Meta-Data.txt",
                        type=str, default='./Meta-Data.txt')
    parser.add_argument('--directory', '-d', help="Path to directory containing images (default: ./Images/)",
                        type=str, default='./Images')
    parser.add_argument('--scaleA4', '-s', help="Scale images to A4 size. Whitespace will be padded if required",
                        action='store_true')
    parser.add_argument('--rotate', '-r', help="Angle in degrees to rotate all the images clockwise (default: 0)",
                        type=str)
    parser.add_argument('--gui', '-g', help="Start GUI (Graphical User Interface)", action='store_true')
    args = parser.parse_args()
    return args


def parse_args(args):
    bookmarks_filepath = args.bookmarks
    metadata_filepath = args.meta_data
    images_directory_path = args.directory
    rotate_angle = args.rotate
    actions = []
    if args.scaleA4:
        actions.append(Action.SCALE_TO_A4)
    gui = args.gui
    args_input_data = InputData(bookmarks_filepath, metadata_filepath, images_directory_path, rotate_angle, actions,
                                gui)
    return args_input_data


def start_interactor(args_input_data):
    if args_input_data.gui:
        GUI.main(args_input_data, execute_callback)
    else:
        CLI.main(args_input_data, execute_callback)


def execute_callback(input_data: InputData):
    print('Executing Commands')
    InputValidator(input_data).validate_inputs()
    Helper.main(input_data)


def main():
    args = setup_args()
    delete_temp_dir(args.gui)
    args_input_data = parse_args(args)
    start_interactor(args_input_data)


if __name__ == '__main__':
    main()
