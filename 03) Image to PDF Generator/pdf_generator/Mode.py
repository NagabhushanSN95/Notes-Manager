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
