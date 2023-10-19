import tkinter as tk
from time import strftime



root = tk.Tk()
root.title("App test")
root.minsize(750, 400)

# 使用Grid布局管理器
listbox_frame = tk.Frame(root)
listbox_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

listbox_label = tk.Label(listbox_frame, text="Items:")
listbox_label.grid(row=0, column=0, sticky="w")

listbox = tk.Listbox(listbox_frame, width=5, height=20)
listbox.grid(row=1, column=0, sticky="nsew")

entry = tk.Entry(listbox_frame)
entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

add_button = tk.Button(listbox_frame, text="Add Item", command=add_item)
add_button.grid(row=3, column=0, sticky="ew")

remove_button = tk.Button(listbox_frame, text="Remove Selected", command=remove_item)
remove_button.grid(row=4, column=0, sticky="ew")

# 设置Grid布局权重，以便随着窗口放大而调整大小
listbox_frame.columnconfigure(0, weight=1)
listbox_frame.rowconfigure(1, weight=1)

# 右侧标签显示时间（放在右上角）
time_label = tk.Label(root, font=("Cascadia Code", 20), text="")
time_label.grid(row=0, column=1, padx=10, pady=10, sticky="ne")


# 设置Grid布局权重，以便随着窗口放大而调整大小
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# 初始化并启动时间更新
update_time()

# 运行主循环
root.mainloop()
