"""
BoundBuilder Application
------------------------

This is a program designed by Austin Swanlaw to generate bound
PDF projects using pypdf2.
"""
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import tkinter.messagebox as messagebox


def mergePdfs(paths, output):
    """
    Params:
    -------
        paths: an iterable collection of paths of pdfs to merge.
        
        output: the Path object for the output file.
    
    Returns:
    --------
        None
    
    Action:
    -------
        Takes the pdfs found in paths and merges them into one pdf
        file and saves the pdf file to output.
    """
    pdf_writer = PdfWriter()
    
    for path in paths:
        pdf_reader = PdfReader(path)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
    
    with open(output, 'wb') as out:
        pdf_writer.write(out)


def getConfig(CWD):
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
    config = CWD / '.config'
    
    sets = {}
    
    with open(config, 'r') as cfg:
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
                raise RuntimeError(f"The line \"{line.strip()}\" in .config is not correctly formatted.")
    
    return sets
    
def configParser(file):
    pass


def main():
    CWD = Path.cwd()
    
    try:
        files = getConfig(CWD)
    except RuntimeError as err:
        messagebox.showerror("Incorrect Input Structure", err)
        quit()
    
    for boundset, mergers in files.items():
        mergePdfs(mergers, boundset)


if __name__ == "__main__":
    main()