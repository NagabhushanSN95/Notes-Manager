# Shree KRISHNAya Namaha
# Graphical Interface
# Author: Nagabhushan S N

import tkinter
from tkinter import Button, Checkbutton, Entry, Frame, Label, filedialog
from tkinter.filedialog import askopenfilename

from DataStructures import InputData
from Enums import Action


class NotesManagerGui(Frame):
    def __init__(self, parent=None, execute_function=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.execute_function = execute_function
        self.pack()
        self.winfo_toplevel().title('Images to PDF Generator')

        self.res_frame = FileChooserFrame(self)
        self.res_frame.pack()
        self.add_res_frame()

        self.actions_frame = ActionsFrame(self)
        self.actions_frame.pack()
        self.add_actions()

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
                action_name = Action.get_action(action_component[0].cget('text'))
                actions.append(action_name)
        self.parent.destroy()
        # Todo: Add input for rotation angle
        input_data = InputData(bookmarks_filename, metadata_filename, images_directory, 0, actions)
        self.execute_function(input_data)


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
