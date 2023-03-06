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
    
    for path in paths[output]:
        try:
            pdf_reader = PdfReader(path)
        except FileNotFoundError:
            boundname = depathize(path)
            
            if path in paths:
                mergePdfs(
                    output=path,
                    paths=paths
                )
                
                pdf_reader = PdfReader(path)
                #output.remove(boundname)
            else:
                #tb = sys.exception().__traceback__
                raise FileNotFoundError(f"File {boundname}.pdf could not be found.")
        
        print(path)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
    
    with open(output, 'wb') as out:
        pdf_writer.write(out)


def mergePdfsPike(paths, output, pf):
    pdf_writer = pikepdf.Pdf.new()
    
    for file in paths[output]:
        print(file)
        
        if file in paths:
            mergePdfsPike(
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


def pathize(line, CWD):
    return CWD / (line.strip() + '.pdf')


def depathize(path):
    return path.parts[-1].replace('.pdf', '')


def level(line: str) -> int:
    accum = Increment()
    for char in line:
        if char == '\t':
            +accum
        else:
            break
    
    return accum.value


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
                mergePdfsPike(
                    output=output,
                    paths=files,
                    pf=processedfiles
                )
            except FileNotFoundError as err:
                messagebox.showerror("Error!", err)
    
    """
    for boundset, mergers in files.items():
        mergePdfs(output=boundset, paths=mergers)
    """
    
    """
    pdf_writer = PdfWriter()
    
    for path in path[output]:
        try:
            pdf_reader = PdfReader(path)
        except FileNotFoundError:
            boundname = depathize(path)
            
            if boundame in output:
                mergePdfs(
                    output=path,
                    paths=paths
                )
                output.remove(boundname)
            else:
                raise FileNotFoundError
            
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
    
    with open(output, 'wb') as out:
        pdf_writer.write(out)
    """


if __name__ == "__main__":
    main()