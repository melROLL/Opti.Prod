from tkinter import *
from tkinter.ttk import *
from time import strftime
import time
import configparser
from PIL import Image, ImageTk
from tkinter import messagebox
from pymodbus.client import ModbusTcpClient
import threading
import os

class AddPlaceWindow(Toplevel):
    '''
    Class for 'Add place' menu.
    '''

    def __init__(self, parent):
        super().__init__(parent)  # Call initialisation method of the parent class
        self.parent = parent  # Set parent window
        self.title("Add Place")  # Set window title
        self.geometry("300x370")  # Set window size

        # Calculate the position of the window so that it is in the centre of the main window
        # Update the main window to ensure dimensions are calculated correctly
        parent.update_idletasks()
        parent_width = parent.winfo_width()  # Get the width of the main window
        parent_height = parent.winfo_height()  # Get the height of the main window
        x = parent.winfo_rootx() + parent_width // 2 - self.winfo_width() // 2
        y = parent.winfo_rooty() + parent_height // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")  # Set window position so that it is centred

        # Create and place various labels and input boxes
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

        self.label_register_address = Label(
            self, text="Enter register_address : ")
        self.label_register_address.pack(pady=10)

        self.entry_register_address = Entry(self)
        self.entry_register_address.pack()

        self.label_register_count = Label(self, text="Enter register_count : ")
        self.label_register_count.pack(pady=10)

        self.entry_register_count = Entry(self)
        self.entry_register_count.pack()

        # "Add" button, click it to call add_place method
        self.add_button = Button(self, text="Add", command=self.add_place)
        self.add_button.pack(pady=10)

    def add_place(self):
        '''
        add_place method is used to handle the logic of adding a place
        '''
        # Get the data entered by the user
        place_name = self.entry_name.get()
        ip_address = self.entry_ip.get()
        port = self.entry_port.get()
        register_address = self.entry_register_address.get()
        register_count = self.entry_register_count.get()

        # Check that all fields are filled in
        if place_name and ip_address and port and register_address and register_count:
            # If all fields are filled in, write this information to the configuration file
            config = configparser.ConfigParser()  # Create a profile parser
            config.read('setting.ini')
            if place_name in config:
                # Show error message if place name already exist.
                messagebox.showerror(
                    "Error", "Place name already exist", parent=self)
            else:
                config[place_name] = {}
                config[place_name]['ip'] = ip_address
                config[place_name]['port'] = port
                config[place_name]['register_address'] = register_address
                config[place_name]['register_count'] = register_count

                # Open the configuration file for writing
                with open('setting.ini', 'w') as configfile:
                    # Write configuration information
                    config.write(configfile, space_around_delimiters=True)

                # Close the window when you're done adding and refresh the parent window's list box
                self.destroy()
                self.parent.refresh_listbox()
        else:
            # Display an error message if a field is not filled in.
            messagebox.showerror(
                "Error", "All fields must be filled.", parent=self)


class ModifyPlaceWindow(Toplevel):
    '''
    Class for 'Modify place' menu.
    '''
    def __init__(self, parent, selected_item):
        # Initialize the window
        super().__init__(parent)
        self.parent = parent
        self.title("Modify Place")
        self.geometry("300x370")

        # Position the window in the center of the parent window
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        x = parent.winfo_rootx() + parent_width // 2 - self.winfo_width() // 2
        y = parent.winfo_rooty() + parent_height // 2 - self.winfo_height() // 2
        self.geometry(f"+{x}+{y}")
        self.place_name = selected_item

        # Create and pack widgets
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

        self.label_register_address = Label(
            self, text="Enter register_address : ")
        self.label_register_address.pack(pady=10)

        self.entry_register_address = Entry(self)
        self.entry_register_address.pack()

        self.label_register_count = Label(self, text="Enter register_count : ")
        self.label_register_count.pack(pady=10)

        self.entry_register_count = Entry(self)
        self.entry_register_count.pack()

        # Create a button for applying modifications
        self.modify_button = Button(
            self, text="Modify", command=self.modify_place)
        self.modify_button.pack(pady=10)

        # Load existing information at initialization
        self.load_existing_info()

    def load_existing_info(self):
        # Read existing information from 'setting.ini' and populate the fields
        config = configparser.ConfigParser()
        config.read('setting.ini')
        if self.place_name in config:
            place_info = config[self.place_name]
            # Populate the name entry with the selected place name
            self.entry_name.insert(0, self.place_name)
            # Populate the IP address entry
            self.entry_ip.insert(0, place_info.get('ip', ''))
            self.entry_port.insert(0, place_info.get(
                'port', ''))   # Populate the port entry
            self.entry_register_address.insert(0, place_info.get(
                'register_address', ''))   # Populate the register address entry
            self.entry_register_count.insert(
                0, place_info.get('register_count', ''))    # Populate the register count entry

    def modify_place(self):
        # Retrieve user input from the form fields
        place_name = self.entry_name.get()
        ip_address = self.entry_ip.get()
        port = self.entry_port.get()
        register_address = self.entry_register_address.get()
        register_count = self.entry_register_count.get()

        if place_name and ip_address and port and register_address and register_count:
            # Validate and update the information in 'setting.ini' if all fields are filled
            config = configparser.ConfigParser()
            config.read('setting.ini')
            if self.place_name in config:
                # Remove existing section before updating
                config.remove_section(self.place_name)
            config[place_name] = {}
            config[place_name]['ip'] = ip_address
            config[place_name]['port'] = port
            config[place_name]['register_address'] = register_address
            config[place_name]['register_count'] = register_count

            with open('setting.ini', 'w') as configfile:
                config.write(configfile, space_around_delimiters=True)

            # Close the window and refresh the parent form
            self.destroy()
            self.parent.refresh_listbox()
        else:
            # Show an error message if any field is empty
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
        self.label_vars = []  # List to store StringVar instances
        self.labels = []  # List to store Label widgets
        for i in range(4):
            # Create different StringVar instances for Temp, Flux, P inject, and P attend
            label_var1 = StringVar()  
            label_var2 = StringVar() 
            label_var3 = StringVar()
            label_var4 = StringVar()
            # Initial value for labels
            init = 0
            self.label_vars.append(label_var1)
            self.label_vars.append(label_var2)
            self.label_vars.append(label_var3)
            self.label_vars.append(label_var4)
            # Create and configure labels based on the iteration
            if i == 0:
                label1 = self.__create_label1(
                    self, f"Temp: {init} C°", label_var1)
                label2 = self.__create_label2(
                    self, f"P inject: {init} kW", label_var2)
                label3 = self.__create_label3(
                    self, f"Flux: {init} W/m²", label_var3)
                label4 = self.__create_label4(
                    self, f"Pression: {init} Pa", label_var4)
            if i == 1:
                label1 = self.__create_label1(
                    self, f"Temp2: {init} C°", label_var1)
                label2 = self.__create_label2(
                    self, f"P attend: {init} kW", label_var2)
                label3 = self.__create_label3(
                    self, f"Hum: {init} %", label_var3)
                label4 = self.__create_label4(
                    self, f"Gaz R: {init} ohm", label_var4)
            self.labels.extend([label1, label2, label3, label4])  # Add labels to the list
        self.state_label = self.__state_label(self, 'State :')
        self.state_img_label = self.__state_img_label(self)
        self.surface_var = StringVar()
        self.surface_label = self.__create_surface_label(
            self, f"Surface: {init} m²", self.surface_var)
        self.place_var = StringVar()
        self.place_var.set('Please Select')
        self.place_label = self.__Place_label(self, '')
        # Bind the place_var to the text of the place_label
        self.place_label.config(
            textvariable=self.place_var, anchor='center', justify='center')
        self.update_time()  # Update the time continuously

    def __win(self):
        self.title("Solar Panel Application")
        # Set window size and center it on the screen
        width = 600
        height = 350
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
                                    (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)
        

    def scrollbar_autohide(self, bar, widget):
        # Automatically hide the scrollbar
        self.__scrollbar_hide(bar, widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar, widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar, widget))

    def __scrollbar_show(self, bar, widget):
         # Show the scrollbar
        bar.lift(widget)

    def __scrollbar_hide(self, bar, widget):
        # Hide the scrollbar
        bar.lower(widget)

    def vbar(self, ele, x, y, w, h, parent):
        # Create a vertical scrollbar
        sw = 15   # Scrollbar width
        x = x + w - sw
        vbar = Scrollbar(parent)
        ele.configure(yscrollcommand=vbar.set)
        vbar.config(command=ele.yview)
        vbar.place(x=x, y=y, width=sw, height=h)
        self.scrollbar_autohide(vbar, ele)

    def load_settings(self):
        # Load settings from 'setting.ini'
        config = configparser.ConfigParser()
        config_path = 'setting.ini'
        if not os.path.exists(config_path):
            # Create a default configuration if the file doesn't exist
            config['Test'] = {
                'ip': '11.1.1.1',
                'port': '111',
                'register_address': '0x00',
                'register_count': '11'
            }
            with open(config_path, 'w') as configfile:
                config.write(configfile)
        config.read(config_path)
        sections = config.sections()
        sorted_sections = sorted(sections)
        for section in sorted_sections:
            self.tk_list_box_main.insert(END, section)  # Populate the list box with settings sections

    def __tk_list_box_main(self, parent):
         # Create and configure the main list box
        lb = Listbox(parent)
        lb.place(x=30, y=50, width=150, height=220)
        return lb

    def __tk_button_info(self, parent):
         # Create and configure the 'Info' button
        btn = Button(
            parent,
            text=">",
            takefocus=False,
        )
        btn.place(x=190, y=115, width=50, height=100)
        return btn

    def __tk_button_add(self, parent):
        # Create and configure the 'Add' button
        btn = Button(
            parent,
            text="Add",
            takefocus=False,
        )
        btn.place(x=30, y=300, width=70, height=35)
        return btn

    def __tk_button_delete(self, parent):
        # Create and configure the 'Delete' button
        btn = Button(
            parent,
            text="Delete",
            takefocus=False,
        )
        btn.place(x=110, y=300, width=70, height=35)
        return btn

    def __tk_button_modify(self, parent):
        # Create and configure the 'Modify' button
        btn = Button(
            parent,
            text="Modify",
            takefocus=False,
        )
        btn.place(x=60, y=10, width=90, height=35)
        return btn

    # Functions to create and configure various labels in the GUI
    def __create_label1(self, parent, text, var):
        label = Label(
            parent,
            textvariable=var,
            font=("Helvetica", 13)
        )
        label.place(x=250, y=100 + len(self.labels) * 10) 
        var.set(text) 
        return label

    def __create_label2(self, parent, text, var):
        label = Label(
            parent,
            textvariable=var,
            font=("Helvetica", 13)
        )
        label.place(x=425, y=100 + len(self.labels) * 10) 
        var.set(text)
        return label

    def __create_label3(self, parent, text, var):
        label = Label(
            parent,
            textvariable=var, 
            font=("Helvetica", 13)
        )
        label.place(x=250, y=175 + len(self.labels) * 10) 
        var.set(text) 
        return label

    def __create_label4(self, parent, text, var):
        label = Label(
            parent,
            textvariable=var,
            font=("Helvetica", 13)
        )
        label.place(x=425, y=175 + len(self.labels) * 10)
        var.set(text) 
        return label

    def __state_label(self, parent, text):
        label = Label(
            parent,
            text=text,
            font=("Helvetica", 15)
        )
        label.place(x=300, y=290) 
        return label

    def __state_img_label(self, parent):
        label = Label(
            parent,
            font=("Helvetica", 16)
        )
        label.place(x=400, y=277) 
        return label

    def __Place_label(self, parent, text):
        label = Label(
            parent,
            text=text,
            font=("Helvetica", 16)
        )
        label.place(x=350, y=50) 
        return label

    def __time_label(self, parent):
        # Create and configure the time label
        time_label = Label(
            parent,
            text="",
            font=("Helvetica", 20)
        )
        time_label.place(x=450, y=10) 
        return time_label

    def __create_surface_label(self, parent, text, var):
        # Create and configure the surface label
        label = Label(
            parent,
            textvariable=var, 
            font=("Helvetica", 10)
        )
        label.place(x=250, y=55)  # Position the surface label
        var.set(text)
        return label

    def update_time(self):
        # Update the current time on the time label every second
        current_time = strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Schedule the next update in 1 second

    def add_item():
        # Add an item to the listbox
        item = entry.get()
        if item:
            listbox.insert(END, item)
            entry.delete(0, END)

    def remove_item(self):
        # Remove the selected item from the listbox
        selected_index = self.tk_list_box_main.curselection()
        if selected_index:
            selected_item = self.tk_list_box_main.get(selected_index[0])

            # Ask for confirmation before deletion
            confirm = messagebox.askyesno(
                "Confirmation", f"Do you want to delete '{selected_item}'?")

            if confirm:
                # If confirmed, remove the selected item from the Listbox
                self.tk_list_box_main.delete(selected_index)
                # Remove the corresponding configuration information from the setting.ini file.
                config = configparser.ConfigParser()
                config.read('setting.ini')
                if selected_item in config:
                    config.remove_section(selected_item)
                    with open('setting.ini', 'w') as configfile:
                        config.write(configfile)
                    # Reread settings, update configuration variables
                    self.config = self.Read_settings()

    def refresh_listbox(self):
        self.tk_list_box_main.delete(0, END)  # Clear all items in the Listbox
        self.load_settings()  # Reload the data from the setup file and display it

    def modify_item(self):
        selected_index = self.tk_list_box_main.curselection() # Get the index of the selected item
        if selected_index:
            selected_item = self.tk_list_box_main.get(selected_index[0]) # Get the text content of the selected item
            modify_place_window = ModifyPlaceWindow(self, selected_item) # Create a modification window and pass in the current item's data
        self.config = self.Read_settings() # Read settings, update configuration variables


class Win(WinGUI):
    '''
    Classes for GUI applications
    '''
    def __init__(self): # Initialisation methods
        super().__init__()                      # Call initialisation method of the parent class
        self.client = None                      # Initialise Modbus client to None
        self.config = self.Read_settings()      # Read the configuration file
        self.keep_updating = False              # Control asynchronous update flags
        self.modbus_thread = None               # Initialise Modbus thread to None
        self.__event_bind()                     # Bind event handler methods

    def set_image(self, image_path): # Method of setting up an image
        try: # Trying to open and display images
            img = Image.open(image_path)            # Open an image file
            img = ImageTk.PhotoImage(img)           # Convert an image to a PhotoImage object
            self.state_img_label.config(image=img)  # Update the image of the label
            self.state_img_label.image = img        # Maintain references to images
        except Exception as e:
            print(f"Can't load image: {e}")

    def update_label_async(self, client, register_address, register_count): # Asynchronous update of tags
        while self.keep_updating and client.is_socket_open(): # Loop over until you stop updating
            result = client.read_holding_registers(register_address, register_count, slave=1) # Read Modbus registers
            if result.isError():     
                print(f"Modbus error: {result}")
                if "No response received, expected at least 8 bytes (0 received)" in str(result):
                    self.keep_updating = False 
                    messagebox.showwarning("Warning","Modbus disconnected.")
            else:
                self.after(0, lambda: self.update_labels_with_result(result)) # Updated tag content
            time.sleep(0.5) # Pause for a while

    def update_labels_with_result(self, result): # Methods for updating labels with Modbus reading results
        # Set the value of each tag
        self.label_vars[0].set(f"Temp: {result.registers[0]} C°")
        self.label_vars[1].set(f"P inject: {result.registers[6]} kW")
        self.label_vars[4].set(f"Temp2: {result.registers[5]} C°")
        self.label_vars[5].set(f"P attend: {result.registers[7]} kW")
        self.label_vars[2].set(f"Flux: {result.registers[4]} W/m²")
        self.label_vars[3].set(f"Pression: {result.registers[1]} Pa")
        self.label_vars[6].set(f"Hum: {result.registers[3]} %")
        self.label_vars[7].set(f"Gaz R: {result.registers[2]} ohm")
        self.surface_var.set(f"Surface: {result.registers[9]} m²")

        # Update status images based on specific register values
        if result.registers[8] == 1:
            self.set_image('./img/green.png')
        elif result.registers[8] == 0:
            self.set_image('./img/red.gif')
        else:
            self.set_image('./img/gray.png')

    def Read_settings(self): # Read the settings of the
        config = configparser.ConfigParser()
        config.read('setting.ini')
        return config

    def LoadInfo(self, evt): # Methods of loading information
        self.keep_updating = False
        if self.modbus_thread and self.modbus_thread.is_alive():
            self.modbus_thread.join()
        self.modbus_thread = None

        selected_index = self.tk_list_box_main.curselection()
        if selected_index:
            selected_item = self.tk_list_box_main.get(selected_index[0])
            self.place_var.set(f'{selected_item}')
            if selected_item in self.config:
                ip = str(self.config[selected_item].get('ip', '0'))
                port = int(self.config[selected_item].get('port', '0'))
                register_address = int(self.config[selected_item].get('register_address', '0'), 16)
                register_count = int(self.config[selected_item].get('register_count', '0'))

            if self.client and self.client.is_socket_open():
                self.client.close()
                self.client = None

            try_time = 0
            connection_successful = False

            # Connect the Modbus client according to the selected configuration and start updating labels asynchronously
            while try_time < 3 and not connection_successful:
                self.client = ModbusTcpClient(ip, port=port)
                if self.client.connect():
                    print('connected')
                    self.keep_updating = True
                    connection_successful = True
                else:
                    try_time += 1
                    self.client.close()
                    if try_time == 3:
                        messagebox.showinfo("Connection failed", "Connection failed.\nPlease check the ip address or your internet.")

            if connection_successful:
                self.keep_updating = True
                self.modbus_thread = threading.Thread(target=self.update_label_async, args=(self.client, register_address, register_count))
                self.modbus_thread.daemon = True
                self.modbus_thread.start()

    def AddPlace(self, evt): # Method of adding locations
        add_place_window = AddPlaceWindow(self)
        self.config = self.Read_settings()

    def __event_bind(self): # Private methods for binding events
        self.tk_button_info.bind('<Button>',
                                self.LoadInfo)
        self.tk_button_add.bind('<Button>', self.AddPlace)
        self.tk_button_delete.bind('<Button-1>', lambda event: self.remove_item())
        self.tk_button_modify.bind('<Button-1>', lambda event: self.modify_item())
        pass


if __name__ == "__main__": # Launch the application.
    win = Win()
    win.mainloop()
