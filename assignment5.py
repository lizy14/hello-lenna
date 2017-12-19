'''
Assignment 5: frequency domain filters
'''

import cv233io
from utils import *
import numpy as np

@transformation
def freqBlur(img, method='Gaussian', param=20):
    def freqBlurChannel(channel):
        spectrum = np.fft.fftshift(np.fft.fft2(channel))
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

        reconstructed = np.fft.ifft2(np.fft.ifftshift(spectrum))
        return reconstructed.real

    return clip_to_byte(apply_channelwise(img, freqBlurChannel)).astype(np.uint8)


@transformation
def freqSharpen(img, method='Gaussian', param=10):
    def freqSharpenChannel(channel):
        spectrum = np.fft.fftshift(np.fft.fft2(channel))
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
        reconstructed = np.fft.ifft2(np.fft.ifftshift(spectrum))
        return reconstructed.real
    return clip_to_byte(apply_channelwise(img, freqSharpenChannel)).astype(np.uint8)
