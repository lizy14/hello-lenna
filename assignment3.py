'''
Assignment 3, histogram, gray level transformation
'''
# from libc cimport math
import cv233io
from utils import transformation
import numpy as np


@transformation
def histogramEqualization(img):
    w = img.shape[0]
    h = img.shape[1]
    hist = histogram(img, channel=0) / w / h / 3
    cum = np.cumsum(hist)
    result = np.empty(img.shape)
    for y in range(h):
        for x in range(w):
            for c in range(3):
                result[y, x, c] = cum[img[y, x, c]] * 255
    return result


    
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

    def split_channels(img):
        return img[:, :, 0], img[:, :, 1], img[:, :, 2]

    def concat_channels(r, g, b):
        rgb = (r[..., np.newaxis], g[..., np.newaxis], b[..., np.newaxis])
        return np.concatenate(rgb, axis=-1)

    def clip_to_byte(a):
        return np.minimum(np.maximum(a, 0), 255)

    def channel_svd_compression(bitmap, depth):
        U, Sd, Vt = np.linalg.svd(bitmap, full_matrices=True)
        S = np.zeros(bitmap.shape, dtype=Sd.dtype) 
        S[:depth, :depth] = np.diag(Sd[:depth])
        return U.dot(S).dot(Vt)

    return clip_to_byte(
        concat_channels( 
            *map(
                lambda c:
                    channel_svd_compression(c, depth),
                split_channels(img)
            )
        )
    )
