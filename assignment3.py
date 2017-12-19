'''
Assignment 3, histogram, gray level transformation
'''

import cv233io
from utils import *
import numpy as np


@transformation
def histogramEqualization(img):
    hist = histogram(img, channel=0) / img.size
    cum = np.cumsum(hist) * 255
    return grayscaleTransformation(img, cum.astype(np.uint8))


@transformation
def grayscaleTransformation(img, mapping):
    return mapping[img]
    
def histogram(img, channel=0):
    ''' 
    channel: -1 for gray, 0 for RGB, 1 for R, 2 for G, 3 for B
    '''

    if channel == 0:
        pixels = img.flatten()
    elif channel == -1:
        pixels = np.mean(img, axis=2)
    else:
        pixels = img[:, :, channel - 1]

    hist, _ = np.histogram(pixels, bins=256, range=(0, 255))
    return hist


@transformation
def svdCompression(img, depth):

    def channel_svd_compression(bitmap, depth):
        U, Sd, Vt = np.linalg.svd(bitmap, full_matrices=True)
        S = np.zeros(bitmap.shape, dtype=Sd.dtype) 
        S[:depth, :depth] = np.diag(Sd[:depth])
        return U.dot(S).dot(Vt)

    return clip_to_byte(apply_channelwise(
        img, 
        lambda c:
            channel_svd_compression(c, depth)
    ))
