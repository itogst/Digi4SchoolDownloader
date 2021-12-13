#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
==============================================================================
                                all_svg2pdf

    A Python module to convert all .svg files in a root folder (and below) 
    to .pdf according to the following inkscape options:
    --without-gui
    --export-area-drawing

    For more inkscape options see: http://inkscape.org/doc/inkscape-man.html

    Usage: 
    $python all_svg2pdf.py
==============================================================================
'''
import os

__author__ = "Manolis Georgioudakis"
__version__ = "Revision: 0.1"
__date__ = "Date: 2013/09"
__copyright__ = "Copyright (c) 2013"
__license__ = "Python"


def getPaths():
    """Get root directory and define extension"""

    cwd = os.getcwd()
    extension = '.svg'

    return cwd, extension

def getSVGList(root, extension):
    """Get all svg files in root directory and below"""

    svg_list = []

    for path, subdirs, files in os.walk(root):
        for file in files:
            if file.endswith(extension):
                abspath_file = path + os.sep + file
                svg_list.append(abspath_file)
    print('Were found %i svg files under root path: %s' %(len(svg_list), root))
    return svg_list
                
def svg2pdf(list):
    """Convert all svg files to pdf according to specified options"""

    options = '--shell --export-area-drawing'
    print('\nConverting, please wait...\n')
    for file in list:
        print('Converting file: %s' %file)
        fileParts = file.split("\\")
        pdf_abspath = "output/"+fileParts[fileParts.__len__()-1].split(".")[0]
        os.system('inkscape %s --export-area-drawing --batch-process --export-type=pdf --export-filename=%s.pdf' %(file, pdf_abspath))

#--export-area-drawing --batch-process --export-type=pdf --export-filename=output.pdf
#inkscape "Py\5134\24\24.svg" --export-area-drawing --batch-process --export-type=pdf --export-filename=output.pdf

if __name__ == "__main__":
    print(__doc__)
    cwd, extension = getPaths()
    svg_files = getSVGList(cwd, extension)
    svg2pdf(svg_files)