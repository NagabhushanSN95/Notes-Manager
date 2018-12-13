# Shree KRISHNAya Namaha
# Parse Meta-Data File
# Author: Nagabhushan S N

from data.Constants import NUM_PAGES_CONST, OFFSET_CONST, PAGE_NOS_CONST


def get_bookmarks_data(bookmarks_filepath):
    with open(bookmarks_filepath) as bm_file:
        lines = bm_file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    return lines


def generate_page_nos(bookmarks_data):
    num_levels = calc_num_levels(bookmarks_data)

    levels = [0] * (num_levels - 1)
    page_nos = []
    current_level = 0
    for i in range(0, len(bookmarks_data)):
        current_line = bookmarks_data[i]
        if i < len(bookmarks_data) - 1:
            next_line = bookmarks_data[i + 1]
        else:
            next_line = None
        if current_line == '{':
            current_level += 1
            if current_level > 1:
                levels[current_level - 2] += 1
        elif NUM_PAGES_CONST in current_line:
            num_pages = extract_num_pages(current_line)
            if num_pages > 0:
                if (next_line is not None) and (OFFSET_CONST in next_line):
                    offset = extract_offset(next_line)
                    synthesize_serial_page_nos(levels, current_level, num_pages, page_nos, offset)
                else:
                    synthesize_serial_page_nos(levels, current_level, num_pages, page_nos)
        elif PAGE_NOS_CONST in current_line:
            specific_page_nos = extract_page_nos(current_line)
            synthesize_specific_page_nos(levels, current_level, specific_page_nos, page_nos)
        elif current_line == '}':
            current_level -= 1
            reset_levels(levels, current_level)

    # print page_nos
    return page_nos


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


def extract_num_pages(line):
    return int(line.split('=')[1].strip())


def extract_offset(line):
    return int(line.split('=')[1].strip())


def extract_page_nos(line):
    page_nos_string = line.split('=')[1].strip()
    page_nos = [int(page_no) for page_no in page_nos_string.split(',')]
    return page_nos


def synthesize_serial_page_nos(levels, current_level, num_pages, page_nos, offset=0):
    for i in range(0, int(num_pages)):
        page_no = ''
        for j in range(0, current_level - 1):
            page_no += '{:02d}'.format(levels[j]) + '.'
        page_no += '{:02d}'.format(i + 1 + offset)
        page_nos.append(page_no)


def synthesize_specific_page_nos(levels, current_level, specific_page_nos, page_nos):
    for specific_page_no in specific_page_nos:
        page_no = ''
        for j in range(0, current_level - 1):
            page_no += '{:02d}'.format(levels[j]) + '.'
        page_no += '{:02d}'.format(specific_page_no)
        page_nos.append(page_no)


def reset_levels(levels, start_level):
    for i in range(start_level, len(levels)):
        levels[i] = 0


if __name__ == '__main__':
    bookmarks_data = get_bookmarks_data('../Meta-Data (Sample).txt')
    print(bookmarks_data)
