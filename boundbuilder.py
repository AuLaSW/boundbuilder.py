"""
BoundBuilder Application
------------------------

This is a program designed by Austin Swanlaw to generate bound
PDF projects using pypdf2.
"""
# from PyPDF2 import PdfReader, PdfWriter
# from increment import Increment
import pdb
import pikepdf
import time
from pathlib import Path
import tkinter.messagebox as messagebox
import sys
import getopt
from utils import DropIns


def mergePdfs(paths, output, pf, opts):
    pdf_writer = pikepdf.Pdf.new()

    for file in paths[output]:
        print(file)

        if file in paths:
            mergePdfs(
                paths=paths,
                output=file,
                pf=pf,
                opts=opts
            )
            pf.remove(file)

        with pikepdf.Pdf.open(file) as pdf:
            for page in pdf.pages:
                if opts['rotate'] != 0:
                    page.rotate(
                        angle=opts['rotate'],
                        relative=False
                    )
                pdf_writer.pages.append(page)

    pdf_writer.save(output)
    pdf_writer.close()


def getConfig(CWD: Path):
    """
    Params:
    -------
        CWD: a Path object containing the current working path.

    Returns:
    --------
        sets: a dictionary of sets to combine, with keys being the
              bound sets and items in a list being the files to bind.

    Action:
    -------
    Returns a set of paths for different bound sets.
    """
    config = CWD / '.smpl'

    if not config.exists():
        config = CWD / '.config'

    sets = dict()

    with open(config, 'r') as cfg:
        configParser(cfg, CWD, sets)

    return sets


def configParser(cfg, CWD, sets):
    for line in cfg:
        # if the line has no whitespace around it
        # (aka, it is not tabbed in)
        if line.lstrip() == line:
            # cbs = current bound set
            cbs = CWD / (line.strip() + '.pdf')
            # create a list to hold the paths
            sets[cbs] = []
        elif line.startswith("\t") or line.startswith("    "):
            sets[cbs].append(CWD / (line.strip() + '.pdf'))
        else:
            # raise RuntimeError(f"The line \"{line.strip()}\" in .config is not correctly formatted.")
            err = RuntimeError(f"The line \"{line.strip()}\" in .config is not correctly formatted.")
            messagebox.showerror("Incorrect Input Structure", err)
            quit()


def pathize(line, CWD):
    return CWD / (line.strip() + '.pdf')


def parseArgs(argv):
    """
    Parse the arguments passed through the main function
    """
    # single-letter options available
    # see the help variable for what these options are
    options = "hr:"
    long_options = ["rotate="]

    optpass = {
        "rotate": 0,
    }

    # get the options and their arguments from the argv input
    opts, args = getopt.getopt(argv, options, long_options)

    for opt, arg in opts:
        # show the help
        if opt == "-h":
            print(help.strip())
            quit()
        # get value for rotation of pdf's
        if opt in ("-r", "--rotate"):
            optpass['rotate'] = int(arg)

    return optpass, args


def main(argv):
    CWD = Path.cwd()

    opts, file_inputs = parseArgs(argv)

    # the new way of doing it, where you can just drop files
    if len(file_inputs) > 0:
        drop_files = DropIns(*file_inputs).order()

        for key, value in drop_files.items():
            print()
            print(key)
            print()
            for sheet in value:
                print(sheet.full_name)

        time.sleep(10)
    # here we will grab the files from the folder, only the PDFs
    elif len(file_inputs) == 0 and not (CWD / 'config.yaml').exists():
        # grab all of the pdf files in the current working directory
        file_names = list(CWD.glob('*.pdf'))

        pdb.set_trace()
        drop_files = DropIns(*file_names).order()

        for key, value in drop_files.items():
            print()
            print(key)
            print()
            for sheet in value:
                print(sheet.full_name)

        time.sleep(10)
    # the old method of doing it, where there is a config file in the folder
    else:
        files = getConfig(CWD)

        processedfiles = []

        for boundset in files.keys():
            processedfiles.append(boundset)

        for output in files.keys():
            if output in processedfiles:
                try:
                    mergePdfs(
                        output=output,
                        paths=files,
                        pf=processedfiles,
                        opts=opts
                    )
                except FileNotFoundError as err:
                    messagebox.showerror("Error!", err)


version = "v0.4.0-alpha"

help = f"""
BoundBuilder, {version}.

bounbuilder.py [opts]

Options:
    h               help
    r, --rotate     rotate each sheet in the set by 
                    the value in degrees
"""


if __name__ == "__main__":
    main(sys.argv[1:])
