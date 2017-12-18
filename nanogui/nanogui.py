import tkinter
from tkinter import ttk
import os
import nanoplot.NanoPlot as nanoplot
import logging
from datetime import datetime as dt
import sys
from .version import __version__
import time
from argparse import ArgumentParser
from nanogui.nanoguis import nanoPlotGui as nanoPlotGui
from nanogui.nanoguis import nanoCompGui as nanoCompGui
# from nanogui.nanoguis import nanoFiltGui as nanoFiltGui


class toolSelector(tkinter.Frame):
    def __init__(self, logfile):
        self.logfile = logfile
        s = ttk.Style()
        if 'alt' in s.theme_names():
            s.theme_use('alt')
        self.root = tkinter.Frame.__init__(self)
        self.master.title("Welcome to nanoGUI")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=10, pady=10)
        ttk.Label(self,
                  text='Which tool do you want to use?',
                  ).grid(column=0, row=0, sticky=tkinter.W, padx=3, pady=3)
        ttk.Button(self,
                   text="NanoPlot",
                   command=self.start_nanoplotgui,
                   ).grid(column=0, row=1, sticky=tkinter.W, padx=3, pady=3)
        ttk.Button(self,
                   text="NanoComp",
                   command=self.start_nanocompgui,
                   ).grid(column=0, row=2, sticky=tkinter.W, padx=3, pady=3)
        # ttk.Button(self,
        #            text="NanoFilt",
        #            command=self.start_nanofiltgui,
        #            ).grid(column=1, row=1, sticky=tkinter.W, padx=3, pady=3)

    def start_nanoplotgui(self):
        self.destroy()
        nanoplotgui(self.logfile)

    def start_nanocompgui(self):
        self.destroy()
        nanocompgui(self.logfile)

    # def start_nanofiltgui(self):
    #     self.destroy()
    #     nanofiltgui(self.logfile)


def main():
    args = get_args()
    if args.debug:
        logfile = init_logs()
    else:
        logfile = None
    toolSelector(logfile).mainloop()


def nanoplotgui(logfile):
    nanoPlotGui(logfile).mainloop()


def nanocompgui(logfile):
    nanoCompGui(logfile).mainloop()


# def nanofiltgui(logfile):
#     nanoFiltGui(logfile).mainloop()


def init_logs():
    """Initiate log file."""
    start_time = dt.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M')
    logname = os.path.join(os.path.expanduser("~") + "/nanoGUI_" + start_time + ".log")
    handlers = [logging.FileHandler(logname)]
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        handlers=handlers,
        level=logging.INFO)
    logging.info('NanoGUI {} started with NanoPlot {}'.format(__version__, nanoplot.__version__))
    logging.info('Python version is: {}'.format(sys.version.replace('\n', ' ')))
    return logname


def get_args():
    parser = ArgumentParser(description="Gui for NanoPlot".upper())
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        help="create logfile creating debug info in $HOME")
    return parser.parse_args()


if __name__ == '__main__':
    main()
