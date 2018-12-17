# Shree KRISHNAya Namaha
import os

from data.Enums import Action


class InputData:

    def __init__(self, bookmarks_filepath, metadata_filepath, images_directory_path, rotate_angle, actions, gui=False):
        self.bookmarks_filepath = bookmarks_filepath
        self.metadata_filepath = metadata_filepath
        self.images_directory_path = images_directory_path
        self.rotate_angle = rotate_angle
        self.actions = actions
        self.gui = gui

    def remove_invalid_fields(self):
        if not os.path.exists(self.bookmarks_filepath):
            self.bookmarks_filepath = None
        if not os.path.exists(self.metadata_filepath):
            self.metadata_filepath = None
        if not os.path.exists(self.images_directory_path):
            self.images_directory_path = None

    @classmethod
    def from_dict(cls, input_data_dict: dict):
        if input_data_dict['actions'].strip('[]'):
            actions = [Action.get_action(action_name.strip(' ')) for action_name in
                       input_data_dict['actions'].strip('[]').split(',')]
        else:
            actions = []
        return cls(input_data_dict['bookmarks_filepath'], input_data_dict['metadata_filepath'],
                   input_data_dict['images_directory_path'], input_data_dict['rotate_angle'], actions,
                   input_data_dict['gui'])

    @classmethod
    def merge(cls, obj1, obj2):
        actions = list(obj1.actions) if obj1.actions else []
        actions.extend([action for action in obj2.actions if action not in obj1.actions])
        return cls(obj1.bookmarks_filepath if obj1.bookmarks_filepath is not None else obj2.bookmarks_filepath,
                   obj1.metadata_filepath if obj1.metadata_filepath is not None else obj2.metadata_filepath,
                   obj1.images_directory_path if obj1.images_directory_path is not None else obj2.images_directory_path,
                   obj1.rotate_angle if obj1.rotate_angle is not None else obj2.rotate_angle, actions,
                   obj1.gui if obj1.gui is not None else obj2.gui)
