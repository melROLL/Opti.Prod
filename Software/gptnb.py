from tkinter import *
from tkinter.ttk import *

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.listbox_main = self.__create_listbox(self)
        self.info_button = self.__create_info_button(self)
        self.add_button = self.__create_add_button(self)
        self.delete_button = self.__create_delete_button(self)
        self.entry_fields = self.__create_entry_fields(self)

    def __win(self):
        self.title("Solar Panel Application")
        width = 500
        height = 300
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=True, height=True)
        self.minsize(400, 200)

    def __create_listbox(self, parent):
        lb = Listbox(parent, width=20, height=10)
        lb.insert(END, "列表框")
        lb.insert(END, "Python")
        lb.insert(END, "Tkinter Helper")
        lb.pack(side=LEFT, padx=20, pady=20)
        return lb

    def __create_info_button(self, parent):
        btn = Button(parent, text=">", width=5, bg="#CCCCCC")
        btn.place(x=190, y=125)
        return btn

    def __create_add_button(self, parent):
        btn = Button(parent, text="ADD", width=10, bg="#CCCCCC")
        btn.place(x=250, y=250)
        return btn

    def __create_delete_button(self, parent):
        btn = Button(parent, text="DELETE", width=10, bg="#CCCCCC")
        btn.place(x=350, y=250)
        return btn

    def __create_entry_fields(self, parent):
        Label(parent, text="PLACE").place(x=250, y=10)
        Label(parent, text="Temp:").place(x=250, y=50)
        Entry(parent, width=20).place(x=300, y=50)
        
        Label(parent, text="Flux:").place(x=250, y=90)
        Entry(parent, width=20).place(x=300, y=90)

        Label(parent, text="ELEC:").place(x=250, y=130)
        Entry(parent, width=20).place(x=300, y=130)

        Label(parent, text="Stat:").place(x=250, y=170)
        Entry(parent, width=20).place(x=300, y=170)

        Label(parent, text="Co..d").place(x=250, y=210)
        Entry(parent, width=20).place(x=300, y=210)
        return {}

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def LoadInfo(self, evt):
        print("<Button>事件未处理:", evt)

    def AddPlace(self, evt):
        print("<Button>事件未处理:", evt)

    def __event_bind(self):
        self.info_button.bind('<Button>', self.LoadInfo)
        self.add_button.bind('<Button>', self.AddPlace)

if __name__ == "__main__":
    win = Win()
    win.mainloop()
