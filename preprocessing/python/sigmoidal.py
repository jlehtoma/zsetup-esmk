#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# $Id$
#
# Project:  GDAL custom tools
# Purpose:  Script to deal with with signed bytes used by e.g. ArcGIS by default
#           for specific data sets. Signed byte is not a valid data type for
#           GDAL, so it needs to be converted to at least Int16/UInt16. Script
#           uses parts from val_repl.py script in GDAL examples by Andrey 
#           Kiselev.
#
# Author:   Joona Lehtomäki, joona.lehtomaki@gmail.com
#
###############################################################################
# Copyright (c) 2010, Joona Lehtomäki <joona.lehtomaki@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################


try:
    from osgeo import gdal
    from osgeo.gdalconst import *
    gdal.TermProgress = gdal.TermProgress_nocb
except ImportError:
    import gdal
    from gdalconst import *

try:
    import numpy
except ImportError:
    import Numeric as numpy


import sys, os
import glob
from optparse import OptionParser

# =============================================================================
def ParseType(type):
    if type == 'Byte':
        return GDT_Byte
    elif type == 'Int16':
        return GDT_Int16
    elif type == 'UInt16':
        return GDT_UInt16
    elif type == 'Int32':
        return GDT_Int32
    elif type == 'UInt32':
        return GDT_UInt32
    elif type == 'Float32':
        return GDT_Float32
    elif type == 'Float64':
        return GDT_Float64
    elif type == 'CInt16':
        return GDT_CInt16
    elif type == 'CInt32':
        return GDT_CInt32
    elif type == 'CFloat32':
        return GDT_CFloat32
    elif type == 'CFloat64':
        return GDT_CFloat64
    else:
        return GDT_Byte
# =============================================================================

def sigmoidal(options):
    pass
    
def main():
    
    formats = ['tif', 'img']
    
    usage = "usage: %prog [options] format infile1 infile2 outfile"
    
    parser = OptionParser(usage)
    parser.add_option("--infile1", dest="infile1", help="Infile 1")
    parser.add_option("--infile2", dest="infile2", help="Infile 2")
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="write data to FILENAME")
    
    parser.add_option("-f", "--format", dest="format", default="GTiff",
                      help="file format for FILENAME")
    
    parser.add_option("-v", "--verbose", default=False,
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")

    (options, args) = parser.parse_args()

    if options.infile1 is None or options.infile2 is None:
        parser.error("Names of the input files must be provided")
    if options.outfile is None and not options.info:
        parser.error("Name of the output file must be provided")
    
    if options.verbose: 
        print "Using %s and %s..." % (options.infile1, options.infile2)
    
    sigmoidal(options)

if __name__ == '__main__':
    sys.exit(main())
