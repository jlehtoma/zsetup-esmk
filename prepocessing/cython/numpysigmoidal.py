# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 13:00:36 2011

@author: admin_jlehtoma
"""

import numpy as np

def numpy_asym_sigmoidal(x, xmid, asym=1.0, mod_asym=1.0, lscale=1.0, rscale=1.0):
    #ndx = np.where(np.sum(data, 0) <= xmid)
    ndx = np.where(data <= xmid)
    # only those data points that satisfy the condition (are even) 
    # are passed to one function then another and the result off applying both 
    # functions to each data point is stored in an array
    res = np.apply_along_axis( fnx2, 1, data[ndx,] )
