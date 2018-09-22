#! /usr/bin/env python3

# notes:
#  -will require the user to download BlueZ for python
#  -might require reconfiguration of bluetooth settings
#  -must use the disconnect button before ending GUI application

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
        self.connectSock()
        self.createButtons()
    
    def configureWindow(self):
        """ Sets the title, size, and label of window """
        self.master.title("Bluetooth Controller App")
        self.master.geometry('400x200')
        self.createLabelMessage()
        
        self.main_label = tk.Label(self,textvariable=self.menu_message)
        self.main_label.pack(side="top")
        
        self.return_msg_label = tk.Label(self,textvariable=self.return_message)
        self.return_msg_label.pack(side="top")

    def createLabelMessage(self):
        temp1 = "Hello, User. This app allows you to send "
        temp2 = "messages over\nbluetooth to an Arduino. There are 2 commands:"
        temp3 = "\n1. test     2. arduino"
        self.default_menu_message = temp1 + temp2 + temp3
        
        self.menu_message = tk.StringVar(self)
        self.menu_message.set(self.default_menu_message)
        
        self.return_message = tk.StringVar(self)

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

    def connectSock(self):
        """ Connects to Blue Smirf device that's connected to an Arduino"""
        self.bd_dev = "00:06:66:DC:93:9D" 
        self.port = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((self.bd_dev, self.port))

    def startBluetoothControl(self, sock, mode_cmd=""):
        """Non-looping bluetooth controller function that returns number of bytes."""
        return_msg = ""
        if mode_cmd == "test":
            result1 = sock.send(bytes(arduinoCommandBuilder(mode_cmd),'UTF-8'))
            return_msg = "Number of bytes sent: " + str(result1)
        elif mode_cmd == "arduino":
            print("Enter one of the following Arduino commands:\n")
            print("1. display 'msg'  note: replace msg with the message that you want to display.")
            print("2. insult \n3. noise")
            ard_cmd = str(input("\n>>"))
            result2 = sock.send(bytes(arduinoCommandBuilder(ard_cmd),'UTF-8'))
            return_msg= "Number of bytes sent: " + str(result2)
        else:
            return_msg = "You did not enter a valid option.\n"
        return return_msg
    
    def sendCommand(self):
        cmd = str(input("Type in your command:\n>>"))
        self.return_message.set(self.startBluetoothControl(self.sock,cmd))
        
    def disconnectSock(self):
        self.sock.close()

if __name__ == "__main__":
    root = tk.Tk()
    menu = MainMenu(master = root)
    menu.mainloop()
