# Shree KRISHNAya Namaha
# Command Line Interface
# Author: Nagabhushan S N
from data.DataStructures import InputData
from data.Enums import Action
from utils.CommonUtilities import yes_no_prompt


def collect_actions():
    actions = []
    if yes_no_prompt('Do you want to rename image files?'):
        actions.append(Action.RENAME_IMAGES)
    if yes_no_prompt('Do you want to scale images to A4 size?'):
        actions.append(Action.SCALE_TO_A4)
    if yes_no_prompt('Do you want to convert images to pdf files?'):
        actions.append(Action.CONVERT_TO_PDF)
    if yes_no_prompt('Do you want to merge pdf files?'):
        actions.append(Action.MERGE_PDF)
    if yes_no_prompt('Do you want to add bookmarks in the merged pdf file?'):
        actions.append(Action.ADD_BOOKMARKS)
    if yes_no_prompt('Do you want to clean temporary files?'):
        actions.append(Action.CLEAN_TEMP_FILES)
    if yes_no_prompt('Do you want to notify task completion?'):
        actions.append(Action.NOTIFY_COMPLETION)
    return actions


def main(args_input_data: InputData, execute_callback):
    actions = collect_actions()
    args_input_data.actions = actions
    if args_input_data.rotate_angle is None:
        args_input_data.rotate_angle = '0'
    execute_callback(args_input_data)
