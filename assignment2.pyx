from libc cimport math
import cv233io
from utils import transformation
from numpy cimport ndarray as array_t
from numpy cimport uint8_t as uint8_t

cdef inline int value_to_radius(int value, int spacing, float gamma):
    cdef float x = 1. - (value / 255.)
    cdef float y
    if x > .5:
        y = 1.
    else:
        y = math.pow(x / .5, gamma)
    return <int>(y * spacing / 2)

@transformation
def colorHalftone(array_t[uint8_t, ndim=3] img, int spacing=8, float gamma=.5):


    shape = img.shape
    cdef int height = shape[0]
    cdef int width = shape[1]
    cdef array_t[uint8_t, ndim=3] img_ = cv233io.new_img(width, height)
    
    cdef int y, x, dy, dx, r
    for y in range(-10 * height, 10 * height, spacing):
        for x in range(-10 * width, 10 * width, spacing):
            if x >= 0 and x < width and y >= 0 and y < height:
                r = value_to_radius(img[y, x, 0], spacing, gamma)
                for dy in range(-r, r):
                    for dx in range(-r, r):
                        if dy * dy + dx * dx <= r * r + 1:
                            if x+dx >= 0 and x+dx < width and y+dy >= 0 and y+dy < height:
                                img_[y+dy, x+dx, 0] = img[y+dy, x+dx, 0]
    
    for y in range(-10 * height, 10 * height, spacing):
        for x in range(-10 * width, 10 * width, spacing):
            y -= <int>(.3 * spacing)
            x += <int>(.3 * spacing)
            if x >= 0 and x < width and y >= 0 and y < height:
                r = value_to_radius(img[y, x, 1], spacing, gamma)
                for dy in range(-r, r):
                    for dx in range(-r, r):
                        if dy * dy + dx * dx <= r * r + 1:
                            if x+dx >= 0 and x+dx < width and y+dy >= 0 and y+dy < height:
                                img_[y+dy, x+dx, 1] = img[y+dy, x+dx, 1]

    for y in range(-10 * height, 10 * height, spacing):
        for x in range(-10 * width, 10 * width, spacing):
            y -= <int>(.7 * spacing)
            x += <int>(.7 * spacing)
            if x >= 0 and x < width and y >= 0 and y < height:
                r = value_to_radius(img[y, x, 2], spacing, gamma)
                for dy in range(-r, r):
                    for dx in range(-r, r):
                        if dy * dy + dx * dx <= r * r + 1:
                            if x+dx >= 0 and x+dx < width and y+dy >= 0 and y+dy < height:
                                img_[y+dy, x+dx, 2] = img[y+dy, x+dx, 2]

    return img_

@transformation
def convertRgbToHsv(array_t[uint8_t, ndim=3] img):
    shape = img.shape
    cdef int height = shape[0]
    cdef int width = shape[1]
    cdef array_t[uint8_t, ndim=3] img_ = cv233io.new_img(width, height)

    cdef float h, s, v
    cdef float r, g, b, min_, max_
    cdef int x, y
    for y in range(height):
        for x in range(width):
            r = img[y, x, 0] / 255.
            g = img[y, x, 1] / 255.
            b = img[y, x, 2] / 255.
            
            max_ = max(r, g, b)
            min_ = min(r, g, b)
            v = max_
            s = ((v - min_) / v) if v != 0 else 0
            if min_ == max_: # r = g = b
                h = 0
            elif v == r:
                h = 60 * (g - b) / (v - min_)
            elif v == g:
                h = 120 + 60 * (b - r) / (v - min_)
            elif v == b:
                h = 240 + 60 * (r - g) / (v - min_)
            if h < 0:
                h += 360
            img_[y, x, 0] = <int>(h / 2.)
            img_[y, x, 1] = <int>(s * 255)
            img_[y, x, 2] = <int>(v * 255)
    return img_


@transformation
def convertHsvToRgb(array_t[uint8_t, ndim=3] img):
    shape = img.shape
    cdef int height = shape[0]
    cdef int width = shape[1]
    cdef array_t[uint8_t, ndim=3] img_ = cv233io.new_img(width, height)

    cdef float h, s, v
    cdef float r, g, b
    cdef float f, p, q, t
    cdef float h60, h60f
    cdef int hi
    cdef int x, y
    for y in range(height):
        for x in range(width):
            h = img[y, x, 0] * 2.
            s = img[y, x, 1] / 255.
            v = img[y, x, 2] / 255.
            
            h60 = h / 60.0
            h60f = math.floor(h60)
            hi = <int>h60f % 6
            f = h60 - h60f
            p = v * (1 - s)
            q = v * (1 - f * s)
            t = v * (1 - (1 - f) * s)
            
            r, g, b = 0, 0, 0
            if hi == 0: 
                r, g, b = v, t, p
            elif hi == 1: 
                r, g, b = q, v, p
            elif hi == 2: 
                r, g, b = p, v, t
            elif hi == 3: 
                r, g, b = p, q, v
            elif hi == 4: 
                r, g, b = t, p, v
            elif hi == 5: 
                r, g, b = v, p, q
            
            img_[y, x, 0] = <int>(r * 255)
            img_[y, x, 1] = <int>(g * 255)
            img_[y, x, 2] = <int>(b * 255)
    return img_

@transformation
def changeHsv(array_t[uint8_t, ndim=3] img, float h_, float s_, float v_):
    ''' s_, v_ in range [-1, 1], h in range [0, 1] '''
    shape = img.shape
    cdef int height = shape[0]
    cdef int width = shape[1]
    cdef array_t[uint8_t, ndim=3] img_ = cv233io.new_img(width, height)
    
    cdef float h, s, v
    cdef int x, y
    for y in range(height):
        for x in range(width):
            h = img[y, x, 0] / 180. # / 2 * 360
            s = img[y, x, 1] / 255.
            v = img[y, x, 2] / 255.
            h += h_
            if h > 1: h -= 1

            s *= math.exp(2 * s_)
            if s > 1: s = 1
            if s < 0: s = 0
            v *= math.exp(2 * v_)
            if v > 1: v = 1
            if v < 0: v = 0

            img_[y, x, 0] = <int>(h * 180)
            img_[y, x, 1] = <int>(s * 255)
            img_[y, x, 2] = <int>(v * 255)
    return img_