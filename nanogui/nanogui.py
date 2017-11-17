"""

Based on:


"""

import tkinter
from tkinter import ttk
from tkinter import filedialog
import os


class nanoGui(tkinter.Frame):
    def __init__(self):
        tkinter.Frame.__init__(self)
        self.master.title("Welcome to nanoGUI")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=10, pady=10)
        self.source = tkinter.StringVar()
        ttk.Label(self, text='Which data type do you want to analyze?').grid(column=0, row=0)
        sources = {"summary": 'Summary file', "fastq_rich": 'Fastq file(s)', "bam": 'Bam file'}
        for i, source in enumerate(sources.keys()):
            ttk.Radiobutton(self,
                            text=sources[source],
                            variable=self.source,
                            value=source,
                            command=self.flick_summary_options
                            ).grid(column=0, row=1 + i, sticky=tkinter.W, padx=3, pady=3)

    def select_file_and_add(self):
        targetfile = filedialog.askopenfile()
        if targetfile:
            ttk.Label(self, text=os.path.basename(targetfile.name)[:40]
                      ).grid(column=1, row=4, sticky=tkinter.W, padx=3, pady=3)
            self.target = ttk.Button(self,
                                     text='Select output directory',
                                     command=self.select_destdir_and_add
                                     ).grid(column=0, row=5, sticky=tkinter.W, padx=3, pady=3)
        return targetfile

    def select_destdir_and_add(self):
        destdir = filedialog.askdirectory()
        if destdir:
            ttk.Label(self, text=destdir
                      ).grid(column=1, row=5, sticky=tkinter.W, padx=3, pady=3)
            ttk.Button(self,
                       text="Start plotting",
                       command=start(),
                       ).grid(column=0, row=12, sticky=tkinter.W, padx=3, pady=3)
            ttk.Button(self,
                       text="More Options",
                       command=self.flick_more_options,
                       ).grid(column=0, row=13, sticky=tkinter.W, padx=3, pady=3)
        return destdir

    def flick_summary_options(self):
        if self.source.get() == "summary":
            self.subframe = ttk.Frame()
            self.subframe.grid(column=1, row=0, sticky=tkinter.W + tkinter.N, pady=10, padx=10)
            self.readtype = tkinter.StringVar(None, "1D")
            ttk.Label(self.subframe, text="Which type of sequencing?").grid(
                column=0, row=1, padx=3, pady=3)
            for i, t in enumerate(['1D', '2D', '1D2']):
                ttk.Radiobutton(self.subframe,
                                text=t,
                                variable=self.readtype,
                                value=t
                                ).grid(column=0, row=2 + i, sticky=tkinter.W, padx=3, pady=3)
            self.barcoded = tkinter.StringVar()
            ttk.Checkbutton(self.subframe,
                            text="Split barcodes",
                            variable=self.barcoded
                            ).grid(column=1, row=3, sticky=tkinter.W, padx=3, pady=3)
        else:
            if hasattr(self, "subframe"):
                self.subframe.grid_remove()
        self.target = ttk.Button(self,
                                 text='Select data file(s)',
                                 command=self.select_file_and_add
                                 ).grid(column=0, row=4, sticky=tkinter.W, padx=3, pady=3)

    def flick_more_options(self):
        if not hasattr(self, "optframe"):
            self.optframe = ttk.Frame()
            self.optframe.grid(column=0, row=14, sticky=tkinter.W + tkinter.N,  pady=10, padx=10)
            ttk.Label(self.optframe, text="Which output format?").grid(column=0, row=0, padx=20)
            self.figformat = tkinter.StringVar(None, "png")
            ttk.Radiobutton(self.optframe,
                            text='png',
                            variable=self.figformat,
                            value='png',
                            ).grid(column=0, row=1, sticky=tkinter.W, padx=20, pady=3)
            for i, t in enumerate(['svg', 'pdf', 'jpeg', 'tif', 'eps']):
                ttk.Radiobutton(self.optframe,
                                text=t,
                                variable=self.figformat,
                                value=t,
                                ).grid(column=0, row=2 + i, sticky=tkinter.W, padx=20, pady=3)
            ttk.Label(self.optframe, text="Which plotting color?").grid(column=1, row=0, padx=20)
            self.color = tkinter.StringVar(None, "blue")
            for i, c in enumerate(['blue', 'red', 'green', 'orange', "purple", "yellow"]):
                ttk.Radiobutton(self.optframe,
                                text=c,
                                variable=self.color,
                                value=c,
                                ).grid(column=1, row=1 + i, sticky=tkinter.W, padx=20, pady=3)
        else:
            self.optframe.grid_remove()
            delattr(self, "optframe")


def start():
    nanoplot()


def nanoplot():
    pass


if __name__ == '__main__':
    nanoGui().mainloop()
