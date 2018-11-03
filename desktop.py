import tkinter
import requests
import os
import time
from tkinter import *

top = tkinter.Tk()

def pins_from_database():
    r = requests.get(url="http://13.66.133.71:3000/jsony")
    data = r.json()
    data = data['array']
    str = ""
    flag = 0
    for hash in data:
        status = os.system("ipfs pin add " + hash['ids'])
        if status != 0:
            flag = 1
            str = str + hash['ids'] + " " + "Not pinned yet \n"

    if flag == 0:
        L2.config(text="Pinning is upto date")
    else:
        L2.config(text=str)
    time.sleep(10)

def pin_all():
    r = requests.get(url="http://13.66.133.71:3000/jsony")
    data = r.json()
    data = data['array']
    for hash in data:
        os.system("ipfs pin add " + hash['ids'])
    top.after(20000, pin_all)


def pin():
    hash = Entry.get(E1)
    print(hash)
    try:
        status = os.system("ipfs pin add " + hash)
        if status!=0:
            L4.config(text="Pinning not Successful")
        else:
            L4.config(text="Pinning Successful")
    except tkinter.TclError:
        L4.config(text="Error in pinning")

def unpin():
    hash = Entry.get(E2)
    try:
        status = os.system("ipfs pin rm " + hash)
        if status!=0:
            L4.config(text="Unpinning not Successful")
        else:
            L4.config(text="Unpinning Successful")
    except tkinter.TclError:
        L4.config(text="Error in unpinning")
#
# def start_daemon():
#     try:
#         os.system("ipfs daemon &")
#         L7.config(text="Daemon running")
#     finally:
#         L7.config(text = "Daemon already running")


pin_all()
L1 = Label(top, text="FILES PINNED TO LOCAL REPOSITORY                        ").grid(row=0,column=0)
B=Button(top, text ="View Hashes",command = pins_from_database).grid(row=1,column=0)
L2 = Label(top,)
L2.grid(row=2,column=0)
L3 = Label(top, text="ENTER FILE HASH TO BE PINNED                       ").grid(row=3,column=0)
E1 = Entry(top, bd =5)
E1.grid(row=3,column=1)
B=Button(top, text ="Pin",command = pin).grid(row=4,column=0)
L4 = Label(top,)
L4.grid(row=5,column=0)
L5 = Label(top, text="ENTER FILE HASH TO BE UNPINNED                        ").grid(row=6,column=0)
E2 = Entry(top, bd =5)
E2.grid(row=6,column=1)
B=Button(top, text ="Unpin",command = unpin).grid(row=7,column=0)
L6 = Label(top,)
L6.grid(row=8,column=0)
# B=Button(top, text ="Start Daemon",command = start_daemon).grid(row=7,column=0)
# L7 = Label(top,)
# L7.grid(row=8,column=0)
top.after(20000, pin_all)
top.mainloop()