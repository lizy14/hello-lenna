'''
Assignment 4: Spacial Filters
DJANGO
'''

import cv233io
from utils import *
import numpy as np

@transformation
def gaussianFilter(img, sigma):
    def gaussian_kernel(sigma):
        l = np.ceil(3 * sigma * 2 // 2 + 1)
        axis = np.arange(-l // 2 + 1., l // 2 + 1.)
        x, y = np.meshgrid(axis, axis)
        kernel = np.exp(-(x**2 + y**2) / (2. * sigma**2))
        return kernel / np.sum(kernel)
        
    return applyKernelFilter(img, gaussian_kernel(sigma))


@transformation
def sharpen(img):
    SobelHorizontal = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1],
    ])
    SobelVertical = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    grad = np.absolute(applyKernelFilter(img, SobelVertical)) + np.absolute(applyKernelFilter(img, SobelHorizontal))
    return clip_to_byte(img + 0.1 * grad)

@transformation
def snow(img):
    k = 20
    snow = np.zeros(img.shape)

    sizes = np.random.randint(1, 10, size=100)

    height = img.shape[0]
    width = img.shape[1]

    for h in sizes:
        x = np.random.randint(width - h)
        y = np.random.randint(height - h)
        snow[y: y+h, x: x+h] = [255, 255, 255]

    snow = applyKernelFilter(snow, np.identity(k) / k)    
    
    return clip_to_byte(255 - np.multiply(1 - snow / 255, 255 - img))

def applyKernelFilter(img, kernel):
    assert(kernel.shape[0] == kernel.shape[1])
    kernel_size = kernel.shape[0]
    half_kernel_size = kernel_size // 2
    height = img.shape[0]
    width = img.shape[1]

    padded = concat_channels(*map(
        lambda channel: 
            np.pad(channel, (half_kernel_size, half_kernel_size), 'edge'), 
        split_channels(img)
    )).astype(np.uint8)
    result = np.zeros((width + kernel_size - 1, height + kernel_size - 1, 3))
    result = cv233io.new_img(width, height)

    for y in range(height):   
        print(y) 
        for x in range(width):
            original = padded[
                y: y + kernel_size,
                x: x + kernel_size
            ]
            weighted = np.multiply(
                original, 
                kernel[:, :, np.newaxis], 
            )
            result[y, x] = weighted.sum(axis=(0, 1))
            

    return result.astype(np.uint8)

@transformation
def medianFilter(img, kernel_size):

    assert(kernel_size % 2 == 1)
    assert(kernel_size > 0)

    half_kernel_size = kernel_size // 2
    shape = img.shape
    height = shape[0]
    width = shape[1]

    result = cv233io.new_img(width, height)
    padded = concat_channels(*map(
        lambda channel: 
            np.pad(channel, (half_kernel_size, half_kernel_size), 'edge'), 
        split_channels(img)
    ))

    '''
     01234567
    -++++++++-
    0123456789
    [-]    [-]
     01234567
    '''

    for y in range(height):    
        for x in range(width):
            np.median(
                padded[
                    y: y + kernel_size,
                    x: x + kernel_size
                ],
                (0, 1),
                out=result[y, x]
            )

    return result
