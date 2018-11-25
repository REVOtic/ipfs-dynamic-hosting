import tkinter
import requests
import os
import time
from tkinter import *
import multiprocessing
from multiprocessing import *
import gettext
_ = gettext.gettext
import logging
from TraceConsole import *
import time

hashes = []
local_files = []

t = TraceConsole()
time = time.time()
name = str(time) + ".txt"
f= open(name,"w+")

logging.basicConfig(filename=name,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


def pins_from_database():
    t.log('Adding everything from website to local repository')
    logging.info('Adding everything from website to local repository')
    r = requests.get(url="http://13.66.133.71:8000/jsony", headers={'Connection':'close'})
    data = r.json()
    data = data['array']
    str1 = ""
    for hash in data:
        if hash['ids'] not in hashes:
            status = os.system("ipfs pin add " + hash['ids'])
            hashes.append(hash['ids'])
            local_files.append(hash['ids'])
            if status != 0:
                str1 = str1 + hash['ids'] + " " + "Not pinned yet \n"
    top.after(20000, pins_from_database)

def view():
    t.log('displaying files that are pinned to local node from website')
    logging.info('displaying files that are pinned to local node from website')
    str1 = ""
    for hash in hashes:
        str1 = str1 + hash + "\n"
    t.log(str1)
    logging.info(str1)
    if str1 == "":
        L2.config(text="oops")
    else:
        L2.config(text=str1)

def view1():
    t.log('displaying files that are pinned to local node')
    logging.info('displaying files that are pinned to local node')
    str1 = ""
    for hash in local_files:
        str1 = str1 + hash + "\n"
    t.log(str1)
    logging.info(str1)
    if str1 == "":
        L2.config(text="No file is there")
    else:
        L2.config(text=str1)

def pin():
    t.log('Pinning hash seperately')
    logging.info('Pinning hash seperately')
    hash = Entry.get(E1)
    print(hash)
    t.log(hash + ' to be pinned')
    logging.info(hash + ' to be pinned')
    try:
        status = os.system("ipfs pin add " + hash)
        if hash not in local_files:
            local_files.append(hash)
        if status!=0:
            L4.config(text="Pinning not Successful")
            t.log('Pinning is not successful')
            logging.info('Pinning is not successful')
        else:
            L4.config(text="Pinning Successful")
            t.log('Pinning is successful')
            logging.info('Pinning is successful')
    except tkinter.TclError:
        L4.config(text="Error in pinning")

def unpin():
    t.log('Unpinning hash')
    logging.info('Unpinning hash')
    hash = Entry.get(E2)
    t.log(hash + ' to be unpinned')
    logging.info(hash + ' to be unpinned')
    try:
        status = os.system("ipfs pin rm " + hash)
        if hash in local_files:
            local_files.remove(hash)
        if status!=0:
            L4.config(text="Unpinning not Successful")
            t.log('Unpinning is not successful')
            logging.info('Unpinning is not successful')
        else:
            L4.config(text="Unpinning Successful")
            t.log('Unpinning is successful')
            logging.info('Unpinning is successful')
    except tkinter.TclError:
        L4.config(text="Error in unpinning")

global top
top = tkinter.Tk()

L1 = Label(top, text="FILES PINNED TO LOCAL REPOSITORY FROM WEBSITE                       ").grid(row=0,column=0)
B=Button(top, text ="View File Hashes",command = view).grid(row=1,column=0)
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
L7 = Label(top, text="FILES PRESENT IN LOCAL NODE                       ").grid(row=9,column=0)
B=Button(top, text ="View File Hashes",command = view1).grid(row=10,column=0)
L3 = Label(top,)
L3.grid(row=11,column=0)
top.after(20000, pins_from_database)

top.mainloop()

