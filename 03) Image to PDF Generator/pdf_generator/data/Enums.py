from enum import Enum


class Mode(Enum):
    GENERATE_PDF = 'Generate-PDF'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    @staticmethod
    def get_mode(mode):
        for valid_mode in Mode:
            if mode == valid_mode.value:
                return valid_mode
        raise Exception('Invalid Mode: ' + mode)

    @staticmethod
    def get_all_modes():
        modes = [mode for mode in Mode]
        return modes


class Action(Enum):
    RENAME_IMAGES = 'Rename Images'
    SCALE_TO_A4 = 'Scale to A4 size'
    CONVERT_TO_PDF = 'Convert to PDF'
    MERGE_PDF = 'Merge PDFs'
    ADD_BOOKMARKS = 'Add Bookmarks in PDF'
    NOTIFY_COMPLETION = 'Notify Task Completion'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    @staticmethod
    def get_action(action):
        for valid_action in Action:
            if action == valid_action.value:
                return valid_action
        raise Exception('Invalid Action: ' + action)

    @staticmethod
    def get_all_actions():
        actions = [action for action in Action]
        return actions
