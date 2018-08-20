#! /urs/bin/env python

import codecs
import os
import subprocess
import bluetooth

def arduinoCommandBuilder(ard_cmd):
    """ Turns the user command into something readable for the Arduino """
    ard_cmd = "<" + ard_cmd + ">" #format for commands sent to arduino
    hex_repr = "".join(r'\x{0:x}'.format(ord(c)) for c in ard_cmd)
    temp = codecs.decode(hex_repr,'unicode_escape') #raw string is connverted back to regular string 
    return temp


def startBluetoothController():
    """Sends commands """
    print("Hello, User. You have three options for modes:\n1. test")
    print("2. terminal\n3. arduino\nEnter \"stop\" to end the program.\n\n")

    bd_dev = "00:06:66:DC:93:9D" #Blue Smirf device that's connected to an Arduino
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_dev, port))
    
    while 1:   
        mode_cmd = str(input("Please, enter your mode command.\n>>"))
        if mode_cmd == "test":
            result1 = sock.send(bytes(arduinoCommandBuilder(mode_cmd),'UTF-8'))
            print("Number of bytes sent: ",result1)
        elif mode_cmd == "terminal":
            print("The current directory is ", os.getcwd())ar
            print(subprocess.check_call((str(input("\nEnter your terminal command:\n>>"))),shell=True))
        elif mode_cmd == "arduino":
            print("Enter one of the following Arduino commands:\n")
            print("1. display 'msg'  note: replace msg with the message that you want to display.")
            print("2. insult \n3. noise")
            ard_cmd = str(input("\n>>"))
            result2 = sock.send(bytes(arduinoCommandBuilder(ard_cmd),'UTF-8'))
            print("Number of bytes sent: ",result2)
        elif mode_cmd == "stop":
            break
        else:
            print("You did not enter a valid option.\n")

    sock.close() #make sure to always exit out of loop to prevent weird bluetooth errors on PI


if __name__ == "__main__":
    startBluetoothController()
