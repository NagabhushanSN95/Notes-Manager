# Shree KRISHNAya Namaha
# Performs all the backend operations
# Author: Nagabhushan S N
import math
import os
import shlex
import shutil
import subprocess

from backend import BookmarksParser
from DataStructures import InputData
from Enums import Action
from backend.MetaDataParser import MetaDataParser
from data.Constants import META_DATA_AUTHOR_KEY, META_DATA_TITLE_KEY, NUM_PAGES_CONST, OFFSET_CONST, PAGE_NOS_CONST


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


def rotate_files(directory, degrees):
    if degrees != 0:
        print("Rotating files by " + degrees + " clockwise")
        for fileName in os.listdir(directory):
            cmd = 'convert ' + directory + fileName + ' -rotate ' + degrees + ' ' + directory + fileName
            os.system(cmd)
        print("Rotating Files complete")


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


# Todo: Use the one in Bookmark Parser or put it in utils
def extract_num_pages(line):
    return int(line.split('=')[1].strip())


# Todo: Use the one in Bookmark Parser or put it in utils
def extract_page_nos(line):
    page_nos_string = line.split('=')[1].strip()
    page_nos = [int(page_no) for page_no in page_nos_string.split(',')]
    return page_nos


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


def main(input_data: InputData):
    bookmarks_data = BookmarksParser.get_bookmarks_data(input_data.bookmarks_filepath)
    metadata_dict = MetaDataParser(input_data.metadata_filepath).metadata_dict
    rotate_files(input_data.images_directory_path, input_data.rotate_angle)
    title = metadata_dict[META_DATA_TITLE_KEY]
    page_numbers = BookmarksParser.generate_page_nos(bookmarks_data)
    meta_data = generate_meta_data(metadata_dict, bookmarks_data)
    if Action.RENAME_IMAGES in input_data.actions:
        rename_files(input_data.images_directory_path, title, page_numbers, input_data.bookmarks_filepath)
    os.mkdir("./temp")
    # directory = 'Images/'
    if Action.SCALE_TO_A4 in input_data.actions:
        scale_to_a4(input_data.images_directory_path)
    if Action.CONVERT_TO_PDF in input_data.actions:
        convert_to_pdf(input_data.images_directory_path)
    if Action.MERGE_PDF in input_data.actions:
        merge_files()
    add_bookmarks(title, meta_data)
    clean()
    if Action.NOTIFY_COMPLETION in input_data.actions:
        print("Process Complete")