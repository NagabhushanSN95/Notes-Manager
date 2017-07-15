#!/usr/bin/env python
# Shree KRISHNAya Namaha
# Author: Nagabhushan S N


# Please execute the below line in terminal before executing the Python program
# chmod u+x Image_To_PDF_Generator.py
# Execute this python file as below
# ./Image_To_PDF_Generator.py -b Bookmarks.txt -t <TITLE> -a <AUTHOR> -d ./Images/

import argparse
import os
import shutil

META_DATA_TITLE_KEY = 'Title'
META_DATA_AUTHOR_KEY = 'Author'
NUM_PAGES_CONST = 'NumPages'


def prompt(prompt_string):
	response = raw_input(prompt_string)
	if response == 'Y':
		return True
	else:
		return False


def setup_args():
	parser = argparse.ArgumentParser(description='Create PDF from images')
	parser.add_argument('--bookmarks', '-b', help="Bookmarks file (default: ./Bookmarks.txt",
						type=str, default='./Bookmarks.txt')
	parser.add_argument('--meta-data', '-md', help="Meta-Data file (default: ./Meta-Data.txt",
						type=str, default='./Meta-Data.txt')
	parser.add_argument('--directory', '-d', help="Path to directory containing images (default: ./Images/)",
						type=str, default='./Images')
	args = parser.parse_args()
	return args


def validate_inputs(args):
	# Check if Bookmarks file exists
	bookmarks_file_name = args.bookmarks
	bookmarks_file = file(bookmarks_file_name, 'r')
	if not os.path.exists(bookmarks_file):
		print("The Bookmarks file '" + bookmarks_file_name + "' doesn't exist.\n")
		print("Exiting Program...")
		exit()

	# Check if Meta-Data file exists
	meta_data_file_name = args.meta_data
	meta_data_file = file(meta_data_file_name, 'r')
	if not os.path.exists(meta_data_file):
		print("The Meta-Data file '" + meta_data_file_name + "' doesn't exist.\n")
		print("Exiting Program...")
		exit()

	# Check if Images directory exists
	images_directory_name = args.images
	images_directory = file(images_directory_name, 'r')
	if not os.path.exists(images_directory):
		print("The directory '" + images_directory_name + "' doesn't exist.\n")
		print("Exiting Program...")
		exit()


def read_inputs(args):
	bookmarks_file_name = args.bookmarks
	bookmarks_file = file(bookmarks_file_name, 'r')
	bookmarks_data = bookmarks_file.read().splitlines()
	bookmarks_data = [line.strip() for line in bookmarks_data if line.strip()]
	bookmarks_file.close()

	meta_data_file_name = args.meta_data
	meta_data_file = file(meta_data_file_name, 'r')
	meta_data_list = meta_data_file.read().splitlines()
	meta_data_list = [line.strip() for line in meta_data_list if line.strip()]
	# Convert list into a Dictionary
	meta_data = dict(map(*[iter(meta_data_list)]*2))
	meta_data_file.close()

	directory = args.directory

	return bookmarks_file_name, bookmarks_data, meta_data, directory


def generate_page_nos(bookmarks_data):
	# Split input string
	# tokens = re.split('(\n)', bookmarks_data)
	# tokens = filter(lambda a: a != '', tokens)
	# print bookmarks_data

	num_levels = calc_num_levels(bookmarks_data)
	# print num_levels

	levels = [0] * (num_levels-1)
	page_nos = []
	current_level = 0
	for i in range(0, len(bookmarks_data)):
		current_line = bookmarks_data[i]
		if current_line == '{':
			current_level += 1
			if current_level > 1:
				levels[current_level - 2] += 1
		elif NUM_PAGES_CONST in current_line:
			num_pages = extract_num_pages(current_line)
			if num_pages > 0:
				synthesize_page_nos(levels, current_level, num_pages, page_nos)
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


def synthesize_page_nos(levels, current_level, num_pages, page_nos):
	for i in range(0, int(num_pages)):
		page_no = ''
		for j in range(0, current_level - 1):
			page_no += '{:02d}'.format(levels[j]) + '.'
		page_no += '{:02d}'.format(i + 1)
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
		if current_line == '{':
			current_level += 1
		elif current_line == '}':
			current_level -= 1
		elif NUM_PAGES_CONST not in current_line:
			if (NUM_PAGES_CONST not in next_to_next_line) or (extract_num_pages(next_to_next_line) > 0):
				append_bookmark(current_line, current_level, current_page_num, meta_data)
		elif NUM_PAGES_CONST in current_line:
			current_page_num += extract_num_pages(current_line)

	# print page_nos
	return meta_data


def append_bookmark(bookmark_name, level, page_num, meta_data):
	meta_data.append("BookmarkBegin")
	meta_data.append("BookmarkTitle: " + bookmark_name)
	meta_data.append("BookmarkLevel: " + str(level))
	meta_data.append("BookmarkPageNumber: " + str(page_num))


def rename_files(directory, title, page_nos, bookmarks_file_name):
	print "Renaming Files"
	i = 0
	os.chdir(directory)
	num_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
	num_pages = len(page_nos)
	# Provide a prompt to continue or exit
	if num_files < num_pages:
		if not prompt("Warning: " + bookmarks_file_name + " lists a total of " + str(num_pages) + " pages. "
					"But the directory '" + directory + "' has only " + str(num_files) + " files."
					"Do you want to proceed? [Y/n]:"):
			exit()
	elif num_files > num_pages:
		if not prompt("Warning: " + bookmarks_file_name + " lists a total of " + str(num_pages) + " pages. " \
					"But the directory '" + directory + "' has " + str(num_files) + " files. " \
					"First " + str(num_pages) + " files will be renamed. Do you want to proceed? [Y/n]:"):
			exit()

	for fileName in sorted(os.listdir('.')):
		extension = os.path.splitext(fileName)[1]
		os.rename(fileName, title + ' - ' + page_nos[i] + extension)
		i += 1
		if i >= num_pages:
			break
	os.chdir("../")
	print "Renaming Files complete"


def convert_to_pdf(directory):
	print "Converting Images to PDFs"
	for file_name in sorted(os.listdir(directory)):
		file_name = file_name.replace(" ", "\ ")
		command = "convert " + directory + "/" + file_name + " ./temp/" + os.path.splitext(file_name)[0] + ".pdf"
		os.system(command)
	print "Converting Images to PDFs complete"


def merge_files():
	print "Merging files into single PDF"
	cmd = "pdftk "
	for file_name in sorted(os.listdir("./temp")):
		file_name = file_name.replace(" ", "\ ")
		cmd += "./temp/" + file_name + " "
	cmd += "output ./temp/merged.pdf"
	os.system(cmd)
	print "Merging complete"


def add_bookmarks(title, meta_data):
	cmd = "pdftk ./temp/merged.pdf dump_data > ./temp/meta_data.txt"
	os.system(cmd)
	meta_data_file = file("./temp/meta_data.txt", 'a')
	meta_data_file.writelines("%s\n" % item for item in meta_data)
	meta_data_file.close()
	title1 = title.replace(" ", "\ ")
	cmd = "pdftk ./temp/merged.pdf update_info ./temp/meta_data.txt output " + title1 + ".pdf"
	os.system(cmd)


def clean():
	print "Cleaning Residual and Temporary Files"
	shutil.rmtree("./temp")


def main():
	# Remove temporary directory ./temp if it exists
	if os.path.exists("./temp"):
		if(prompt("Directory temp already exists. It needs to be removed to proceed. "
						"Do you want to remove it now? [Y/n]:")):
			shutil.rmtree("./temp")
		else:
			print "Exiting program"
			exit()

	args = setup_args()
	validate_inputs(args)
	(bookmarks_file_name, bookmarks_data, meta_data_dict, directory) = read_inputs(args)
	title = meta_data_dict[META_DATA_TITLE_KEY]
	page_numbers = generate_page_nos(bookmarks_data)
	meta_data = generate_meta_data(meta_data_dict, bookmarks_data)
	rename_files(directory, title, page_numbers, bookmarks_file_name)
	os.mkdir("./temp")
	convert_to_pdf(directory)
	merge_files()
	add_bookmarks(title, meta_data)
	clean()
	print "Process Complete"

main()
