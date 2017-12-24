'''
Assignment 5: frequency domain filters
'''

import cv233io
from utils import *
import numpy as np

def fft(channel):
    return np.fft.fftshift(np.fft.fft2(channel))

def ifft(spectrum):
    return np.fft.ifft2(np.fft.ifftshift(spectrum)).real


def freqChannel(channel, direction, method, param):

    if method == 'Ideal':
        r = param
        if direction == 'Sharpen':
            mask = lambda x, y: .1 + (x*x + y*y >= r*r)
        else:
            mask = lambda x, y: x*x + y*y <= r*r
    elif method == 'Gaussian':
        sigma = param
        if direction == 'Sharpen':
            mask = lambda x, y: .1 + 1 - np.exp(-(x**2 + y**2) / (2. * sigma**2))
        else:
            mask = lambda x, y: np.exp(-(x**2 + y**2) / (2. * sigma**2))

    return freqApplyMaskChannel(channel, mask)


def freqApplyMaskChannel(channel, maskFunction):
    spectrum = fft(channel)

    w = spectrum.shape[0]
    h = spectrum.shape[1]
    y, x = np.ogrid[
        -h // 2 : h // 2, 
        -w // 2 : w // 2
    ]

    mask = maskFunction(x, y)

    spectrum = np.multiply(spectrum, mask)
    return ifft(spectrum)

@transformation
def freqBlur(img, method='Gaussian', param=20):
    return clip_to_byte(apply_channelwise(img, lambda c: freqChannel(c, 'Blur', method, param)))

@transformation
def freqSharpen(img, method='Gaussian', param=10):
    return clip_to_byte(apply_channelwise(img, lambda c: freqChannel(c, 'Sharpen', method, param)))

