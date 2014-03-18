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
def ListRasters(formats):
    files = []
    for format in formats:
        temp_files = glob.glob('*.' + format)
        for file in temp_files:
            files.append(file)
    return files
  
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

def ConvertRaster(options):

    indataset = gdal.Open(options.infile, GA_ReadOnly)

    if options.verbose:
        print 'Writing output data set - driver: %s type %s' %(options.format,
                                                               options.type)
    for iBand in range(1, indataset.RasterCount + 1):
        if options.verbose:
            print 'Transforming band %s' % (iBand)
        inband = indataset.GetRasterBand(iBand)
        type = gdal.GetDataTypeName(inband.DataType)
        if options.info or options.verbose:
            sys.stdout.write(('%s band %s pixel type is %s' % (options.infile, iBand, type)))
            if type == 'Byte':
                meta = inband.GetMetadata('IMAGE_STRUCTURE')
                if meta.has_key('PIXELTYPE'):
                    print(' that *seems* to be %s, conversion to 16 bits or more is recommended' % meta['PIXELTYPE'])
                else:
                    print(' that *seems* to be UNSIGNED.')
            else:
                pass
                 
        if not options.info:
            
            out_driver = gdal.GetDriverByName(options.format)
            outdataset = out_driver.Create(options.outfile, indataset.RasterXSize,
                                   indataset.RasterYSize, indataset.RasterCount,
                                   ParseType(options.type))
            
            print 'Converting raster to %s' % options.type
            
            outband = outdataset.GetRasterBand(iBand)

            for i in range(inband.YSize - 1, -1, -1):
                scanline = inband.ReadAsArray(0, i, inband.XSize, 1, inband.XSize, 1)
                outband.WriteArray(scanline, 0, i)
            
            outband.FlushCache()
            
            if options.verbose:
                print 'Setting NoData to %s' % ParseNodata(options.type)
            outband.SetNoDataValue(ParseNodata(options.type))
            
            # georeference the image and set the projection
            #if options.verbose:
            #    print 'Doing Geotransformation and projection'
            #outdataset.SetGeoTransform(inband.GetGeoTransform())
            #outdataset.SetProjection(inband.GetProjection())
            
            # build pyramids
            if options.verbose:
                print 'Building pyramids'
            gdal.SetConfigOption('HFA_USE_RRD', 'YES')
            outdataset.BuildOverviews(overviewlist=[2,4,8,16,32,64,128])
    
    inband = None
    outdataset = None 

def main():
    
    formats = ['tif', 'img']
    
    usage = "usage: %prog [options] datatype infile outfile"
    
    parser = OptionParser(usage)
    parser.add_option("-i", "--infile", dest="infile",
                      help="read data from FILENAME")
    parser.add_option("-o", "--outfile", dest="outfile",
                      help="write data to FILENAME")
    
    parser.add_option("-t", "--type", dest="type", default=GDT_Byte,
                      help="data type for FILENAME")
    parser.add_option("-f", "--format", dest="format", default="GTiff",
                      help="file format for FILENAME")
    
    parser.add_option("-n", "--info", default=False,
                      action="store_true", dest="info")
    parser.add_option("-l", "--list", default=False,
                      action="store_true", dest="list")
    parser.add_option("-r", "--recursive", default=False,
                      action="store_true", dest="recursive")
    
    parser.add_option("-v", "--verbose", default=False,
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")

    (options, args) = parser.parse_args()
    
    if options.list or options.recursive:
        files = ListRasters(formats)
        print "Raster files %s in the directory %s:" % (formats, os.getcwd())
        for file in files:
            print " " + file
        if options.list and (not options.infile or not options.outfile):
            return
        if options.recursive:
            options.infile = files
    
    if options.infile is None and not options.recursive:
        parser.error("Name of the input file must be provided")
    if options.outfile is None and not options.info:
        parser.error("Name of the output file must be provided")
    
    if options.verbose: 
        print "reading %s..." % options.infile
    
    if type(options.infile) == type(str()):
        ConvertRaster(options)
    elif type(options.infile) == type(list()):
        files = options.infile
        for file in files:
            options.infile = file
            ConvertRaster(options)

if __name__ == '__main__':
    sys.exit(main())
