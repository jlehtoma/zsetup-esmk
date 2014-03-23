#!/usr/bin/env python
#
# -*- coding: utf-8 -*-

import os
import sys

import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.CheckOutExtension("Spatial")

# Current working directory is the directory where this file resides
wd = os.path.dirname(__file__)
# Set the workspaces to the correct location. This is mostly to avoid
# hard coding paths
inputws = os.path.abspath(os.path.join(wd, "../../data/msnfi/indices"))
outputws = os.path.join(inputws, "per_sf_class")

conditional_raster = os.path.abspath(os.path.join(wd, "../../data/common",
                                     "esmk_soil_fertility.img"))

# Check that workspaces exists
if not os.path.exists(inputws):
    print("Input workspace {0} does not exist".format(outputws))
    sys.exit(0)
elif not os.path.exists(outputws):
    print("Output workspace {0} does not exist".format(outputws))
    sys.exit(0)
else:
    print("Using input workspace: {0}".format(inputws))
    print("Using output workspace: {0}".format(outputws))
    # Set the workspace to provided input workspace
    env.workspace = inputws

# Hard code the used soil fertility classes that will be the basis of extraction
sfc_classes = [1, 2, 3, 4, 5]

# List rasters in the input workspace
rasters = arcpy.ListRasters("*", "*")

# Loop over all values and all rasters
for raster in rasters:
    for value in sfc_classes:

        print("Extracting {0} with value {1}".format(raster, value))

        outSetNull = SetNull(conditional_raster, raster,
                             "VALUE <> {0}".format(value))
        # [fixme] - creation of output name is tied to an exact structure of
        # e.g. 'index_msnfi_4_odecid.tif'
        tokens = raster.split("_")
        # Remove the numeric component
        del tokens[2]
        # Add sfc_class value to the end of the file name
        tokens[2] = tokens[2].split(".")[0] + "_{0}.".format(value) + \
            tokens[2].split(".")[1]
        output_name = "_".join(tokens)
        outputRaster = os.path.join(outputws, output_name)
        outSetNull.save(outputRaster)

print("All finished")
