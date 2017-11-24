import tkinter
from tkinter import ttk
from tkinter import filedialog
import os
import nanoplot.utils as utils
import nanoplot.NanoPlot as nanoplot
from nanoget import get_input
from nanoplotter import check_valid_format
from nanomath import write_stats
import logging
from datetime import datetime as dt
import sys
from .version import __version__
import time
import webbrowser
from argparse import ArgumentParser


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

    def start_nanoplotgui(self):
        self.destroy()
        nanoplotgui(self.logfile)

    def start_nanocompgui(self):
        self.destroy()
        nanocompgui(self.logfile)


class nanoPlotGui(tkinter.Frame):
    def __init__(self, logfile):
        self.logfile = logfile
        s = ttk.Style()
        if 'alt' in s.theme_names():
            s.theme_use('alt')
        self.root = tkinter.Frame.__init__(self)
        self.master.title("Welcome to NanoPlot")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=10, pady=10)
        self.source = tkinter.StringVar()
        self.figformat = tkinter.StringVar(None, "png")
        self.color = tkinter.StringVar(None, "blue")
        self.readtype = tkinter.StringVar(None, "1D")
        self.barcoded = tkinter.BooleanVar(None, False)
        self.loglength = tkinter.BooleanVar(None, False)
        self.n50 = tkinter.BooleanVar(None, False)
        self.maxlength = tkinter.IntVar(None, None)
        self.minqual = tkinter.IntVar(None, None)
        ttk.Label(self,
                  text='Which data type do you want to analyze?',
                  ).grid(column=0, row=0)
        sources = {"summary": 'Summary file', "fastq_rich": 'Fastq file(s)', "bam": 'Bam file'}
        for i, source in enumerate(sources.keys()):
            ttk.Radiobutton(self,
                            text=sources[source],
                            variable=self.source,
                            value=source,
                            command=self.selected_source
                            ).grid(column=0, row=1 + i, sticky=tkinter.W, padx=3, pady=3)
        ttk.Label(self, text="Which type of sequencing?").grid(
            column=1, row=0, padx=75, pady=3)
        self.readtypes = []
        for i, t in enumerate(['1D', '2D', '1D2']):
            a = ttk.Radiobutton(self,
                                text=t,
                                variable=self.readtype,
                                value=t,
                                state=tkinter.DISABLED)
            a.grid(column=1, row=1 + i, sticky=tkinter.W, padx=75, pady=3)
            self.readtypes.append(a)
        ttk.Checkbutton(self,
                        text="Split barcodes",
                        variable=self.barcoded
                        ).grid(column=2, row=2, sticky=tkinter.W, padx=3, pady=3)

    def select_file_and_add(self):
        self.targetfile = filedialog.askopenfile(initialdir=os.path.expanduser("~"))
        if self.targetfile:
            ttk.Label(self, text=os.path.basename(self.targetfile.name)[:40]
                      ).grid(column=1, row=4, sticky=tkinter.W, padx=3, pady=3)
            ttk.Button(self,
                       text='Select output directory',
                       command=self.select_destdir_and_add
                       ).grid(column=0, row=5, sticky=tkinter.W, padx=3, pady=3)

    def select_destdir_and_add(self):
        self.destdir = filedialog.askdirectory()
        if self.destdir:
            ttk.Label(self, text=self.destdir
                      ).grid(column=1, row=5, sticky=tkinter.W, padx=3, pady=3)
            ttk.Button(self,
                       text="Start plotting",
                       command=self.run,
                       ).grid(column=0, row=6, sticky=tkinter.W, padx=3, pady=3)
            ttk.Button(self,
                       text="More Options",
                       command=self.flick_more_options,
                       ).grid(column=0, row=7, sticky=tkinter.W, padx=3, pady=3)

    def selected_source(self):
        if self.source.get() == "summary":
            for i in self.readtypes:
                i.config(state=tkinter.NORMAL)
        else:
            for i in self.readtypes:
                i.config(state=tkinter.DISABLED)
        ttk.Button(self,
                   text='Select data file(s)',
                   command=self.select_file_and_add
                   ).grid(column=0, row=4, sticky=tkinter.W, padx=3, pady=3)

    def flick_more_options(self):
        if not hasattr(self, "optframe"):
            self.optframe = ttk.Frame(self.root)
            self.optframe.grid(column=0, row=14, sticky=tkinter.W + tkinter.N,  pady=10, padx=10)
            ttk.Label(self.optframe, text="Which output format?"
                      ).grid(column=0, row=0, padx=20)
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
            ttk.Label(self.optframe, text="Which plotting color?"
                      ).grid(column=1, row=0, padx=20)
            for i, c in enumerate(['blue', 'red', 'green', 'orange', "purple", "yellow"]):
                ttk.Radiobutton(self.optframe,
                                text=c,
                                variable=self.color,
                                value=c,
                                ).grid(column=1, row=1 + i, sticky=tkinter.W, padx=20, pady=3)
            ttk.Checkbutton(self.optframe,
                            text="Log transform read lengths",
                            variable=self.loglength
                            ).grid(column=2, row=1, sticky=tkinter.W, padx=20, pady=3)
            ttk.Checkbutton(self.optframe,
                            text="Show N50 on histograms",
                            variable=self.n50
                            ).grid(column=2, row=2, sticky=tkinter.W, padx=20, pady=3)
            vcmd = (self.register(self.validate_integer),
                    '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            ttk.Label(self.optframe, text="Maximal read length for plotting?"
                      ).grid(column=2, row=3, padx=20)
            ttk.Entry(self.optframe,
                      textvariable=self.maxlength,
                      validate='key',
                      validatecommand=vcmd
                      ).grid(column=2, row=4, sticky=tkinter.W, padx=20, pady=3)
            ttk.Label(self.optframe, text="Minimal quality for plotting?"
                      ).grid(column=2, row=5, padx=20)
            ttk.Entry(self.optframe,
                      textvariable=self.minqual,
                      validate='key',
                      validatecommand=vcmd
                      ).grid(column=2, row=6, sticky=tkinter.W, padx=20, pady=3)
        else:
            self.optframe.grid_remove()
            delattr(self, "optframe")

    def validate_integer(self, action, index, value_if_allowed, prior_value,
                         text, validation_type, trigger_type, widget_name):
        """Check if text Entry is valid (number).

        I have no idea what all these arguments are doing here but took this from
        https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
        """
        if(action == '1'):
            if text in '0123456789.-+':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def run(self):
        ttk.Label(self, text="Processing... please be patient."
                  ).grid(column=1, row=6, sticky=tkinter.W, padx=3, pady=3)
        self.update_idletasks()
        try:
            utils.make_output_dir(self.destdir)
            settings = {
                'alength': False,
                "drop_outliers": False,
                "maxlength": self.maxlength.get(),
                "minqual": self.minqual.get(),
                "loglength": self.loglength.get(),
                "downsample": 10000,
                "no_N50": not self.n50.get(),
                "bam": False,
                "summary": False,
                "fastq": False,
                "readtype": self.readtype.get(),
                "barcoded": self.barcoded.get(),
                "format": check_valid_format(self.figformat.get()),
                "color": self.color.get(),
                "plots": ["kde", "hex", "dot"],
                "title": None,
                "path": self.destdir + "/",
                self.source.get(): True
            }
            datadf = get_input(
                source=self.source.get(),
                files=[self.targetfile.name],
                threads=4,
                readtype=settings["readtype"],
                combine="simple",
                barcoded=settings["barcoded"])
            write_stats(
                datadfs=[datadf],
                outputfile=settings["path"] + "NanoStats.txt")
            logging.info("Calculated statistics")
            datadf, settings = nanoplot.filter_data(datadf, settings)
            if settings["barcoded"]:
                for barc in list(datadf["barcode"].unique()):
                    settings["path"] = os.path.join(self.destdir, barc + "_")
                    dfbarc = datadf[datadf["barcode"] == barc]
                    write_stats(dfbarc, settings["path"] + "NanoStats.txt")
                    nanoplot.make_plots(dfbarc, settings)
            else:
                plots = nanoplot.make_plots(datadf, settings)
            html_report = nanoplot.make_report(
                plots=plots,
                path=settings["path"],
                logfile=self.logfile,
                statsfile=settings["path"] + "NanoStats.txt")
            logging.info("Finished!")
            ttk.Label(self, text="Finished, opening web browser."
                      ).grid(column=1, row=6, sticky=tkinter.W, padx=3, pady=3)
            self.update_idletasks()
            webbrowser.open(html_report, new=2)
        except Exception as e:
            logging.error(e, exc_info=True)
            ttk.Label(self, text="Something unexpected happened and NanoPlot has crashed."
                      ).grid(column=1, row=6, sticky=tkinter.W, padx=3, pady=3)
            self.update_idletasks()
            raise


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
    print("not implemented")
    # nanoPlotGui(logfile).mainloop()


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
