# Shree KRISHNAya Namaha

import os
import re


def generate_page_nos(input_string):
	# Split input string
	tokens = re.split('(\W)', input_string)
	tokens = filter(lambda a: a != '', tokens)
	
	num_levels = calc_num_levels(input_string)
	levels = [0]*num_levels
	page_nos = []
	current_level = 0
	
	for i in range(0, len(tokens)):
		current_element = tokens[i]
		if i != len(tokens)-1:
			next_element = tokens[i+1]
		if current_element == '{':
			current_level += 1
			levels[current_level-1] += 1
		elif current_element.isdigit():
			if next_element == '{':
				continue
			elif next_element == ',' or next_element == '}':
				synthesize_page_nos(levels, current_level, current_element, page_nos)
		elif current_element == ',':
			levels[current_level - 2] += 1
			reset_levels(levels, current_level - 1)
		elif current_element == '}':
			current_level -= 1
	
	return page_nos


def calc_num_levels(input_string):
	level = max_level = 0
	for char in input_string:
		if char == '{':
			level += 1
			if level > max_level:
				max_level = level
		elif char == '}':
			level -= 1
	return max_level
			
	
def synthesize_page_nos(levels, current_level, num_pages, page_nos):
	for i in range(0, int(num_pages)):
		page_no = ''
		for j in range(0, current_level-1):
			page_no += '{:02d}'.format(levels[j]) + '.'
		page_no += '{:02d}'.format(i+1)
		page_nos.append(page_no)


def reset_levels(levels, start_level):
	for i in range(start_level, len(levels)):
		levels[i] = 1


def rename_files(page_nos):
	i = 0
	os.chdir(directory)
	for fileName in sorted(os.listdir('.')):
		print(fileName)
		os.rename(fileName, title + ' - ' + page_nos[i] + '.pdf')
		i += 1


input_data = '{6{3{0,8,0},3{0,14,0},3{0,4,0},3{0,8,0},3{0,3,0},3}}'
title = 'Control Systems - BE 5th Sem - My Notes'
directory = './PDFs/'
page_numbers = generate_page_nos(input_data)
rename_files(page_numbers)
