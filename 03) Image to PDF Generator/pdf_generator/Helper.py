# Shree KRISHNAya Namaha
import os
import shutil
from argparse import Namespace

META_DATA_TITLE_KEY = 'Title'
META_DATA_AUTHOR_KEY = 'Author'
NUM_PAGES_CONST = 'NumPages'
OFFSET_CONST = 'Offset'
PAGE_NOS_CONST = 'PageNos'


class PdfGenerator:

	def __init__(self, args):
		assert isinstance(args, Namespace)
		self.args = args
		(self.bookmarks_file_name, self.bookmarks_data, self.meta_data_dict, self.directory, self.rotate_degrees) = self.read_inputs()
		self.title = self.meta_data_dict[META_DATA_TITLE_KEY]
		self.page_numbers = self.generate_page_nos()
		self.meta_data = self.generate_meta_data()
		os.mkdir("./temp")

	def read_inputs(self):
		bookmarks_file_name = self.args.bookmarks
		bookmarks_file = open(bookmarks_file_name, 'r')
		bookmarks_data = bookmarks_file.read().splitlines()
		bookmarks_data = [line.strip() for line in bookmarks_data if line.strip()]
		bookmarks_file.close()

		meta_data_file_name = self.args.meta_data
		meta_data_file = open(meta_data_file_name, 'r')
		meta_data_list = meta_data_file.read().splitlines()
		meta_data_list = [line.strip() for line in meta_data_list if line.strip()]
		# Convert list into a Dictionary
		meta_data = dict(map(None, *[iter(meta_data_list)] * 2))		# Todo: Change for python3
		meta_data_file.close()

		directory = self.args.directory
		if not directory.endswith('/'):
			directory = directory + '/'
		rotate_degrees = self.args.rotate

		return bookmarks_file_name, bookmarks_data, meta_data, directory, rotate_degrees

	def rotate_files(self):
		if self.rotate_degrees != 0:
			print("Rotating files by " + self.rotate_degrees + " clockwise")
			for file_name in os.listdir(self.directory):
				cmd = 'convert ' + self.directory + file_name + ' -rotate ' + self.rotate_degrees + ' ' + self.directory + file_name
				os.system(cmd)
			print("Rotating Files complete")

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
				num_pages = self.extract_num_pages(current_line)
				if num_pages > 0:
					if (next_line is not None) and (OFFSET_CONST in next_line):
						offset = self.extract_offset(next_line)
						self.synthesize_serial_page_nos(levels, current_level, num_pages, page_nos, offset)
					else:
						self.synthesize_serial_page_nos(levels, current_level, num_pages, page_nos)
			elif PAGE_NOS_CONST in current_line:
				specific_page_nos = self.extract_page_nos(current_line)
				self.synthesize_specific_page_nos(levels, current_level, specific_page_nos, page_nos)
			elif current_line == '}':
				current_level -= 1
				self.reset_levels(levels, current_level)

		# print page_nos
		return page_nos

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

	def generate_meta_data(self):
		meta_data = list()
		meta_data.append("InfoBegin")
		meta_data.append("InfoKey: Title")
		meta_data.append("InfoValue: " + self.meta_data_dict[META_DATA_TITLE_KEY])
		meta_data.append("InfoBegin")
		meta_data.append("InfoKey: Author")
		meta_data.append("InfoValue: " + self.meta_data_dict[META_DATA_AUTHOR_KEY])
		current_level = 0
		current_page_num = 1
		for i in range(0, len(self.bookmarks_data)):
			current_line = self.bookmarks_data[i]
			if i < len(self.bookmarks_data) - 2:
				next_to_next_line = self.bookmarks_data[i + 2]
			if current_line == '{':
				current_level += 1
			elif current_line == '}':
				current_level -= 1
			elif NUM_PAGES_CONST in current_line:
				current_page_num += self.extract_num_pages(current_line)
			elif OFFSET_CONST in current_line:
				# Do Nothing
				continue
			elif PAGE_NOS_CONST in current_line:
				current_page_num += len(self.extract_page_nos(current_line))
			elif (NUM_PAGES_CONST not in next_to_next_line) or (self.extract_num_pages(next_to_next_line) > 0):
				# If NUM_PAGES_CONST is not present in next-to-next-line, then this is the name of a chapter
				# or something like that and hence has to be added in bookmarks
				# If next-to-next-line has NumPages>0, then this is the lowest level, but has pages
				# and hence this has to be added to bookmarks
				self.append_bookmark(current_line, current_level, current_page_num, meta_data)

		# print page_nos
		return meta_data

	@staticmethod
	def append_bookmark(bookmark_name, level, page_num, meta_data):
		meta_data.append("BookmarkBegin")
		meta_data.append("BookmarkTitle: " + bookmark_name)
		meta_data.append("BookmarkLevel: " + str(level))
		meta_data.append("BookmarkPageNumber: " + str(page_num))

	def rename_files(self, directory, title, page_nos, bookmarks_file_name):
		print("Renaming Files")
		i = 0
		os.chdir(directory)
		num_files = len([name for name in os.listdir('.') if os.path.isfile(name)])
		num_pages = len(page_nos)
		# Provide a prompt to continue or exit
		if num_files < num_pages:
			if not self.prompt("Warning: " + bookmarks_file_name + " lists a total of " + str(num_pages) + " pages. "
								"But the directory '" + directory + "' has only " + str(num_files) + " files."
							 	"Do you want to proceed? [Y/n]:"):
				print("Exiting program...")
				exit()
		elif num_files > num_pages:
			if not self.prompt("Warning: " + bookmarks_file_name + " lists a total of " + str(num_pages) + " pages. "
								"But the directory '" + directory + "' has " + str(num_files) + " files. "
								"First " + str(num_pages) + " files will be renamed. Do you want to proceed? [Y/n]:"):
				print("Exiting program...")
				exit()

		for file_name in sorted(os.listdir('.')):
			extension = os.path.splitext(file_name)[1]
			os.rename(file_name, title + ' - ' + page_nos[i] + extension)
			i += 1
			if i >= num_pages:
				break
		os.chdir("../")
		print("Renaming Files complete")

	@staticmethod
	def convert_to_pdf(directory):
		print("Converting Images to PDFs")
		for file_name in sorted(os.listdir(directory)):
			file_name = file_name.replace(" ", "\ ")
			command = "convert " + directory + "/" + file_name + " ./temp/" + os.path.splitext(file_name)[0] + ".pdf"
			os.system(command)
		print("Converting Images to PDFs complete")

	@staticmethod
	def merge_files():
		print("Merging files into single PDF")
		cmd = "pdftk "
		for file_name in sorted(os.listdir("./temp")):
			file_name = file_name.replace(" ", "\ ")
			cmd += "./temp/" + file_name + " "
		cmd += "output ./temp/merged.pdf"
		os.system(cmd)
		print("Merging complete")

	@staticmethod
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

	@staticmethod
	def clean():
		print("Cleaning Residual and Temporary Files")
		shutil.rmtree("./temp")

	@staticmethod
	def prompt(prompt_string):
		response = input(prompt_string)
		if response == 'Y':
			return True
		else:
			return False


class Validator:

	def __init__(self, args) -> None:
		assert isinstance(args, Namespace)
		self.args = args

	def validate_inputs(self):
		# Check if Bookmarks file exists
		bookmarks_file_name = self.args.bookmarks
		if not os.path.isfile(bookmarks_file_name):
			print("The Bookmarks file '" + bookmarks_file_name + "' doesn't exist.\n")
			print("Exiting Program...")
			exit()

		# Check if Meta-Data file exists
		meta_data_file_name = self.args.meta_data
		if not os.path.isfile(meta_data_file_name):
			print("The Meta-Data file '" + meta_data_file_name + "' doesn't exist.\n")
			print("Exiting Program...")
			exit()

		# Check if Images directory exists
		images_directory_name = self.args.directory
		if not os.path.isdir(images_directory_name):
			print("The directory '" + images_directory_name + "' doesn't exist.\n")
			print("Exiting Program...")
			exit()
