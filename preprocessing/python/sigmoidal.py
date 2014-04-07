#!/usr/bin/env python
#
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import sys

import numpy as np
import numpy.ma as ma

from osgeo import gdal
from osgeo.gdalconst import (GA_ReadOnly, GDT_Float32)

# register all of the GDAL drivers
gdal.AllRegister()

from utils import create_output_name


def asym_sigmoidal(x, asym=1.0, mod_asym=1.0, xmid=None, lscale=1.0,
                   rscale=1.0):
    if xmid is None:
        xmid = ma.median(x)
    return np.where(x <= xmid, (asym * mod_asym) /
                    (1 + ma.exp((xmid - x) / lscale)),
                    asym / (1 + ma.exp((xmid - x) / rscale)))


def sigmoidal(x, asym=1.0, xmid=None, xmod=0, scale=1.0):
    if xmid is None:
        xmid = ma.median(x)
    xmid = xmid + xmod
    return asym / (1 + ma.exp((xmid - x) / scale))


def sigmoidal_index(raster, output, mod_asym, rxmod, lxmod, lscale, rscale,
                    xmid=None):

    startTime = time.time()

    # open the image
    output_name = os.path.join(output,
                               create_output_name(os.path.basename(raster)))

    ds = gdal.Open(raster, GA_ReadOnly)

    if ds is None:
        print 'Could not open %s' % raster
        sys.exit(1)

    # get raster  size
    rows = ds.RasterYSize
    cols = ds.RasterXSize

    # get the bands and block sizes
    inBand = ds.GetRasterBand(1)

    # create the output image
    driver = gdal.GetDriverByName('HFA')
    dst_options = ['COMPRESS=LZW']
    outDs = driver.Create(output_name, cols, rows, 1, GDT_Float32, dst_options)
    if outDs is None:
        print 'Could not create %s' % output_name
        sys.exit(1)
    outBand = outDs.GetRasterBand(1)

    # Get NoData

    NO_DATA = inBand.GetNoDataValue()
    if NO_DATA is not None:
        print 'NoData value: %s' % NO_DATA
    else:
        if inBand.DataType == GDT_Float32:
            NO_DATA = -3.40282346639e+38
            print 'NoData value not available, using default for GDT_Float32'
        else:
            print 'No NoData information available, defaulting to -1'
            NO_DATA = -1

    print 'Reading in data...'
    data_raster = inBand.ReadAsArray()

    print 'Masking NoData...'
    ma_data = ma.masked_where(data_raster == NO_DATA, data_raster)

    ma_max = ma_data.max()

    if not xmid:
        xmid = ma.median(ma_data)

    print 'Masked max: %s' % ma_max
    print 'Xmid: %s' % xmid
    print 'Lxmid: %s' % lxmod
    print 'Rxmod: %s' % rxmod
    print 'Mod asym (if used): %s' % mod_asym
    print 'Lscale: %s' % lscale
    print 'Rscale: %s' % rscale

    print 'Calculationg sigmoidal transformation...'
    # This is the assymetric version
    ma_sig = np.where(ma_data <= xmid,
                      sigmoidal(ma_data, asym=mod_asym,
                                xmid=xmid + (ma_max * lxmod),
                                scale=(ma_max / lscale)),
                      sigmoidal(ma_data,
                                xmid=xmid + (ma_max * rxmod),
                                scale=(ma_max / rscale)))

    # Write data
    data = ma.filled(ma_sig, fill_value=NO_DATA)
    print 'Writing raster...'
    outBand.WriteArray(data)

    # flush data to disk, set the NoData value and calculate stats
    outBand.FlushCache()
    if NO_DATA is not None:
        print "Setting NoData to: %s" % NO_DATA
        outBand.SetNoDataValue(NO_DATA)

    # georeference the image and set the projection
    outDs.SetGeoTransform(ds.GetGeoTransform())
    outDs.SetProjection(ds.GetProjection())

    # build pyramids
    gdal.SetConfigOption('HFA_USE_RRD', 'YES')
    outDs.BuildOverviews(overviewlist=[2, 4, 8, 16, 32, 64, 128])

    ds = None
    outDs = None

    print('Calculation of %s took %s seconds to run\n'
          % (raster, time.time() - startTime))


# FIXME: how is xmid exactly handled? Now *must be* provided as a parameter
def sigmoidal_multiply_index(raster1, raster2, output, mod_asym, xmid, lxmod,
                             rxmod, lscale, rscale):

    startTime = time.time()

    # open the image
    raster_lpm = raster1
    print("Raster 1 (AVDIA): {0}".format(os.path.basename(raster_lpm)))
    raster_vol = raster2
    print("Raster 2 (VOL): {0}".format(os.path.basename(raster_vol)))
    output_name = os.path.join(output,
                               create_output_name(os.path.basename(raster_lpm)))
    print("Output: {0}".format(output_name))
    
    ds_lpm = gdal.Open(raster_lpm, GA_ReadOnly)
    ds_vol = gdal.Open(raster_vol, GA_ReadOnly)

    if ds_lpm is None:
        print 'Could not open %s' % raster_lpm
        sys.exit(1)
    elif ds_vol is None:
        print 'Could not open %s' % raster_vol
        sys.exit(1)

    # get raster 1 size
    rows_lpm = ds_lpm.RasterYSize
    cols_lpm = ds_lpm.RasterXSize

    # get raster 2 size
    rows_vol = ds_vol.RasterYSize
    cols_vol = ds_vol.RasterXSize

    # Check dimensions
    if rows_lpm != rows_vol or cols_lpm != cols_vol:
        print('Raster dimensions do not match: <%s %s> <%s %s>'
              % (rows_lpm, cols_lpm, rows_vol, cols_vol))
        sys.exit(1)

    # get the bands and block sizes
    inBand_lpm = ds_lpm.GetRasterBand(1)
    inBand_vol = ds_vol.GetRasterBand(1)

    # create the output image
    driver = gdal.GetDriverByName('HFA')
    outDs = driver.Create(output_name, cols_lpm, rows_lpm, 1, GDT_Float32)
    if outDs is None:
        print 'Could not create %s' % output_name
        sys.exit(1)
    outBand = outDs.GetRasterBand(1)

    # Get NoData

    NO_DATA = inBand_lpm.GetNoDataValue()
    if NO_DATA is not None:
        print 'NoData value: %s' % NO_DATA
    else:
        if inBand_lpm.DataType == GDT_Float32:
            NO_DATA = -3.40282346639e+38
            print 'NoData value not available, using default for GDT_Float32'
        else:
            print 'No NoData information available, defaulting to -1'
            NO_DATA = -1

    print 'Reading in data...'
    data_lpm = inBand_lpm.ReadAsArray()
    data_vol = inBand_vol.ReadAsArray()

    print 'Masking NoData...'
    ma_data_lpm = ma.masked_where(data_lpm == NO_DATA, data_lpm)
    ma_data_vol = ma.masked_where(data_vol == NO_DATA, data_vol)

    ma_lpm_max = ma_data_lpm.max()

    if not xmid:
        xmid = ma.median(ma_data_lpm)

    print 'Left Xmod: %s' % lxmod
    print 'Right Xmod: %s' % rxmod
    print 'Mod asym (if used): %s' % mod_asym
    print 'Left scale: %s' % lscale
    print 'Right scale: %s' % rscale

    print 'Data min: %s' % ma_data_lpm.min()
    print 'Data max: %s' % ma_data_lpm.max()
    print 'Data mean: %s' % ma_data_lpm.mean()
    print 'Data median: %s' % ma.median(ma_data_lpm)

    print 'Calculationg sigmoidal transformation...'
    ma_sig_lpm = np.where(ma_data_lpm <= xmid,
                          sigmoidal(ma_data_lpm, asym=mod_asym,
                                    xmid=xmid + (ma_lpm_max * lxmod),
                                    scale=(ma_lpm_max / lscale)),
                          sigmoidal(ma_data_lpm,
                                    xmid=xmid + (ma_lpm_max * rxmod),
                                    scale=(ma_lpm_max / rscale)))
    print 'Masked trans max: %s' % ma_sig_lpm.max()
    print 'Masked data (vol) max: %s' % ma_data_vol.max()
    ma_product = ma_sig_lpm * ma_data_vol
    print 'Masked index max: %s' % ma_product.max()

    #test_mid = xmid + (ma_lpm_max * rxmod)
    #test_scale = (ma_lpm_max / rscale)
    #print 'test_mid: %s' % test_mid
    #print 'test_scale: %s' % test_scale

    #test_val = sigmoidal(32.24, asym=mod_asym, xmid=test_mid, scale=test_scale)
    #print 'Testing calc: %s' % test_val

    # Write data
    data = ma.filled(ma_product, fill_value=NO_DATA)
    print 'Writing raster...'
    outBand.WriteArray(data)

    # flush data to disk, set the NoData value and calculate stats
    outBand.FlushCache()
    if NO_DATA is not None:
        print "Setting NoData to: %s" % NO_DATA
        outBand.SetNoDataValue(NO_DATA)

    # georeference the image and set the projection
    outDs.SetGeoTransform(ds_lpm.GetGeoTransform())
    outDs.SetProjection(ds_lpm.GetProjection())

    # build pyramids
    gdal.SetConfigOption('HFA_USE_RRD', 'YES')
    outDs.BuildOverviews(overviewlist=[2, 4, 8, 16, 32, 64, 128])

    ds_lpm = None
    ds_vol = None
    outDs = None

    print('Calculation of %s and %s took %s seconds to run\n'
          % (raster_lpm, raster_vol, time.time() - startTime))


def multiprocess_sigmoidal(rasters, params, processes=4):

    # Divide the rasters into equal subsets
    subsets = []
    no_rasters = len(rasters)
    # Calculate the modulo (is the number pf rasters dividable into equal sets?)
    modulo = no_rasters % processes
    # Extract the modulo so that the are equal sets
    division = no_rasters - modulo
    leap = division / processes
    for i in range(processes):
        if i != processes - 1:
            subset = rasters[i * leap: (i + 1) * leap]
        else:
            subset = rasters[i * leap: (i + 1) * leap + modulo]
        subsets.append(subset)

    print '%s rasters' % no_rasters
    print 'Using %s processes' % processes

    processList = []
    for r in range(processes):
        processList.append(subprocess.Popen([r"C:\Python26\python.exe",
                                            scriptPathList[r]],
                                            shell=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE))
        gp.addmessage("Launched process " + str(r) + "\n")
        time.sleep(2)


def process_sigmoidal(raw_rasters, params, idfield, outputdir, multiply=True):

    if multiply:

        no_rasters = len(raw_rasters)
        if no_rasters % 2 != 0:
            print 'An even number of rasters needed!'
            sys.exit(1)
        else:
            no_pairs = no_rasters / 2
            current_pair = 1

        rasters = raw_rasters
        rasters = []
        i = 0
        while i < no_rasters:
            rasters.append((raw_rasters[i], raw_rasters[i + 1]))
            i += 2

        for raster in rasters:
            a_raster = raster[0]
            b_raster = raster[1]
            ID1 = a_raster.get_tag('ID1')
            ID2 = a_raster.get_tag('ID2')
            if ID1 == b_raster.get_tag('ID1'):
                if ID2 == b_raster.get_tag('ID2'):

                    print("\n[{0} / {1}]".format(current_pair, no_pairs))
                    print('Workspace: %s' % os.path.dirname(a_raster.path))
                    print('Starting with %s and %s' % (a_raster.name,
                                                       b_raster.name))

                    try:
                        # Extract the parameter information from params
                        # DataFrame
                        mod_asym = params.where_field_equal(idfield,
                                                            int(ID1)).mod_asym
                        xmid = params.where_field_equal(idfield,
                                                        int(ID1)).median
                        lxmod = params.where_field_equal(idfield,
                                                         int(ID1)).xmod_lavdia
                        rxmod = params.where_field_equal(idfield,
                                                         int(ID1)).xmod_ravdia
                        lscale = params.where_field_equal(idfield,
                                                          int(ID1)).scaled_lavdia
                        rscale = params.where_field_equal(idfield,
                                                          int(ID1)).scaled_ravdia
                    except AttributeError:
                        print('Identifier %s not found in parameters list.'
                              % ID1)
                        continue

                    sigmoidal_multiply_index(a_raster.path, b_raster.path,
                                             outputdir, mod_asym=mod_asym,
                                             xmid=xmid,
                                             lxmod=lxmod, rxmod=rxmod,
                                             lscale=lscale, rscale=rscale)
                else:
                    print('ID2 do not match for %s and %s'
                          % (a_raster.name, b_raster.name))
                    print 'Skipping.'
            else:
                print('ID1 do not match for %s and %s'
                      % (a_raster.name, b_raster.name))
                print 'Skipping.'
            current_pair += 1

    else:
        for raster in raw_rasters:
            ID = raster.get_tag('ID1')
            print 'Workspace: %s' % os.path.dirname(raster.path)
            print 'Starting with %s' % (raster.name)

            try:
                # Extract the parameter information from params DataFrame
                mod_asym = params.where_field_equal(idfield, int(ID)).mod_asym
                lxmod = params.where_field_equal(idfield, int(ID)).xmod_lavdia
                rxmod = params.where_field_equal(idfield, int(ID)).xmod_ravdia
                lscale = params.where_field_equal(idfield,
                                                  int(ID)).scaled_lavdia
                rscale = params.where_field_equal(idfield,
                                                  int(ID)).scaled_ravdia

            except AttributeError:
                print 'Identifier %s not found in parameters list.' % ID
                continue

            sigmoidal_index(raster.path, outputdir, mod_asym=mod_asym,
                            lxmod=lxmod, rxmod=rxmod, lscale=lscale,
                            rscale=rscale)
