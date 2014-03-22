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

import DataFrame
from sigmoidal import process_sigmoidal
from utils import list_rasters, ParsedFileName


def main():

    formats = ['tif', 'img']

    parser = ArgumentParser()
    parser.add_argument("-i", "--in", dest="inws", help="Input workspace")
    parser.add_argument("-o", "--out", dest="outws", help="Output workspace")
    parser.add_argument("-p", "--parameters", dest="parameters",
                        help="Path to parameters csv file")
    parser.add_argument("-l", "--link-field", dest="link_field",
                        help="Link field in the parameters file")
    parser.add_argument("-f", "--format", dest="format", default="tif",
                        help="file format for FILENAME")
    parser.add_argument("-t", "--template", dest="template",
                        default="<BODY1>_<ID1>_<BODY2>_<ID2>_<BODY3>",
                        help="Template for file names in input workspace")

    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose")

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
        parser.error("Provided format must be one of: %s"
                     % ', '.join(formats))

    # List the rasters found in the input workspace
    inrasters = list_rasters(inws, [args.format], sorted=True)

    # Read the parameters file in as Dataframe
    parameters_df = DataFrame.read_csv(args.parameters,
                                       dialect=DataFrame.ZCustom)

    # Get all the field names from the generated DataFrame
    fields = parameters_df.get_fields()
    if not args.link_field:
        parser.error("No link field provided, available fields " +
                     "are: \n" + '\n'.join(fields))
    elif args.link_field not in fields:
        parser.error("Link field provided not found, available fields " +
                     "are: \n" + '\n'.join(fields))
    else:
        link_field = args.link_field

    if args.verbose:
        print("\n")
        print("STARTING " + "*" * 70)
        print("Input workspace: {0}".format(inws))
        print("Output workspace: {0}".format(outws))
        print("Parameters file: {0}".format(parameters))
        print("Format: {0}".format(args.format))
        print("File name template: {0}".format(args.template))
        if len(inrasters) > 0:
            print("Following rasters found in input workspace:")
            for raster in inrasters:
                print("\t" + os.path.basename(raster))
        else:
            print("Could not find any rasters with format <" +
                  "{0}> in input workspace".format(args.format))
        print("\n")

    # Construct ParsedFileNames from the input workspace based on a template
    inrasters = [ParsedFileName(raster, args.template) for raster in inrasters]

    process_sigmoidal(inrasters, parameters_df, link_field, outws,
                      multiply=True)

if __name__ == '__main__':
    sys.exit(main())
