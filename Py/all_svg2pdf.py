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


def get_file_list(root, extension):
    """Get all svg files in root directory and below"""

    svg_list = []

    for path, subdirs, files in os.walk(root):
        for file in files:
            if file.endswith(extension):
                abspath_file = path + os.sep + file
                svg_list.append(abspath_file)
    print('%i svg files were found under root path: %s' %(len(svg_list), root))
    return svg_list

