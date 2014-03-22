#!/usr/bin/env python
#
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
# Author:   Joona Lehtomaki, joona.lehtomaki@gmail.com
#
###############################################################################
# Copyright (c) 2010, Joona Lehtomaki <joona.lehtomaki@gmail.com>
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

import sys
import os
from argparse import ArgumentParser

from osgeo import gdal
from osgeo.gdalconst import *
gdal.TermProgress = gdal.TermProgress_nocb

import numpy


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


def sigmoidal(args):
    pass


def main():

    formats = ['tif', 'img']

    parser = ArgumentParser()
    parser.add_argument("-i", "--in", dest="inws", help="Input workspace")
    parser.add_argument("-o", "--out", dest="outws", help="Output workspace")
    parser.add_argument("-p", "--parameters", dest="parameters",
                        help="Path to parameters csv file")
    parser.add_argument("-f", "--format", dest="format", default="GTiff",
                        help="file format for FILENAME")

    parser.add_argument("-v", "--verbose", default=False,
                        action="store_true", dest="verbose")

    args = parser.parse_args()

    if not args.inws:
        parser.error("Path to input workspace must be provided")
    else:
        inws = os.path.abspath(args.inws)
        if not os.path.exists(inws):
            parser.error("Input workspace {0} does not exist".format(inws))

    if not args.outws:
        parser.error("Path to output workspace must be provided")
    else:
        outws = os.path.abspath(args.outws)
        if not os.path.exists(args.outws):
            parser.error("Output workspace {0} does not exist".format(outws))

    if not args.parameters:
        parser.error("Path to parameters CSV file must be provided")
    else:
        parameters = os.path.abspath(args.parameters)
        if not os.path.exists(parameters):
            parser.error("Parameters file {0} does not ".format(parameters) +
                         " exist")

    if args.format not in formats:
        parser.error("Provided format must be one of: "
                     % ', '.join(formats))

    if args.verbose:
        print("\n")
        print("INITIATING " + "*" * 70)
        print("Using input workspace: {0}".format(inws))
        print("Using output workspace: {0}".format(outws))
        print("Using parameters file: {0}".format(parameters))
        print("Format: {0}".format(args.format))
        print("\n")

    sigmoidal(args)

if __name__ == '__main__':
    sys.exit(main())
