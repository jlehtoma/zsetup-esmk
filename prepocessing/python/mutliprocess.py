#!/usr/bin/env python

import multiprocessing
import threading
import time

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper


def counter():
    for i in xrange(1000000):
        pass

@print_timing
def serialrun(x):
    for i in xrange(x):
        counter()

@print_timing
def parallelrun(x):
    proclist = []
    for i in xrange(x):
        p = multiprocessing.Process(target=counter)
        proclist.append(p)
        p.start()

    for i in proclist:
        i.join()

@print_timing
def threadedrun(x):
    threadlist = []
    for i in xrange(x):
        t = threading.Thread(target=counter)
        threadlist.append(t)
        t.start()

    for i in threadlist:
        i.join()

def main():
    serialrun(50)
    parallelrun(50)
    threadedrun(50)

if __name__ == '__main__':
    main()