"""
BoundBuilder Application
------------------------

This is a program designed by Austin Swanlaw to generate bound
PDF projects using pypdf2.
"""
import pikepdf
from pathlib import Path
import sys
import getopt
from utils import DropIns


def bind(sheets: DropIns, name: str | list[str], opts):
    # take list FileName objects and generate the PDf associated with them
    pdf_writer = pikepdf.Pdf.new()

    bound_name = f"BOUND {name}.pdf"

    if isinstance(name, list):
        bound_name = "BOUND SET.pdf"
        for key in name:
            __pdf_work(pdf_writer, key, sheets, opts)
    else:
        __pdf_work(pdf_writer, name, sheets, opts)

    pdf_writer.save(sheets.base_path / bound_name)
    pdf_writer.close()


def __pdf_work(writer, key, sheets, opts):
    for sheet in sheets.files[key]:
        with pikepdf.Pdf.open(sheets.base_path / (sheet.full_name + '.pdf')) as pdf:
            for page in pdf.pages:
                if opts['rotate'] != 0:
                    page.rotate(
                        angle=opts['rotate'],
                        relative=False
                    )
                writer.pages.append(page)


def parse_args(argv):
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

    opts, file_inputs = parse_args(argv)

    # here we will grab the files from the folder, only the PDFs
    if not file_inputs:
        # grab all of the pdf files in the current working directory
        file_inputs = list(CWD.glob('*.pdf'))

    # pdb.set_trace()
    drop_files = DropIns(*file_inputs)

    non_empty = list()
    for key, value in drop_files.files.items():
        if len(value) > 0:
            # merge the pdfs into their sub bound sets
            bind(drop_files, key, opts)
        if drop_files.proj_ord.config[key][0]:
            non_empty.append(key)

    bind(drop_files, non_empty, opts)


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
