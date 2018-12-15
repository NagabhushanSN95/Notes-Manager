# Shree KRISHNAya Namaha
# Common Utility Functions
# Author: Nagabhushan

import shlex
import subprocess
from tkinter import Tk, messagebox


def prompt(prompt_string):
    response = input(prompt_string)
    return response.lower() in 'yes'


def yes_no_prompt(prompt_string, gui: bool = False):
    if gui:
        root = Tk()
        root.withdraw()
        response = messagebox.askyesno(message=prompt_string)
        root.destroy()
    else:
        response = (input(prompt_string + " [Y/n]:")).lower() in 'yes'
    if response:
        return True
    else:
        return False


def display_message(message_string: str, gui: bool = False):
    if gui:
        root = Tk()
        root.withdraw()
        messagebox.showinfo(message=message_string)
        root.destroy()
    else:
        print(message_string)


def execute_cmd(cmd, print_cmd=False):
    if print_cmd:
        print("terminal$ " + cmd)
    if isinstance(cmd, list):
        commands = cmd
    else:
        commands = shlex.split(cmd)
    output = subprocess.Popen(commands, stdout=subprocess.PIPE).communicate()[0]
    return output
