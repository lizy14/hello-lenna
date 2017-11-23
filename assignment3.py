'''
Assignment 3, histogram, gray level transformation
'''
# from libc cimport math
import cv233io
from utils import transformation
import numpy as np


def histogram(img, interval=4, channel=0):
    '''
    channel: 0 for all, 1 for R, 2 for G, 3 for B
    '''

    w = img.shape[0]
    h = img.shape[1]
    n = int(256 // interval)  # number of groups
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
