'''
Assignment 3, histogram, gray level transformation
'''
#from libc cimport math
import cv233io
from utils import transformation
import numpy as np

def histogram(img, interval=4, channel=0):
    '''
    channel: 0 for all, 1 for R, 2 for G, 3 for B
    '''

    w = img.shape[0]
    h = img.shape[1]
    n = int(256 // interval) # number of groups
    result = np.zeros((n,), dtype='int32')
    for y in range(h):
        for x in range(w):
            if channel == 0:
                pixel = img[y, x].mean()
            else:
                pixel = img[y, x, channel - 1]
            group = int(pixel // interval)
            result[group] += 1
            
    return result