# Shree KRISHNAya Namaha


class FunctionData:

	def __init__(self, functions, help=None):
		self.functions = functions
		self.help = help

	def __str__(self):
		string = '[ '
		for function in self.functions:
			string += function.__name__
			string += ','
		string = string[:-1]
		string += ' ]'
		return string


class CompleteData:

	def __init__(self, input_data, functions_data):
		self.input_data = input_data
		self.functions_data = functions_data
