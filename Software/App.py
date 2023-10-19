from tkinter import *
from tkinter.ttk import *
from time import strftime
import configparser
from PIL import Image, ImageTk
from tkinter import messagebox
class AddPlaceWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Place")
        self.geometry("300x370")  # 设置窗口尺寸

        # 计算窗口的位置，使其位于主窗口中央
        parent.update_idletasks()  # 确保主窗口的尺寸已计算
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        x = parent.winfo_rootx() + parent_width // 2 - self.winfo_width() // 2
        y = parent.winfo_rooty() + parent_height // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")  # 设置窗口位置

        self.label_name = Label(self, text="Enter place name : ")
        self.label_name.pack(pady=10)

        self.entry_name = Entry(self)
        self.entry_name.pack()

        self.label_ip = Label(self, text="Enter IP address : ")
        self.label_ip.pack(pady=10)

        self.entry_ip = Entry(self)
        self.entry_ip.pack()

        self.label_port = Label(self, text="Enter Port : ")
        self.label_port.pack(pady=10)

        self.entry_port = Entry(self)
        self.entry_port.pack()

        self.label_register_address = Label(self, text="Enter register_address : ")
        self.label_register_address.pack(pady=10)

        self.entry_register_address = Entry(self)
        self.entry_register_address.pack()

        self.label_register_count = Label(self, text="Enter register_count : ")
        self.label_register_count.pack(pady=10)

        self.entry_register_count = Entry(self)
        self.entry_register_count.pack()

        self.add_button = Button(self, text="Add", command=self.add_place)
        self.add_button.pack(pady=10)

    def add_place(self):
        place_name = self.entry_name.get()
        ip_address = self.entry_ip.get()
        port = self.entry_port.get()
        register_address = self.entry_register_address.get()
        register_count = self.entry_register_count.get()

        if place_name and ip_address and port and register_address and register_count:
            # 使用 configparser 写入信息到 setting.ini 文件
            config = configparser.ConfigParser()
            config.read('setting.ini')
            config[place_name] = {}
            config[place_name]['alpha'] = ip_address
            config[place_name]['beta'] = port
            config[place_name]['charli'] = register_address
            config[place_name]['delta'] = register_count
            config[place_name]['ether'] = '500'

            with open('setting.ini', 'w') as configfile:
                config.write(configfile, space_around_delimiters=True)

            # 关闭窗口
            self.destroy()
            self.parent.refresh_listbox()
        else:
            messagebox.showerror("Error", "All fields must be filled.")

class ModifyPlaceWindow(Toplevel):
    def __init__(self, parent, selected_item):
        super().__init__(parent)
        self.parent = parent
        self.title("Modify Place")
        self.geometry("300x370")
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        x = parent.winfo_rootx() + parent_width // 2 - self.winfo_width() // 2
        y = parent.winfo_rooty() + parent_height // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")
        self.place_name = selected_item
        self.label_name = Label(self, text="Enter place name : ")
        self.label_name.pack(pady=10)

        self.entry_name = Entry(self)
        self.entry_name.pack()

        self.label_ip = Label(self, text="Enter IP address : ")
        self.label_ip.pack(pady=10)

        self.entry_ip = Entry(self)
        self.entry_ip.pack()

        self.label_port = Label(self, text="Enter Port : ")
        self.label_port.pack(pady=10)

        self.entry_port = Entry(self)
        self.entry_port.pack()

        self.label_register_address = Label(self, text="Enter register_address : ")
        self.label_register_address.pack(pady=10)

        self.entry_register_address = Entry(self)
        self.entry_register_address.pack()

        self.label_register_count = Label(self, text="Enter register_count : ")
        self.label_register_count.pack(pady=10)

        self.entry_register_count = Entry(self)
        self.entry_register_count.pack()

        self.modify_button = Button(self, text="Modify", command=self.modify_place)
        self.modify_button.pack(pady=10)

        # 在初始化时加载现有信息
        self.load_existing_info()

    def load_existing_info(self):
        # 从setting.ini文件中读取现有信息并填充到输入框中
        config = configparser.ConfigParser()
        config.read('setting.ini')
        if self.place_name in config:
            place_info = config[self.place_name]
            self.entry_name.insert(0, self.place_name)  # 插入地点名称到输入框中
            self.entry_ip.insert(0, place_info.get('alpha', ''))
            self.entry_port.insert(0, place_info.get('beta', ''))
            self.entry_register_address.insert(0, place_info.get('charli', ''))
            self.entry_register_count.insert(0, place_info.get('delta', ''))

    def modify_place(self):
        # 获取用户输入的信息
        place_name = self.entry_name.get()
        ip_address = self.entry_ip.get()
        port = self.entry_port.get()
        register_address = self.entry_register_address.get()
        register_count = self.entry_register_count.get()

        if place_name and ip_address and port and register_address and register_count:
            # 使用 configparser 更新信息到 setting.ini 文件
            config = configparser.ConfigParser()
            config.read('setting.ini')
            if self.place_name in config:
                # 先删除原有的信息
                config.remove_section(self.place_name)
            config[place_name] = {}
            config[place_name]['alpha'] = ip_address
            config[place_name]['beta'] = port
            config[place_name]['charli'] = register_address
            config[place_name]['delta'] = register_count
            config[place_name]['ether'] = '500'  # 500、404 或其他状态值

            with open('setting.ini', 'w') as configfile:
                config.write(configfile, space_around_delimiters=True)

            # 关闭窗口
            self.destroy()
            self.parent.refresh_listbox()
        else:
            messagebox.showerror("Error", "All fields must be filled.")
class WinGUI(Tk):

    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_list_box_main = self.__tk_list_box_main(self)
        self.load_settings()
        self.tk_button_info = self.__tk_button_info(self)
        self.tk_button_add = self.__tk_button_add(self)
        self.tk_button_delete = self.__tk_button_delete(self)
        self.tk_button_modify = self.__tk_button_modify(self)
        self.time_label = self.__time_label(self)
        self.label_vars = []  # 用于存储StringVar的列表
        self.labels = []  # 用于存储标签的列表
        for i in range(2):
            label_var1 = StringVar()  # 为Temp和Flux创建不同的StringVar
            label_var2 = StringVar()  # 为P inject和P attend创建不同的StringVar
            init = 0
            self.label_vars.append(label_var1)
            self.label_vars.append(label_var2)
            if i == 0:
                label1 = self.__create_label1(self, f"Temp: {init} C°", label_var1)
                label2 = self.__create_label2(self, f"P inject: {init} kW", label_var2)
            if i == 1:
                label1 = self.__create_label1(self, f"Flux: {init} W/m²", label_var1)
                label2 = self.__create_label2(self, f"P attend: {init} kW", label_var2)
            self.labels.extend([label1, label2])  # 添加标签到列表中
        self.state_label = self.__state_label(self, 'State :')
        self.state_img_label = self.__state_img_label(self)
        self.place_var = StringVar()
        self.place_var.set('Please Select')
        self.place_label = self.__Place_label(self,'')
        self.place_label.config(textvariable=self.place_var, anchor='center', justify='center')  # 绑定place_var到place_label的文本
        self.update_time()

    def __win(self):
        self.title("Solar Panel Application")
        # 设置窗口大小、居中
        width = 600
        height = 350
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        # 自动隐藏滚动条
    def scrollbar_autohide(self, bar, widget):
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        bar.lower(widget)

    def vbar(self, ele, x, y, w, h, parent):
        sw = 15  # Scrollbar 宽度
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar, ele)

    def load_settings(self):
        config = configparser.ConfigParser()
        config.read('setting.ini')
        sections = config.sections()
        sorted_sections = sorted(sections)
        for section in sorted_sections:
            self.tk_list_box_main.insert(END, section)

    def __tk_list_box_main(self, parent):
        lb = Listbox(parent)
        lb.place(x=30, y=50, width=150, height=220)
        return lb

    def __tk_button_info(self, parent):
        btn = Button(
            parent,
            text=">",
            takefocus=False,
        )
        btn.place(x=190, y=115, width=50, height=100)
        return btn

    def __tk_button_add(self, parent):
        btn = Button(
            parent,
            text="Add",
            takefocus=False,
        )
        btn.place(x=30, y=300, width=70, height=35)
        return btn

    def __tk_button_delete(self, parent):
        btn = Button(
            parent,
            text="Delete",
            takefocus=False,
        )
        btn.place(x=110, y=300, width=70, height=35)
        return btn

    def __tk_button_modify(self, parent):
        btn = Button(
            parent,
            text="Modify",
            takefocus=False,
        )
        btn.place(x=60, y=10, width=90, height=35)
        return btn

    def __create_label1(self, parent, text, var):
        label = Label(
            parent,
            textvariable=var,  # 将StringVar与标签绑定
            font=("Helvetica", 13)
        )
        label.place(x=275, y=150 + len(self.labels) * 30)  # 调整标签的位置
        var.set(text)  # 设置初始文本
        return label

    def __create_label2(self, parent, text, var):
        label = Label(
            parent,
            textvariable=var,  # 将StringVar与标签绑定
            font=("Helvetica", 13)
        )
        label.place(x=425, y=150 + len(self.labels) * 30)  # 调整标签的位置
        var.set(text)  # 设置初始文本
        return label

    def __state_label(self, parent, text):
        label = Label(
            parent,
            text=text,
            font=("Helvetica", 15)
        )
        label.place(x=300, y=270)  # 调整标签的位置
        return label

    def __state_img_label(self, parent):
        label = Label(
            parent,
            font=("Helvetica", 16)
        )
        label.place(x=400, y=257)  # 调整标签的位置
        return label

    def __Place_label(self, parent, text):
        label = Label(
            parent,
            text=text,
            font=("Helvetica", 16)
        )
        label.place(x=360, y=80)  # 调整标签的位置
        return label

    def __time_label(self, parent):
        time_label = Label(
            parent,
            text="",
            font=("Helvetica", 20)
        )
        time_label.place(x=450, y=10)  # 调整时间标签的位置
        return time_label

    def update_time(self):
        current_time = strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)

    def add_item():
        item = entry.get()
        if item:
            listbox.insert(END, item)
            entry.delete(0, END)

    def remove_item(self):
        selected_index = self.tk_list_box_main.curselection()
        if selected_index:
            selected_item = self.tk_list_box_main.get(selected_index[0])

            # 弹出确认对话框
            confirm = messagebox.askyesno("Confirmation", f"Do you want to delete '{selected_item}'?")

            if confirm:
                # 从Listbox中删除项目
                self.tk_list_box_main.delete(selected_index)
                # 从setting.ini文件中删除相应的配置信息
                config = configparser.ConfigParser()
                config.read('setting.ini')
                if selected_item in config:
                    config.remove_section(selected_item)
                    with open('setting.ini', 'w') as configfile:
                        config.write(configfile)

    def refresh_listbox(self):
        self.tk_list_box_main.delete(0, END)  # 清空Listbox
        self.load_settings()  # 重新加载数据

    def modify_item(self):
        selected_index = self.tk_list_box_main.curselection()
        if selected_index:
            selected_item = self.tk_list_box_main.get(selected_index[0])
            modify_place_window = ModifyPlaceWindow(self, selected_item)

class Win(WinGUI):

    def __init__(self):
        super().__init__()
        self.__event_bind()

    def set_image(self, image_path):
        try:
            # 使用Pillow打开GIF图像文件
            img = Image.open(image_path)
            # 将图像转换为Tkinter支持的格式
            img = ImageTk.PhotoImage(img)
            # 更新状态标签以显示图像
            self.state_img_label.config(image=img)
            # 需要保持对图像对象的引用，否则图像会被垃圾回收
            self.state_img_label.image = img
        except Exception as e:
            print(f"无法加载图像: {e}")

    def LoadInfo(self, evt):
            # 获取listbox中选定的项
            selected_index = self.tk_list_box_main.curselection()
            if selected_index:
                selected_item = self.tk_list_box_main.get(selected_index[0])
                self.place_var.set(f'{selected_item}')
                # 从setting.ini文件中读取相应的数据
                config = configparser.ConfigParser()
                config.read('setting.ini')

                if selected_item in config:
                    alpha = config[selected_item].get('alpha', 'N/A')
                    beta = config[selected_item].get('beta', 'N/A')
                    charli = config[selected_item].get('charli', 'N/A')
                    delta = config[selected_item].get('delta', 'N/A')
                    ether = config[selected_item].get('ether', 'N/A')

                    # 更新标签上的文本
                    self.label_vars[0].set(f"Temp: {alpha} C°")
                    self.label_vars[1].set(f"P inject: {charli} kW")
                    self.label_vars[2].set(f"Flux: {beta} W/m²")
                    self.label_vars[3].set(f"P attend: {delta} kW")
                    # 设置文本颜色
                    if ether == '500':
                        self.set_image('./img/green.png')  # 用于表示“Correct”状态的GIF图像
                    elif ether == '404':
                        self.set_image('./img/red.gif')  # 用于表示“Alert”状态的GIF图像
                    else:
                        self.set_image('./img/gray.png')  # 用于表示“Unknown”状态的GIF图像

    def set_text_color(self, text, color):
        self.state_text.config(state=NORMAL)
        self.state_text.delete('1.0', END)
        self.state_text.insert(END, text)
        self.state_text.tag_configure(color, foreground=color)
        self.state_text.tag_add(color, '1.0', 'end')
        self.state_text.config(state=DISABLED)

    def blink_text(self, text, color):
        if self.state_text.cget("state") != NORMAL:
            self.set_text_color(text, color)
        else:
            self.state_text.config(state=HIDDEN)
            self.after(500, lambda: self.blink_text(text, color))


    def AddPlace(self, evt):
        add_place_window = AddPlaceWindow(self)

    def __event_bind(self):
        self.tk_button_info.bind('<Button>', self.LoadInfo)
        self.tk_button_add.bind('<Button>', self.AddPlace)
        self.tk_button_delete.bind('<Button-1>', lambda event: self.remove_item())
        self.tk_button_modify.bind('<Button-1>', lambda event: self.modify_item())
        pass

if __name__ == "__main__":
    win = Win()
    win.mainloop()
