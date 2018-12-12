# Shree KRISHNAya Namaha
# Graphical Interface
# Author: Nagabhushan S N
import tkinter
from tkinter import Button, Entry, Frame, Label, filedialog
from tkinter.filedialog import askopenfilename


class NotesManagerGui(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.winfo_toplevel().title('Images to PDF Generator')

        self.res_frame = FileChooserFrame(self)
        self.res_frame.pack()
        self.add_res_frame()

    def add_res_frame(self):
        self.res_frame.add_component('Bookmarks: ')
        self.res_frame.add_component('Meta Data: ')
        self.res_frame.add_component('Directory: ', file_chooser=False)


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


def main():
    print('GUI started')
    root = tkinter.Tk()
    NotesManagerGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
