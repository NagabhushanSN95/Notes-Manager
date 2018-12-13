# Shree KRISHNAya Namaha
# Parse Bookmarks and Meta-Data File
# Author: Nagabhushan S N

from data.Constants import META_DATA_AUTHOR_KEY, META_DATA_TITLE_KEY, NUM_PAGES_CONST, OFFSET_CONST, PAGE_NOS_CONST
from data.DataStructures import InputData


class Parser:
    def __init__(self, input_data: InputData):
        self.input_data = input_data

    def get_bookmarks_data(self):
        with open(self.input_data.bookmarks_filepath) as bm_file:
            lines = bm_file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        return lines

    def get_metadata_dict(self):
        with open(self.input_data.metadata_filepath) as md_file:
            lines = md_file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        metadata_dict = {}
        for i in range(int(len(lines) / 2)):
            metadata_dict[lines[2 * i]] = lines[2 * i + 1]
        return metadata_dict

    @staticmethod
    def extract_num_pages(line):
        return int(line.split('=')[1].strip())

    @staticmethod
    def extract_offset(line):
        return int(line.split('=')[1].strip())

    @staticmethod
    def extract_page_nos(line):
        page_nos_string = line.split('=')[1].strip()
        page_nos = [int(page_no) for page_no in page_nos_string.split(',')]
        return page_nos

    def get_page_numbers(self):
        bookmarks_data = self.get_bookmarks_data()
        page_nos = PageNumbersGenerator(bookmarks_data).generate_page_nos()
        return page_nos

    def get_pdf_bookmarks(self):
        bookmarks_data = self.get_bookmarks_data()
        metadata_dict = self.get_metadata_dict()
        pdf_bookmarks = PdfBookmarksGenerator.generate_pdf_bookmarks(metadata_dict, bookmarks_data)
        return pdf_bookmarks

    def get_title(self):
        return self.get_metadata_dict()[META_DATA_TITLE_KEY]


class PageNumbersGenerator:
    def __init__(self, bookmarks_data):
        self.bookmarks_data = bookmarks_data

    def generate_page_nos(self):
        num_levels = self.calc_num_levels(self.bookmarks_data)

        levels = [0] * (num_levels - 1)
        page_nos = []
        current_level = 0
        for i in range(0, len(self.bookmarks_data)):
            current_line = self.bookmarks_data[i]
            if i < len(self.bookmarks_data) - 1:
                next_line = self.bookmarks_data[i + 1]
            else:
                next_line = None
            if current_line == '{':
                current_level += 1
                if current_level > 1:
                    levels[current_level - 2] += 1
            elif NUM_PAGES_CONST in current_line:
                num_pages = Parser.extract_num_pages(current_line)
                if num_pages > 0:
                    if (next_line is not None) and (OFFSET_CONST in next_line):
                        offset = Parser.extract_offset(next_line)
                        self.synthesize_serial_page_nos(levels, current_level, num_pages, page_nos, offset)
                    else:
                        self.synthesize_serial_page_nos(levels, current_level, num_pages, page_nos)
            elif PAGE_NOS_CONST in current_line:
                specific_page_nos = Parser.extract_page_nos(current_line)
                self.synthesize_specific_page_nos(levels, current_level, specific_page_nos, page_nos)
            elif current_line == '}':
                current_level -= 1
                self.reset_levels(levels, current_level)

        return page_nos

    # Todo: Make these static methods into instance methods
    @staticmethod
    def calc_num_levels(input_string):
        level = max_level = 0
        for line in input_string:
            if line == '{':
                level += 1
                if level > max_level:
                    max_level = level
            elif line == '}':
                level -= 1
        return max_level

    @staticmethod
    def synthesize_serial_page_nos(levels, current_level, num_pages, page_nos, offset=0):
        for i in range(0, int(num_pages)):
            page_no = ''
            for j in range(0, current_level - 1):
                page_no += '{:02d}'.format(levels[j]) + '.'
            page_no += '{:02d}'.format(i + 1 + offset)
            page_nos.append(page_no)

    @staticmethod
    def synthesize_specific_page_nos(levels, current_level, specific_page_nos, page_nos):
        for specific_page_no in specific_page_nos:
            page_no = ''
            for j in range(0, current_level - 1):
                page_no += '{:02d}'.format(levels[j]) + '.'
            page_no += '{:02d}'.format(specific_page_no)
            page_nos.append(page_no)

    @staticmethod
    def reset_levels(levels, start_level):
        for i in range(start_level, len(levels)):
            levels[i] = 0


class PdfBookmarksGenerator:
    @staticmethod
    def generate_pdf_bookmarks(meta_data_dict, bookmarks_data):
        meta_data = list()
        meta_data.append("InfoBegin")
        meta_data.append("InfoKey: Title")
        meta_data.append("InfoValue: " + meta_data_dict[META_DATA_TITLE_KEY])
        meta_data.append("InfoBegin")
        meta_data.append("InfoKey: Author")
        meta_data.append("InfoValue: " + meta_data_dict[META_DATA_AUTHOR_KEY])
        current_level = 0
        current_page_num = 1
        for i in range(0, len(bookmarks_data)):
            current_line = bookmarks_data[i]
            if i < len(bookmarks_data) - 2:
                next_to_next_line = bookmarks_data[i + 2]
            # noinspection PyUnboundLocalVariable
            if current_line == '{':
                current_level += 1
            elif current_line == '}':
                current_level -= 1
            elif NUM_PAGES_CONST in current_line:
                current_page_num += Parser.extract_num_pages(current_line)
            elif OFFSET_CONST in current_line:
                # Do Nothing
                continue
            elif PAGE_NOS_CONST in current_line:
                current_page_num += len(Parser.extract_page_nos(current_line))
            elif (NUM_PAGES_CONST not in next_to_next_line) or (Parser.extract_num_pages(next_to_next_line) > 0):
                # If NUM_PAGES_CONST is not present in next-to-next-line, then this is the name of a chapter
                # or something like that and hence has to be added in bookmarks
                # If next-to-next-line has NumPages>0, then this is the lowest level, but has pages
                # and hence this has to be added to bookmarks
                PdfBookmarksGenerator.append_bookmark(current_line, current_level, current_page_num, meta_data)

        return meta_data

    @staticmethod
    def append_bookmark(bookmark_name, level, page_num, meta_data):
        meta_data.append("BookmarkBegin")
        meta_data.append("BookmarkTitle: " + bookmark_name)
        meta_data.append("BookmarkLevel: " + str(level))
        meta_data.append("BookmarkPageNumber: " + str(page_num))
