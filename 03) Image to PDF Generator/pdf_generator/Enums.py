from enum import Enum


class Mode(Enum):
    GENERATE_PDF = 'Generate-PDF'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    @staticmethod
    def get_mode(mode):
        if mode == 'Generate-PDF':
            return Mode.GENERATE_PDF
        else:
            raise Exception('Invalid Mode: ' + mode)


class Action(Enum):
    RENAME_IMAGES = 'Rename Images'
    SCALE_TO_A4 = 'Scale to A4 size'
    CONVERT_TO_PDF = 'Convert to PDF'
    MERGE_PDF = 'Merge PDFs'
    NOTIFY_COMPLETION = 'Notify Task Completion'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    @staticmethod
    def get_mode(action):
        for valid_action in Action:
            if action == valid_action.value:
                return valid_action
        raise Exception('Invalid Action: ' + action)
