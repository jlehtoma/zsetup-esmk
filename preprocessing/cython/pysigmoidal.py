# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:13:55 2011

@author: admin_jlehtoma
"""

import numpy as np
import numpy.ma as ma

def py_asym_sigmoidal(x, xmid=None, asym=1.0, mod_asym=1.0, lscale=1.0, rscale=1.0):
    if xmid is None:
        xmid = ma.median(x)
    return np.where(x <= xmid, (asym * mod_asym) / (1 + ma.exp((xmid - x) / lscale)),
             asym / (1 + ma.exp((xmid - x) / rscale)))    
    
    #if x < xmid:
    #    return (asym * mod_asym) / (1 + ma.exp((xmid - x) / lscale))
    #else:    
    #    return asym / (1 + ma.exp((xmid - x) / rscale))
	
def py_sigmoidal(x, asym=1.0, xmid=None, scale=1.0):
    if xmid is None:
        xmid = ma.median(x)
    return asym / (1 + ma.exp((xmid - x) / scale))