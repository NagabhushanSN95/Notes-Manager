#!/usr/bin/env python
# Shree KRISHNAya Namaha
# Author: Nagabhushan S N


# Please execute the below line in terminal before executing the Python program
# chmod u+x Image_To_PDF_Generator.py
# Execute this python file as below
# ./Image_To_PDF_Generator.py -b Bookmarks.txt -md Meta-Data.txt -d ./Images/

import argparse
import math
import os
import shlex
import shutil
import subprocess

META_DATA_TITLE_KEY = 'Title'
META_DATA_AUTHOR_KEY = 'Author'
NUM_PAGES_CONST = 'NumPages'
OFFSET_CONST = 'Offset'
PAGE_NOS_CONST = 'PageNos'


def prompt(prompt_string):
    response = input(prompt_string)
    if response == 'Y':
        return True
    else:
        return False


def execute_cmd(cmd, print_cmd=False):
    if print_cmd:
        print("terminal$ " + cmd)
    if isinstance(cmd, list):
        commands = cmd
    else:
        commands = shlex.split(cmd)
    output = subprocess.Popen(commands, stdout=subprocess.PIPE).communicate()[0]
    return output


def setup_args():
    parser = argparse.ArgumentParser(description='Create PDF from images')
    parser.add_argument('--bookmarks', '-b', help="Bookmarks file (default: ./Bookmarks.txt",
                        type=str, default='./Bookmarks.txt')
    parser.add_argument('--meta-data', '-md', help="Meta-Data file (default: ./Meta-Data.txt",
                        type=str, default='./Meta-Data.txt')
    parser.add_argument('--directory', '-d', help="Path to directory containing images (default: ./Images/)",
                        type=str, default='./Images')
    parser.add_argument('--rotate', '-r', help="Angle in degrees to rotate all the images clockwise (default: 0)",
                        type=str, default=0)
    parser.add_argument('--gui', '-g', help="Start GUI (Graphical User Interface)", action='store_true')
    args = parser.parse_args()
    return args


def validate_inputs(args):
    # Check if Bookmarks file exists
    bookmarks_file_name = args.bookmarks
    if not os.path.isfile(bookmarks_file_name):
        print("The Bookmarks file '" + bookmarks_file_name + "' doesn't exist.\n")
        print("Exiting Program...")
        exit()

    # Check if Meta-Data file exists
    meta_data_file_name = args.meta_data
    if not os.path.isfile(meta_data_file_name):
        print("The Meta-Data file '" + meta_data_file_name + "' doesn't exist.\n")
        print("Exiting Program...")
        exit()

    # Check if Images directory exists
    images_directory_name = args.directory
    if not os.path.isdir(images_directory_name):
        print("The directory '" + images_directory_name + "' doesn't exist.\n")
        print("Exiting Program...")
        exit()


def read_inputs(args):
    bookmarks_file_name = args.bookmarks
    bookmarks_file = open(bookmarks_file_name, 'r')
    bookmarks_data = bookmarks_file.read().splitlines()
    bookmarks_data = [line.strip() for line in bookmarks_data if line.strip()]
    bookmarks_file.close()

    meta_data_file_name = args.meta_data
    meta_data_file = open(meta_data_file_name, 'r')
    meta_data_list = meta_data_file.read().splitlines()
    meta_data_list = [line.strip() for line in meta_data_list if line.strip()]
    # Convert list into a Dictionary (Python2)
    # noinspection PyTypeChecker
    meta_data = dict(map(None, *[iter(meta_data_list)] * 2))
    meta_data_file.close()

    directory = args.directory
    if not directory.endswith('/'):
        directory = directory + '/'
    rotate = args.rotate

    return bookmarks_file_name, bookmarks_data, meta_data, directory, rotate


def rotate_files(directory, degrees):
    if degrees != 0:
        print("Rotating files by " + degrees + " clockwise")
        for fileName in os.listdir(directory):
            cmd = 'convert ' + directory + fileName + ' -rotate ' + degrees + ' ' + directory + fileName
            os.system(cmd)
        print("Rotating Files complete")


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


def generate_meta_data(meta_data_dict, bookmarks_data):
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
            current_page_num += extract_num_pages(current_line)
        elif OFFSET_CONST in current_line:
            # Do Nothing
            continue
        elif PAGE_NOS_CONST in current_line:
            current_page_num += len(extract_page_nos(current_line))
        elif (NUM_PAGES_CONST not in next_to_next_line) or (extract_num_pages(next_to_next_line) > 0):
            # If NUM_PAGES_CONST is not present in next-to-next-line, then this is the name of a chapter
            # or something like that and hence has to be added in bookmarks
            # If next-to-next-line has NumPages>0, then this is the lowest level, but has pages
            # and hence this has to be added to bookmarks
            append_bookmark(current_line, current_level, current_page_num, meta_data)

    # print page_nos
    return meta_data


def append_bookmark(bookmark_name, level, page_num, meta_data):
    meta_data.append("BookmarkBegin")
    meta_data.append("BookmarkTitle: " + bookmark_name)
    meta_data.append("BookmarkLevel: " + str(level))
    meta_data.append("BookmarkPageNumber: " + str(page_num))


def rename_files(directory, title, page_nos, bookmarks_file_name):
    print("Renaming Files")
    i = 0
    os.chdir(directory)
    num_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
    num_pages = len(page_nos)
    # Provide a prompt to continue or exit
    if num_files < num_pages:
        if not prompt("Warning: " + bookmarks_file_name + " lists a total of " + str(num_pages) + " pages. "
                                                                                                  "But the directory "
                                                                                                  "'" + directory +
                      "' has only " + str(
            num_files) + " files."
                         "Do you want to proceed? [Y/n]:"):
            print("Exiting program...")
            exit()
    elif num_files > num_pages:
        if not prompt("Warning: " + bookmarks_file_name + " lists a total of " + str(num_pages) + " pages. "
                                                                                                  "But the directory "
                                                                                                  "'" + directory +
                      "' has " + str(
            num_files) + " files. "
                         "First " + str(num_pages) + " files will be renamed. Do you want to proceed? [Y/n]:"):
            print("Exiting program...")
            exit()

    for fileName in sorted(os.listdir('.')):
        extension = os.path.splitext(fileName)[1]
        os.rename(fileName, title + ' - ' + page_nos[i] + extension)
        i += 1
        if i >= num_pages:
            break
    os.chdir("../")
    print("Renaming Files complete")


# Todo: Move this to a separate class in a separate file
def scale_to_a4(directory):
    print("Scaling Images to A4 size")
    os.mkdir("./temp/scaled_images")
    """
    Display Width:
    convert DSP_03.jpg -format "%[fx:w]" info:
    Display Height:
    convert DSP_03.jpg -format "%[fx:h]" info:
    
    Aspect ratio of A4 is 1/sqrt(2)=0.707
    If aspect ratio is less than 0.707, then width has to be increased. Else, height has to be increased.
    Eg: 1932x3304
    Add 20 pixels margin: 1972x3344
    Calculate the new width/height: 2336x3304; 2364x3344
    Size of A4 is 297mmx210mm
    Calculate density: 3304/29.7=111.2458 pixels/cm; 3344/29.7=112.5926
    Command:
    convert DSP_03.jpg -gravity Center -extent 2336x3304 -density 111.2458 -units pixelspercentimeter out.jpg
    convert DSP_03.jpg -gravity Center -extent 2336x3304 -density 111.2458 -units pixelspercentimeter out.pdf
    
    convert DSP_03.jpg -gravity Center -extent 2364x3344 -density 112.5926 -units pixelspercentimeter out2.jpg
    convert DSP_03.jpg -gravity Center -extent 2364x3344 -density 112.5926 -units pixelspercentimeter out2.pdf
    """
    for file_name in sorted(os.listdir(directory)):
        file_name = file_name.replace(" ", "\ ")
        command = "convert " + directory + "/" + file_name + ' -format "%[fx:w]" info:'
        width = float(execute_cmd(command))
        command = "convert " + directory + "/" + file_name + ' -format "%[fx:h]" info:'
        height = float(execute_cmd(command))
        aspect_ratio = width / height
        a4_aspect_ratio = 1 / math.sqrt(2)
        if aspect_ratio < a4_aspect_ratio:
            # Increase Width
            new_height = height
            new_width = a4_aspect_ratio * height
            convert_to_a4(directory, file_name, new_width, new_height)
        elif aspect_ratio > a4_aspect_ratio:
            # Increase Height
            new_width = width
            new_height = width / a4_aspect_ratio
            convert_to_a4(directory, file_name, new_width, new_height)
        else:
            shutil.copyfile(directory + "/" + file_name, "./temp/scaled_images")
            return
    print("Scaling Images to A4 size complete")


def convert_to_a4(directory, file_name, new_width, new_height):
    density = new_height / 29.7  # Height of A4 = 29.7cm
    command = "convert " + directory + "/" + file_name + " -gravity Center -extent " + str(new_width) + "x" + \
              str(new_height) + " -density " + str(density) + " -units pixelspercentimeter ./temp/scaled_images/" \
              + file_name
    execute_cmd(command)


def convert_to_pdf(directory):
    print("Converting Images to PDFs")
    os.mkdir("./temp/pdfs")
    for file_name in sorted(os.listdir(directory)):
        file_name = file_name.replace(" ", "\ ")
        command = "convert ./temp/scaled_images/" + file_name + " ./temp/pdfs/" + os.path.splitext(file_name)[
            0] + ".pdf"
        os.system(command)
    print("Converting Images to PDFs complete")


def merge_files():
    print("Merging files into single PDF")
    cmd = "pdftk "
    for file_name in sorted(os.listdir("./temp/pdfs")):
        file_name = file_name.replace(" ", "\ ")
        cmd += "./temp/pdfs/" + file_name + " "
    cmd += "output ./temp/merged.pdf"
    os.system(cmd)
    print("Merging complete")


def add_bookmarks(title, meta_data):
    cmd = "pdftk ./temp/merged.pdf dump_data > ./temp/meta_data.txt"
    os.system(cmd)
    # Append additional meta-data and bookmarks to existing meta-data
    meta_data_file = open("./temp/meta_data.txt", 'a')
    meta_data_file.writelines("%s\n" % item for item in meta_data)
    meta_data_file.close()
    title1 = title.replace(" ", "\ ")
    cmd = "pdftk ./temp/merged.pdf update_info ./temp/meta_data.txt output " + title1 + ".pdf"
    os.system(cmd)


def clean():
    print("Cleaning Residual and Temporary Files")
    shutil.rmtree("./temp")


def main():
    # Remove temporary directory ./temp if it exists
    if os.path.exists("./temp"):
        if (prompt("Directory temp already exists. It needs to be removed to proceed. "
                   "Do you want to remove it now? [Y/n]:")):
            shutil.rmtree("./temp")
        else:
            print("Exiting program...")
            exit()

    args = setup_args()
    validate_inputs(args)
    (bookmarks_file_name, bookmarks_data, meta_data_dict, directory, rotate) = read_inputs(args)
    rotate_files(directory, rotate)
    title = meta_data_dict[META_DATA_TITLE_KEY]
    page_numbers = generate_page_nos(bookmarks_data)
    meta_data = generate_meta_data(meta_data_dict, bookmarks_data)
    rename_files(directory, title, page_numbers, bookmarks_file_name)
    os.mkdir("./temp")
    # directory = 'Images/'
    scale_to_a4(directory)
    convert_to_pdf(directory)
    merge_files()
    add_bookmarks(title, meta_data)
    clean()
    print("Process Complete")


if __name__ == '__main__':
    main()
