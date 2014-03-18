# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:21:14 2011

@author: admin_jlehtoma
"""
import numpy as np
import numpy.ma as ma
from utils import print_timing
from pysigmoidal import py_asym_sigmoidal, py_sigmoidal

@print_timing
def run_py_asym_sigmoidal(data):
    #f = np.vectorize(py_asym_sigmoidal)    
    return py_asym_sigmoidal(data)

@print_timing
def run_py_sigmoidal(data):
    return py_sigmoidal(data)
    
@print_timing
def run_numpy_asym_sigmoidal(data):
    xmid = ma.median(data)
    ndx = np.where(data <= xmid)
    # only those data points that satisfy the condition (are even) 
    # are passed to one function then another and the result off applying both 
    # functions to each data point is stored in an array
    res = np.apply_along_axis( fnx2, 1, data[ndx,] )

if __name__ == '__main__':

    dim = 3000

    data = np.random.rand(dim, dim)
    mask = np.random.binomial(1, 0.5, dim ** 2).reshape(dim, dim)
    ma_data = ma.array(data, mask=mask)
    
    t1data = run_py_asym_sigmoidal(ma_data)
    t2data = run_py_sigmoidal(ma_data)
    
