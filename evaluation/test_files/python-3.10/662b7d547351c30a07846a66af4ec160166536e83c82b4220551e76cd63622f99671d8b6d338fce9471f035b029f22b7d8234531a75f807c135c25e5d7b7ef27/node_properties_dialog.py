from tkinter import Tk, StringVar, Label, Entry, Button

class NodePropertiesDialog:

    def __init__(self, node, update=None, title=''):
        self.node = node
        self.update = update
        self.master = Tk()
        self.master.title(title)
        row = 0
        self.name_var = StringVar(self.master)
        self.name_var.set(node.name)
        name_label = Label(self.master, text='Name: ')
        name_entry = Entry(self.master, textvariable=self.name_var)
        name_label.grid(row=row)
        name_entry.grid(row=row, column=1)
        row += 1
        button = Button(self.master, text='OK', command=self.on_update)
        button.grid(row=row)

    def on_update(self):
        self.node.name = self.name_var.get()
        self.master.destroy()
        if self.update:
            self.update(self.node)