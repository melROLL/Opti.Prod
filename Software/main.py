# import tkinter as tk
# from tkinter import ttk
# from pymodbus.client.sync import ModbusTcpClient
# import threading
# import time

# def read_modbus_data():
#     # 从界面获取用户选择的地区
#     selected_area = area_combobox.get()
    
#     # 从配置文件中获取选定地区的Modbus参数
#     modbus_parameters = config[selected_area]
    
#     # 连接到Modbus服务器
#     client = ModbusTcpClient(modbus_parameters['ip'], modbus_parameters['port'])
    
#     # 读取Modbus寄存器数据
#     response = client.read_holding_registers(modbus_parameters['register_address'],
#                                              modbus_parameters['register_count'])
    
#     if response.isError():
#         result_label.config(text="Modbus读取错误")
#     else:
#         data = response.registers
#         temperature_label.config(text=f"Temperature: {data[0]}")
#         flux_label.config(text=f"Flux solaire: {data[1]}")
#         puissance_injectee_label.config(text=f"Puissance injectée: {data[2]}")
#         puissance_attendu_label.config(text=f"Puissance attendue: {data[3]}")
#         alarmes_active_label.config(text=f"Code alarmes active: {data[4]}")
    
#     # 断开与Modbus服务器的连接
#     client.close()

# def update_data_periodically():
#     while True:
#         read_modbus_data()
#         # 定时器间隔（秒）
#         time.sleep(10)  # 10秒钟更新一次数据

# # 创建Tkinter窗口
# root = tk.Tk()
# root.title("Modbus数据读取")

# # 创建下拉栏以选择地区
# area_label = tk.Label(root, text="选择地区:")
# area_label.pack()
# area_combobox = ttk.Combobox(root, values=["地区1", "地区2", "地区3"])  # 你可以根据你的配置文件来添加更多地区
# area_combobox.pack()

# # 创建按钮来触发Modbus数据读取
# read_button = tk.Button(root, text="读取数据", command=read_modbus_data)
# read_button.pack()

# # 创建用于显示Modbus数据的标签
# temperature_label = tk.Label(root, text="Temperature:")
# temperature_label.pack()
# flux_label = tk.Label(root, text="Flux solaire:")
# flux_label.pack()
# puissance_injectee_label = tk.Label(root, text="Puissance injectée:")
# puissance_injectee_label.pack()
# puissance_attendu_label = tk.Label(root, text="Puissance attendue:")
# puissance_attendu_label.pack()
# alarmes_active_label = tk.Label(root, text="Code alarmes active:")
# alarmes_active_label.pack()

# # 从配置文件中加载地区参数
# config = {
#     "地区1": {
#         "ip": "Modbus服务器IP1",
#         "port": 502,
#         "register_address": 0,
#         "register_count": 5
#     },
#     "地区2": {
#         "ip": "Modbus服务器IP2",
#         "port": 502,
#         "register_address": 10,
#         "register_count": 5
#     },
#     # 添加更多地区的配置参数
# }

# # 创建一个定时器线程来定期更新数据
# update_thread = threading.Thread(target=update_data_periodically)
# update_thread.daemon = True
# update_thread.start()

# root.mainloop()

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from pymodbus.client.sync import ModbusTcpClient
import threading
import time
import json

# 设置文件名
SETTINGS_FILE = 'setting.json'


def load_settings():
    """从文件中加载设置"""
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_settings(config):
    """保存设置到文件"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(config, f, indent=4)

class EditAreaDialog(simpledialog.Dialog):
    """自定义对话框用于编辑已有地区的信息"""
    
    def __init__(self, parent, area_data):
        self.area_data = area_data
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text="地区名字:").grid(row=0, column=0)
        self.area_name_entry = tk.Entry(master)
        self.area_name_entry.insert(0, self.area_data['area_name'])
        self.area_name_entry.grid(row=0, column=1)

        tk.Label(master, text="IP地址:").grid(row=1, column=0)
        self.ip_entry = tk.Entry(master)
        self.ip_entry.insert(0, self.area_data['ip'])
        self.ip_entry.grid(row=1, column=1)

        tk.Label(master, text="端口:").grid(row=2, column=0)
        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0, self.area_data['port'])
        self.port_entry.grid(row=2, column=1)

        tk.Label(master, text="寄存器地址:").grid(row=3, column=0)
        self.register_address_entry = tk.Entry(master)
        self.register_address_entry.insert(0, self.area_data['register_address'])
        self.register_address_entry.grid(row=3, column=1)

        tk.Label(master, text="寄存器数量:").grid(row=4, column=0)
        self.register_count_entry = tk.Entry(master)
        self.register_count_entry.insert(0, self.area_data['register_count'])
        self.register_count_entry.grid(row=4, column=1)

        return self.area_name_entry

    def apply(self):
        self.result = {
            "area_name": self.area_name_entry.get(),
            "ip": self.ip_entry.get(),
            "port": int(self.port_entry.get()),
            "register_address": int(self.register_address_entry.get()),
            "register_count": int(self.register_count_entry.get())
        }

class AddAreaDialog(simpledialog.Dialog):
    """自定义对话框用于输入新地区的信息"""

    def body(self, master):
        self.title("添加新地区")

        tk.Label(master, text="地区名字:").grid(row=0, column=0)
        self.area_name_entry = tk.Entry(master)
        self.area_name_entry.grid(row=0, column=1)

        tk.Label(master, text="IP地址:").grid(row=1, column=0)
        self.ip_entry = tk.Entry(master)
        self.ip_entry.grid(row=1, column=1)

        tk.Label(master, text="端口:").grid(row=2, column=0)
        self.port_entry = tk.Entry(master)
        self.port_entry.grid(row=2, column=1)

        tk.Label(master, text="寄存器地址:").grid(row=3, column=0)
        self.register_address_entry = tk.Entry(master)
        self.register_address_entry.grid(row=3, column=1)

        tk.Label(master, text="寄存器数量:").grid(row=4, column=0)
        self.register_count_entry = tk.Entry(master)
        self.register_count_entry.grid(row=4, column=1)

        return self.area_name_entry  # Initial focus

    def apply(self):
        self.result = {
            "area_name": self.area_name_entry.get(),
            "ip": self.ip_entry.get(),
            "port": int(self.port_entry.get()),
            "register_address": int(self.register_address_entry.get()),
            "register_count": int(self.register_count_entry.get())
        }


def add_area():
    """添加新地区"""
    dialog = AddAreaDialog(root)
    if hasattr(dialog, "result"):
        config[dialog.result['area_name']] = {
            "ip": dialog.result['ip'],
            "port": dialog.result['port'],
            "register_address": dialog.result['register_address'],
            "register_count": dialog.result['register_count']
        }
        save_settings(config)
        update_listbox()




def delete_area():
    """删除指定地区"""
    area_to_delete = area_listbox.get(tk.ACTIVE)
    if area_to_delete:
        if messagebox.askyesno("确认", f"你确定要删除 {area_to_delete} 吗?"):
            del config[area_to_delete]
            save_settings(config)
            update_listbox()


# def update_area_combobox():
#     """更新下拉列表框的地区"""
#     area_combobox['values'] = list(config.keys())
#     if area_combobox['values']:
#         area_combobox.current(0)

def update_listbox():
    """更新Listbox的地区内容"""
    area_listbox.delete(0, tk.END)
    for area in config.keys():
        area_listbox.insert(tk.END, area)


def edit_area():
    selected_indices = area_listbox.curselection()
    if not selected_indices:
        return
    selected_index = selected_indices[0]
    selected_area_name = area_listbox.get(selected_index)
    
    area_data = config[selected_area_name].copy()
    area_data['area_name'] = selected_area_name
    dialog = EditAreaDialog(root, area_data)
    
    if hasattr(dialog, "result"):
        # 更新config字典并保存设置
        new_area_name = dialog.result['area_name']
        del config[selected_area_name]  # 删除旧的地区名
        config[new_area_name] = dialog.result
        del config[new_area_name]['area_name']  # 不要在config中保存地区名字段
        save_settings(config)
        update_listbox()

def read_modbus_data():
    """读取Modbus数据并更新界面"""
    selected_indices = area_listbox.curselection()
    if not selected_indices:
        # No item is selected
        return
    selected_index = selected_indices[0]
    selected_area = area_listbox.get(selected_index)

    modbus_parameters = config[selected_area]
    client = ModbusTcpClient(modbus_parameters['ip'], modbus_parameters['port'])
    
    response = client.read_holding_registers(modbus_parameters['register_address'],
                                             modbus_parameters['register_count'])
    
    if response.isError():
        result_label.config(text="Modbus读取错误")
    else:
        data = response.registers
        temperature_label.config(text=f"Temperature: {data[0]}")
        flux_label.config(text=f"Flux solaire: {data[1]}")
        puissance_injectee_label.config(text=f"Puissance injectée: {data[2]}")
        puissance_attendu_label.config(text=f"Puissance attendue: {data[3]}")
        alarmes_active_label.config(text=f"Code alarmes active: {data[4]}")
        result_label.config(text="数据已更新")
    
    client.close()

def update_time_label():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    time_label.config(text=current_time)
    root.after(1000, update_time_label)  # 每秒更新一次

def update_data_periodically():
    """定期更新Modbus数据"""
    while True:
        read_modbus_data()
        time.sleep(10)


# 加载设置
config = load_settings()

# 创建Tkinter窗口
root = tk.Tk()
root.title("Modbus数据读取")

# 创建一个frame来放置控件
frame = tk.Frame(root)
frame.pack(pady=20, padx=20, anchor="w") 

# 左边的地区Listbox
area_listbox = tk.Listbox(frame, height=10, width=20)
area_listbox.grid(row=0, column=0, rowspan=6, padx=(0, 20))
update_listbox()

# 中间的操作按钮
read_button = tk.Button(frame, text="读取数据", command=read_modbus_data, width=15)
read_button.grid(row=0, column=1, pady=(0, 10))

add_button = tk.Button(frame, text="添加地区", command=add_area, width=15)
add_button.grid(row=1, column=1, pady=10)

delete_button = tk.Button(frame, text="删除地区", command=delete_area, width=15)
delete_button.grid(row=2, column=1, pady=10)

edit_button = tk.Button(frame, text="编辑地区", command=edit_area, width=15)
edit_button.grid(row=3, column=1, pady=10)

# 右边显示Modbus数据的标签
# 在右边显示Modbus数据的标签部分上方

labels_frame = tk.Frame(frame)
labels_frame.grid(row=0, column=2, rowspan=6, padx=(20, 0))

time_label = tk.Label(labels_frame, text="")
time_label.pack(pady=5)
temperature_label = tk.Label(labels_frame, text="Temperature:")
temperature_label.pack(pady=5)
flux_label = tk.Label(labels_frame, text="Flux solaire:")
flux_label.pack(pady=5)
puissance_injectee_label = tk.Label(labels_frame, text="Puissance injectée:")
puissance_injectee_label.pack(pady=5)
puissance_attendu_label = tk.Label(labels_frame, text="Puissance attendue:")
puissance_attendu_label.pack(pady=5)
alarmes_active_label = tk.Label(labels_frame, text="Code alarmes active:")
alarmes_active_label.pack(pady=5)

# 用于显示读取结果或错误的标签
result_label = tk.Label(root, text="")
result_label.pack(pady=20)

# 创建一个定时器线程来定期更新数据
update_thread = threading.Thread(target=update_data_periodically)
update_thread.daemon = True
update_thread.start()


update_time_label() 

root.geometry("800x250")
root.mainloop()