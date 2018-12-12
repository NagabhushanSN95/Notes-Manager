# Shree KRISHNAya Namaha
# Starting point
# Author: Nagabhushan S N

import argparse
import math
import os
import shlex
import shutil
import subprocess

import GUI


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


def delete_temp_dir():
	# Remove temporary directory ./temp if it exists
	if os.path.exists("./temp"):
		if (prompt("Directory temp already exists. It needs to be removed to proceed. "
					"Do you want to remove it now? [Y/n]:")):
			shutil.rmtree("./temp")
		else:
			print("Exiting program...")
			exit()


def setup_args():
	parser = argparse.ArgumentParser(description='Create PDF from images')
	parser.add_argument('--bookmarks', '-b', help="Bookmarks file (default: ./Bookmarks.txt",
						type=str, default='./Bookmarks.txt')
	parser.add_argument('--meta-data', '-md', help="Meta-Data file (default: ./Meta-Data.txt",
						type=str, default='./Meta-Data.txt')
	parser.add_argument('--directory', '-d', help="Path to directory containing images (default: ./Images/)",
						type=str, default='./Images')
	parser.add_argument('--scaleA4', '-s', help="Scale images to A4 size. Whitespace will be padded if required",
						action='store_true')
	parser.add_argument('--rotate', '-r', help="Angle in degrees to rotate all the images clockwise (default: 0)",
						type=str, default=0)
	parser.add_argument('--gui', '-g', help="Start GUI (Graphical User Interface)", action='store_true')
	args = parser.parse_args()
	return args


def start_interactor(args: argparse.ArgumentParser):
	if args.gui:
		GUI.main()
	else:
		print('CLI not yet added')


def main():
	delete_temp_dir()
	args = setup_args()
	start_interactor(args)


if __name__ == '__main__':
	main()
