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


def freqBlurChannel(channel, method, param):
    spectrum = fft(channel)

    w = spectrum.shape[0]
    h = spectrum.shape[1]
    y, x = np.ogrid[
        -h // 2 : h // 2, 
        -w // 2 : w // 2
    ]

    if method == 'Ideal':
        r = param
        mask = x*x + y*y <= r*r
    elif method == 'Gaussian':
        sigma = param
        mask = np.exp(-(x**2 + y**2) / (2. * sigma**2))
    
    spectrum = np.multiply(spectrum, mask)
    return ifft(spectrum)


def freqSharpenChannel(channel, method, param):
    spectrum = fft(channel)

    w = spectrum.shape[0]
    h = spectrum.shape[1]
    y, x = np.ogrid[
        -h // 2 : h // 2, 
        -w // 2 : w // 2
    ]

    if method == 'Ideal':
        r = param
        mask = x*x + y*y >= r*r
    elif method == 'Gaussian':
        sigma = param
        mask = 1 - np.exp(-(x**2 + y**2) / (2. * sigma**2))

    spectrum = np.multiply(spectrum, mask + .1)
    return ifft(spectrum)

@transformation
def freqBlur(img, method='Gaussian', param=20):
    return clip_to_byte(apply_channelwise(img, lambda c: freqBlurChannel(c, method, param)))

@transformation
def freqSharpen(img, method='Gaussian', param=10):
    return clip_to_byte(apply_channelwise(img, lambda c: freqSharpenChannel(c, method, param)))
