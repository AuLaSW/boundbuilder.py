"""
BoundBuilder Application
------------------------

This is a program designed by Austin Swanlaw to generate bound
PDF projects using pypdf2.
"""
# from PyPDF2 import PdfReader, PdfWriter
import pikepdf
from pathlib import Path
import tkinter.messagebox as messagebox
from increment import Increment
import pdb
import sys


def mergePdfs(paths, output, pf):
    pdf_writer = pikepdf.Pdf.new()
    
    for file in paths[output]:
        print(file)
        
        if file in paths:
            mergePdfs(
                paths=paths,
                output=file,
                pf=pf
            )
            pf.remove(file)
        
        with pikepdf.Pdf.open(file) as pdf:
            pdf_writer.pages.extend(pdf.pages)

    #pdf_writer.remove_unreferenced_resources()
    
    pdf_writer.save(output)
    pdf_writer.close()


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
            raise RuntimeError(f"The line \"{line.strip()}\" in .config is not correctly formatted.")


def pathize(line, CWD):
    return CWD / (line.strip() + '.pdf')


def main():
    CWD = Path.cwd()
    
    try:
        files = getConfig(CWD)
    except RuntimeError as err:
        messagebox.showerror("Incorrect Input Structure", err)
        quit()

    processedfiles = []
    
    for boundset in files.keys():
        processedfiles.append(boundset)
    
    for output in files.keys():
        if output in processedfiles:
            try:
                mergePdfs(
                    output=output,
                    paths=files,
                    pf=processedfiles
                )
            except FileNotFoundError as err:
                messagebox.showerror("Error!", err)


class SMPLParser:
    def configParser2(cfg, CWD):
        # dictionary of bound sets
        sets = {}
        
        curline = cfg.readline()
        nextline = cfg.readline()
        
        curlinelvl = level(curline)
        nextlinelvl = level(nextline)
        
        if curlinelvl < nextlinelvl:
            """
            curline
                nextline
            """
            prevcbs = cbs
            cbs = pathize(curline, CWD)
            sets[cbs] = []
            # if we are already inside of a bound set,
            # append the name of the current file to
            # the list of files to bind to the original
            # set.
            if cbs >= 2:
                sets[prevcbs].append(cbs)
        elif curlinelvl == nextlinelvl:
            """
            curline
            nextline
            """
            sets[cbs].append(pathize(curline, CWD))
        elif curlinelvl > nextlinelvl:
            """
                curline
            nextline
            """
            sets[cbs].append(pathize(curline, CWD))
            cbs = prevcbs
        
        return sets


    def level(line: str) -> int:
        accum = Increment()
        for char in line:
            if char == '\t':
                +accum
            else:
                break
        
        return accum.value


if __name__ == "__main__":
    main()