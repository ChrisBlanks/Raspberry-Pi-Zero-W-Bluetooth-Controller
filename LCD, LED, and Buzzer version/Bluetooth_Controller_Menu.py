#! /usr/bin/env python3

# notes:
#  -will require the user to download BlueZ for python
#  -might require reconfiguration of bluetooth settings
#  -must use the disconnect button before ending GUI application
#  -make sure to add in your own device info for connecting via bluetooth

import bluetooth
from bluetooth_controller import arduinoCommandBuilder
try:
    import tkinter as tk #python 3 option
except ImportError:
    import Tkinter as tk #python 2 option


class MainMenu(tk.Frame):
    def __init__(self,master=None):
        super(MainMenu,self).__init__(master)
        self.pack()
        self.configureWindow()
        self.createButtons()
        self.createEntry()
        self.connectSock()
        
    default_menu_message = """Hello, User. This app allows you to send 
    messages over bluetooth to an Arduino.\n There are 2 commands:
    \n1. test     2. arduino"""

    arduino_options_msg = """Enter one of the following Arduino commands:
    1. display 'msg'
    2. insult
    3. noise
    note: replace msg with the message that you want to display"""
    
    def configureWindow(self):
        """ Sets the title, size, and label of window """
        self.master.title("Bluetooth Controller App")
        self.master.geometry('400x250')
        self.createLabelMessage()
        
        self.main_label = tk.Label(self,textvariable=self.menu_message)
        self.main_label.pack(side="top")
        
        self.return_msg_label = tk.Label(self,textvariable=self.return_message)
        self.return_msg_label.pack(side="top")

    def createLabelMessage(self):
        """Creates labels that display app information """
        self.menu_message = tk.StringVar(self)
        self.menu_message.set(self.default_menu_message)
        self.return_message = tk.StringVar(self) #message used for return info in a label

    def createButtons(self):
        """Creates quit, disconnect, and command button."""
        self.quit = tk.Button(self, text="QUIT?", fg="red",command=root.destroy)
        self.quit["bg"] = "white"
        self.quit.pack(side="bottom")
        
        self.disconnect = tk.Button(self,text="disconnect bluetooth?", fg="blue",
                                    command=self.disconnectSock)
        self.disconnect["bg"] = "white"
        self.disconnect.pack(side="bottom")
        
        self.command_button = tk.Button(self,text="Send Bluetooth command",fg="black",
                                        command=self.sendCommand)
        self.command_button["bg"] = "white"
        self.command_button.pack(side="bottom")

    def createEntry(self):
        """Creates an entry field for sending commands."""
        self.entry_field = tk.Entry(self)
        self.entry_field.pack(side="top")
        self.entry_field.delete(0,tk.END)
        self.entry_field.insert(0,"Enter your command here...")
        
        self.wait_for_button_click = tk.IntVar() #used only when arduino option is selected
        
    def connectSock(self):
        """ Connects to Blue Smirf device that's connected to an Arduino"""
        self.bd_dev = "00:06:66:DC:93:9D" 
        self.port = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.bd_dev, self.port))
    
    def startBluetoothControl(self, sock, mode_cmd=""):
        """Non-looping bluetooth controller function that returns number of bytes."""
        return_msg = ""
        self.return_message.set("")
    
        if mode_cmd == "test":
            result1 = sock.send(bytes(arduinoCommandBuilder(mode_cmd),'UTF-8'))
            return_msg = "Number of bytes sent: " + str(result1)
        elif mode_cmd == "arduino":
            self.menu_message.set(self.arduino_options_msg)
            
            self.entry_field.delete(0,tk.END)
            self.command_button.configure(text="Send Bluetooth command",fg="black",
                                        command=lambda: self.wait_for_button_click.set(1))
            self.command_button.wait_variable(self.wait_for_button_click)
            ard_cmd = self.entry_field.get()

            result2 = sock.send(bytes(arduinoCommandBuilder(ard_cmd),'UTF-8'))
            return_msg= "Number of bytes sent: " + str(result2)

            #revert changes after sending message
            self.menu_message.set(self.default_menu_message)
            self.command_button.config(text="Send Bluetooth command",fg="black",
                                      command=self.sendCommand) 
        else:
            return_msg = "You did not enter a valid option.\n"
        return return_msg
    
    def sendCommand(self):
        """ Callback method for the "send command" button. Receives input from entry field"""
        cmd = self.entry_field.get()
        self.return_message.set(self.startBluetoothControl(self.sock,cmd))
        
    def disconnectSock(self):
        self.sock.close()

if __name__ == "__main__":
    
    root = tk.Tk()
    menu = MainMenu(master = root)
    menu.mainloop()
