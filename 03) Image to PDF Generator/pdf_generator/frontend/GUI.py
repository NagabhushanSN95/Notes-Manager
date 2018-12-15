# Shree KRISHNAya Namaha
# Graphical Interface
# Author: Nagabhushan S N

import tkinter
from tkinter import Button, Checkbutton, Entry, Frame, Label, filedialog
from tkinter.filedialog import askopenfilename

from data.DataStructures import InputData
from data.Enums import Action


class NotesManagerGui(Frame):
    def __init__(self, parent=None, execute_callback=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.execute_callback = execute_callback
        self.pack()
        self.winfo_toplevel().title('Images to PDF Generator')

        self.res_frame = FileChooserFrame(self)
        self.res_frame.pack()
        self.add_res_frame()

        self.actions_frame = ActionsFrame(self)
        self.actions_frame.pack()
        self.add_actions()

        self.inputs_frame = InputsFrame(self)
        self.inputs_frame.pack()

        button = Button(self, text='Execute', command=self.execute)
        button.pack()

    def add_res_frame(self):
        self.res_frame.add_component('Bookmarks: ')
        self.res_frame.add_component('Meta Data: ')
        self.res_frame.add_component('Directory: ', file_chooser=False)

    def add_actions(self):
        self.actions_frame.add_action(Action.RENAME_IMAGES)
        self.actions_frame.add_action(Action.SCALE_TO_A4)
        self.actions_frame.add_action(Action.CONVERT_TO_PDF)
        self.actions_frame.add_action(Action.MERGE_PDF)
        self.actions_frame.add_action(Action.ADD_BOOKMARKS)
        self.actions_frame.add_action(Action.CLEAN_TEMP_FILES)
        self.actions_frame.add_action(Action.NOTIFY_COMPLETION)

    def execute(self):
        bookmarks_filename = self.res_frame.components[0][1].get()
        metadata_filename = self.res_frame.components[1][1].get()
        images_directory = self.res_frame.components[2][1].get()
        if not images_directory.endswith('/'):
            images_directory = images_directory + '/'
        actions = []
        for action_component in self.actions_frame.components:
            if action_component[1].get() == 1:
                action = Action.get_action(action_component[0].cget('text'))
                actions.append(action)
        rotate_angle = self.inputs_frame.components[0][1].get()
        self.parent.destroy()
        input_data = InputData(bookmarks_filename, metadata_filename, images_directory, rotate_angle, actions, True)
        self.execute_callback(input_data)


class FileChooserFrame(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.components = []

    def add_component(self, label_name, entry_name=None, button_name='Browse', file_chooser=True):
        row_num = len(self.components)
        label = Label(self, text=label_name)
        label.grid(row=row_num, column=0)
        entry = Entry(self)
        entry.grid(row=row_num, column=1)
        button = Button(self, text=button_name, command=lambda: self.load_file(row_num, file_chooser))
        button.grid(row=row_num, column=2)

        if entry_name:
            entry.insert(0, entry_name)
        self.components.append((label, entry, button))

    def load_file(self, row_num, file_chooser=True):
        if file_chooser:
            filename = askopenfilename(filetypes=(("Text files", "*.txt"),
                                                  ("All files", "*.*")))
        else:
            filename = filedialog.askdirectory()
        if filename:
            self.components[row_num][1].delete(0, tkinter.END)
            self.components[row_num][1].insert(0, filename)


class ActionsFrame(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.components = []

    def add_action(self, action_name):
        var = tkinter.IntVar()
        checkbutton = Checkbutton(self, text=action_name, variable=var)
        checkbutton.pack(anchor=tkinter.W)
        self.components.append((checkbutton, var))


class InputsFrame(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.components = []
        self.add_components()

    def add_components(self):
        rotate_label = Label(self, text='Rotate Angle (in degrees)')
        rotate_label.grid(row=0, column=0)
        rotate_entry = Entry(self)
        rotate_entry.insert(0, '0')
        rotate_entry.grid(row=0, column=1)
        rotate_cc_label = Label(self, text='counter-clockwise')
        rotate_cc_label.grid(row=0, column=2)
        self.components.append((rotate_label, rotate_entry))


class ButtonsFrame(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.components = []

    def add_button(self, button_name, button_function):
        button = Button(self, text=button_name, command=button_function)
        button.pack()
        self.components.append(button)


def main(execute_function):
    print('GUI started')
    root = tkinter.Tk()
    NotesManagerGui(root, execute_function)
    root.mainloop()
