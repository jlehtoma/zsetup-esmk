# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:16:50 2011

@author: admin_jlehtoma
"""

import time
def print_timing(func):
    def wrapper(*arg, **kwargs):
        t1 = time.time()
        res = func(*arg, **kwargs)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper