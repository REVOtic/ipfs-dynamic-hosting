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

hashes = []
local_files = []

t = TraceConsole()





def pins_from_database():
    t.log('Ading everything from website to local repository')
    r = requests.get(url="http://13.66.133.71:8000/jsony", headers={'Connection':'close'})
    data = r.json()
    data = data['array']
    str = ""
    for hash in data:
        if hash['ids'] not in hashes:
            status = os.system("ipfs pin add " + hash['ids'])
            hashes.append(hash['ids'])
            local_files.append(hash['ids'])
            if status != 0:
                str = str + hash['ids'] + " " + "Not pinned yet \n"
    top.after(20000, pins_from_database)

def view():
    t.log('displaying files that are pinned to local node from website')
    logger = logging.getLogger(__name__)
    logger.info(_('Done!'))
    str = ""
    for hash in hashes:
        str = str + hash + "\n"
    t.log(str)
    if str == "":
        L2.config(text="oops")
    else:
        L2.config(text=str)

def view1():
    t.log('displaying files that are pinned to local node')
    logger = logging.getLogger(__name__)
    logger.info(_('Done!'))
    str = ""
    for hash in local_files:
        str = str + hash + "\n"
    t.log(str)
    if str == "":
        L2.config(text="No file is there")
    else:
        L2.config(text=str)

def pin():
    t.log('Pinning hash seperately')
    logger = logging.getLogger(__name__)
    logger.info(_('Done!'))
    hash = Entry.get(E1)
    print(hash)
    t.log(hash + ' to be pinned')
    try:
        status = os.system("ipfs pin add " + hash)
        if hash not in local_files:
            local_files.append(hash)
        if status!=0:
            L4.config(text="Pinning not Successful")
            t.log('Pinning is successful')
        else:
            L4.config(text="Pinning Successful")
            t.log('Pinning is not successful')
    except tkinter.TclError:
        L4.config(text="Error in pinning")

def unpin():
    t.log('Unpinning hash')
    logger = logging.getLogger(__name__)
    logger.info(_('Done!'))
    hash = Entry.get(E2)
    t.log(hash + ' to be unpinned')
    try:
        status = os.system("ipfs pin rm " + hash)
        if hash in local_files:
            local_files.remove(hash)
        if status!=0:
            L4.config(text="Unpinning not Successful")
            t.log('Unpinning is successful')
        else:
            L4.config(text="Unpinning Successful")
            t.log('Unpinning is not successful')
    except tkinter.TclError:
        L4.config(text="Error in unpinning")
#
def daemon():
    t.log('IPFS Daemon about to start')
    logger = logging.getLogger(__name__)
    logger.info(_('Done!'))
    os.system("ipfs daemon")



def start_daemon():
    t.log('hello world!')
    logger = logging.getLogger(__name__)
    logger.info(_('Done!'))
    new_window = Toplevel(top)
    SD = Button(new_window,text="start_daemon",command = start).grid(row=0,column=0)
    L7 = Label(new_window, ).grid(row=1,column=0)


# pin_all()
global top
top = tkinter.Tk()

def main():
    t.log('Main method starting ipfs daemon')
    logger = logging.getLogger(__name__)
    logger.info(_('Done!'))
    multiprocessing.freeze_support()
    pool = Pool(processes=1)
    P1 = pool.apply_async(daemon())

if __name__ == '__main__':
    main()

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


