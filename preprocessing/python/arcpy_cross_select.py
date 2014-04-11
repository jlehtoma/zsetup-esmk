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
# Set the workspaces to the correct location.
inputws = "C:/Data/ESMK/preprocessing/workspace/composite/60"
# Just uset the input workspace as output workspace
outputws = os.path.join(inputws, "sfc_classified")

# Check that workspaces exists
if not os.path.exists(inputws):
    print("ERROR: Input workspace {0} does not exist".format(outputws))
    sys.exit(0)
elif not os.path.exists(outputws):
    print("ERROR: Output workspace {0} does not exist".format(outputws))
    sys.exit(0)
else:
    print("INFO: Using input workspace: {0}".format(inputws))
    print("INFO: Using output workspace: {0}".format(outputws))
    # Set the workspace to provided input workspace
    env.workspace = inputws

# Set the condition raster, i.e. the soil fertility class raster
conditional_raster = os.path.abspath(os.path.join(wd,
                                     "../../data/common/60",
                                     "esmk_soil_fertility.img"))

if not os.path.exists(conditional_raster):
    print("ERROR: Conditional raster " +
          "{0} does not exist".format(conditional_raster))
    sys.exit(0)

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
        # MSNFI
        if len(tokens) == 4:
            # Remove the numeric component
            del tokens[2]
            # Add sfc_class value to the end of the file name
            tokens[2] = tokens[2].split(".")[0] + "_{0}.".format(value) + \
                tokens[2].split(".")[1]
        # Composite
        elif len(tokens) == 2:
            tokens[1] = tokens[1].split(".")[0] + "_{0}.".format(value) + \
                tokens[1].split(".")[1]

        output_name = "_".join(tokens)
        outputRaster = os.path.join(outputws, output_name)
        outSetNull.save(outputRaster)

print("All finished")
