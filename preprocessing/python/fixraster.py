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

import sys, os
import glob
import subprocess
from optparse import OptionParser

# Executable must be in PATH
if sys.platform == 'win32':
    EXECUTABLE = 'cfixraster.exe'   
else:
    EXECUTABLE = 'cfixraster'
    

# =============================================================================
def ListRasters(dir='.', formats=None):
    files = []
    for format in formats:
        temp_files = glob.glob(os.path.join(dir, '*.' + format))
        for file in temp_files:
            files.append(file)
    return files

def ParseNodata(type):
    if type == 'Byte':
        return 0
    elif type == 'Int16':
        return -32768
    elif type == 'UInt16':
        return 0
    elif type == 'Int32':
        return -2147483648
    elif type == 'UInt32':
        return 0
    elif type == 'Float32':
        return -3.402823466e+38
    else:
        return -1
# ======================

def fix_raster(input, output, format, options, oldnodata=None,
               newnodata=None, suffix="fixed", verbose=False):
    
    cmd = []
    
    cmd.append(EXECUTABLE)
    cmd.append('-i'); cmd.append(input)
    cmd.append('-o'); cmd.append(output)
    
    if format != '':
        cmd.append('-f'); cmd.append(format)
        
    if options != '':
        for option in options:
            cmd.append('-c'); cmd.append(option)
    
    if oldnodata:
        cmd.append('-n'); cmd.append(str(oldnodata))
    
    if newnodata:
        cmd.append('-m'); cmd.append(str(newnodata))
    
    if verbose:
        print 'Command: ' + ' '.join(cmd)
        
    try:
        retcode = subprocess.call(cmd)
        if retcode < 0:
            print >>sys.stderr, "Execution was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Execution terminated normally"
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e


def batch_fix_rasters(infiles, outdir, *args, **kwargs):
    
    for infile in infiles:
            outfile = os.path.join(outdir, os.path.basename(infile))
            fix_raster(infile, outfile, *args, **kwargs)

def main():
    
    formats = ['tif', 'img']
    
    usage = "usage: %prog [options] datatype infile outfile"
    
    parser = OptionParser(usage)
    parser.add_option("-i", "--infile", dest="infile",
                      help="read data from FILENAME")
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="write data to FILENAME")
    parser.add_option("-f", "--format", dest="format", default="HFA",
                      help="file format for FILENAME")
    parser.add_option("-c", "--creation-options", dest="options", default='',
                      help="Creation options")
    
    parser.add_option("-n", "--old-nodata-value", dest="oldnodata", 
                      default=-128, help="Value for old NoData")
    
    parser.add_option("-m", "--new-nodata-value", dest="newnodata", 
                      default=255, help="Value for new NoData")
    
    parser.add_option("-l", "--list", default=False,
                      action="store_true", dest="list")
    parser.add_option("-v", "--verbose", default=False,
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")

    (options, args) = parser.parse_args()
    
    if options.list:    
        files = ListRasters(formats=formats)
        if files:
            print "Raster files %s in the directory %s:" % (formats, os.getcwd())
            for file in files:
                print " " + file
        else:
            print "No raster files in the current directory."
        
        if not options.infile and not options.outfile:    
            return 0
    
    if options.infile is None and not options.list:
        parser.error("Name of the input file must be provided")
    if options.outfile is None and not options.list:
        parser.error("Name of the output file must be provided")
            
    # Take care of the dot directory notation
    if options.infile == '.':
        options.infile = os.path.abspath('.')
        
    if options.outfile == '.':
        options.outfile = os.path.abspath('.')
    
    print options.infile
    
    if os.path.isdir(options.infile):
        files = ListRasters(formats=formats)
        options.infile = files
        
        if not os.path.exists(options.outfile) or not os.path.isdir(options.outfile):
            print "Provided output location <%s> does not exits or is not a directory." % options.outfile
            resp = raw_input("Should it be created? (Yes/No)>")
            if resp.lower() in ['yes', 'y'] and options.outfile:
                os.mkdir(options.outfile)
                print "Directory created."
            else:
                print "Nothing to do, exiting..."
                return
    
    if type(options.infile) == type(str()):
        if os.path.isfile(options.infile):
            fix_raster(options.infile, options.outfile, options.format, 
                       options.options, options.oldnodata, options.newnodata,
                       verbose=options.verbose)
    elif type(options.infile) == type(list()):
        batch_fix_rasters(options.infile, options.outfile, options.format, 
                       options.options, options.oldnodata, options.newnodata,
                       verbose=options.verbose)
        

if __name__ == '__main__':
    sys.exit(main())
