# Shree KRISHNAya Namaha
# Graphical Interface
# Author: Nagabhushan S N
import json
import os
import tkinter
from tkinter import Button, Checkbutton, Entry, Frame, Label, filedialog
from tkinter.filedialog import askopenfilename

from data.DataStructures import InputData
from data.Enums import Action


class NotesManagerGui(Frame):
    def __init__(self, parent=None, fill_input_data: InputData = None, execute_callback=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.execute_callback = execute_callback
        self.pack()
        self.winfo_toplevel().title('Images to PDF Generator')

        if fill_input_data is None:
            fill_input_data = InputData(None, None, None, 0, [], True)

        self.res_frame = FileChooserFrame(self)
        self.res_frame.pack()
        self.add_res_frame(fill_input_data)

        self.actions_frame = ActionsFrame(self)
        self.actions_frame.pack()
        self.add_actions(fill_input_data)

        self.inputs_frame = InputsFrame(self, fill_input_data=fill_input_data)
        self.inputs_frame.pack()

        button = Button(self, text='Execute', command=self.execute)
        button.pack()

    def add_res_frame(self, fill_input_data: InputData):
        self.res_frame.add_component('Bookmarks: ', fill_input_data.bookmarks_filepath)
        self.res_frame.add_component('Meta Data: ', fill_input_data.metadata_filepath)
        self.res_frame.add_component('Directory: ', fill_input_data.images_directory_path, file_chooser=False)

    def add_actions(self, fill_input_data: InputData):
        self.actions_frame.add_action(Action.RENAME_IMAGES, Action.RENAME_IMAGES in fill_input_data.actions)
        self.actions_frame.add_action(Action.SCALE_TO_A4, Action.SCALE_TO_A4 in fill_input_data.actions)
        self.actions_frame.add_action(Action.CONVERT_TO_PDF, Action.CONVERT_TO_PDF in fill_input_data.actions)
        self.actions_frame.add_action(Action.MERGE_PDF, Action.MERGE_PDF in fill_input_data.actions)
        self.actions_frame.add_action(Action.ADD_BOOKMARKS, Action.ADD_BOOKMARKS in fill_input_data.actions)
        self.actions_frame.add_action(Action.CLEAN_TEMP_FILES, Action.CLEAN_TEMP_FILES in fill_input_data.actions)
        self.actions_frame.add_action(Action.NOTIFY_COMPLETION, Action.NOTIFY_COMPLETION in fill_input_data.actions)
        self.actions_frame.add_buttons()

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
        self.save_state(input_data)
        self.execute_callback(input_data)

    @staticmethod
    def save_state(input_data: InputData):
        serialised_dict = {key: str(value) for key, value in input_data.__dict__.items()}
        if not os.path.exists('./pdf_generator/AppData/'):
            os.makedirs('./pdf_generator/AppData/')
        with open('./pdf_generator/AppData/saved_state.txt', 'w') as state_file:
            state_file.write(json.dumps(serialised_dict))
        print('State saved.')


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

    def add_action(self, action_name, default_state=False):
        var = tkinter.IntVar()
        var.set(default_state)
        checkbutton = Checkbutton(self, text=action_name, variable=var)
        checkbutton.pack(anchor=tkinter.W)
        self.components.append((checkbutton, var))

    def add_buttons(self):
        select_all_button = Button(self, text='Select All', command=self.check_all_buttons)
        select_all_button.pack()
        select_none_button = Button(self, text='Select None', command=self.uncheck_all_buttons)
        select_none_button.pack()

    def check_all_buttons(self):
        for component in self.components:
            component[0].select()

    def uncheck_all_buttons(self):
        for component in self.components:
            component[1].set(0)


class InputsFrame(Frame):
    def __init__(self, parent=None, fill_input_data=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.components = []
        self.add_components(fill_input_data)

    def add_components(self, fill_input_data: InputData):
        if fill_input_data and fill_input_data.rotate_angle:
            fill_rotate_angle = fill_input_data.rotate_angle
        else:
            fill_rotate_angle = '0'
        rotate_label = Label(self, text='Rotate Angle (in degrees)')
        rotate_label.grid(row=0, column=0)
        rotate_entry = Entry(self)
        rotate_entry.insert(0, fill_rotate_angle)
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


def read_saved_state(args_input_data: InputData) -> InputData:
    saved_state_dict = {}
    if os.path.exists('pdf_generator/AppData/saved_state.txt'):
        with open('pdf_generator/AppData/saved_state.txt') as state_file:
            saved_state_dict = json.loads(state_file.readline())
    saved_input_data = InputData.from_dict(saved_state_dict)
    args_input_data.remove_invalid_fields()
    saved_input_data.remove_invalid_fields()
    fill_input_data = InputData.merge(args_input_data, saved_input_data)
    return fill_input_data


def main(args_input_data: InputData, execute_callback):
    print('GUI started')
    fill_input_data = read_saved_state(args_input_data)
    root = tkinter.Tk()
    NotesManagerGui(root, fill_input_data, execute_callback)
    root.mainloop()
