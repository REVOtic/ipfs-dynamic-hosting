import tkinter as Tk

class TraceConsole():

    def __init__(self):
        # Init the main GUI window
        self._logFrame = Tk.Frame()
        self._log      = Tk.Text(self._logFrame, wrap=Tk.NONE, setgrid=True)
        self._scrollb  = Tk.Scrollbar(self._logFrame, orient=Tk.VERTICAL)
        self._scrollb.config(command = self._log.yview)
        self._log.config(yscrollcommand = self._scrollb.set)
        # Grid & Pack
        self._log.grid(column=0, row=0)
        self._scrollb.grid(column=1, row=0, sticky=Tk.S+Tk.N)
        self._logFrame.pack()


    def log(self, msg, level=None):
        # Write on GUI
        self._log.insert('end', msg + '\n')

    def exitWindow(self):
        # Exit the GUI window and close log file
        print('exit..')