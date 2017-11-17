from libc cimport math
import cv233io
from utils import elapsed_timer, transformation
from numpy cimport ndarray as array_t
from numpy cimport uint8_t as uint8_t



@transformation
def rotate(array_t[uint8_t, ndim=3] img, float degree):

    shape = img.shape

    cdef int h = shape[0]
    cdef int w = shape[1]
    cdef float hw = w / 2. # leading h: half
    cdef float hh = h / 2.

    cdef float theta = (degree / 360.) * 2 * math.pi
    cdef float costheta = math.cos(theta)
    cdef float sintheta = math.sin(theta)

    # trailing underscore: after transformation
    cdef int w_ = <int>(w * costheta + h * sintheta)
    cdef int h_ = <int>(w * sintheta + h * costheta)
    cdef array_t[uint8_t, ndim=3] img_ = cv233io.new_img(w_, h_)
    cdef float hw_ = w_ / 2.
    cdef float hh_ = h_ / 2.
    
    cdef int x1, x2, y1, y2
    cdef int q11, q12, q21, q22
    cdef float q_1, q_2, q__
    cdef float x, y
    cdef int x_, y_, c
    for y_ in range(h_):
        for x_ in range(w_):
            x = + (x_ - hw_) * costheta + (y_ - hh_) * sintheta + hw
            y = - (x_ - hw_) * sintheta + (y_ - hh_) * costheta + hh

            x1 = <int>math.floor(x)
            x2 = x1 + 1
            y1 = <int>math.floor(y)
            y2 = y1 + 1

            if x1 >= 0 and x2 < w and y1 >= 0 and y2 < h:
                for c in range(3):
                    q11 = img[y1, x1, c]
                    q12 = img[y2, x1, c]
                    q21 = img[y1, x2, c]
                    q22 = img[y2, x2, c]
                    q_1 = (x2 - x) * q11 + (x - x1) * q21
                    q_2 = (x2 - x) * q12 + (x - x1) * q22
                    q__ = (y2 - y) * q_1 + (y - y1) * q_2
                    img_[y_, x_, c] = <int>math.round(q__)
                
    return img_

@transformation
def vertical_flip(img):
    return img[::-1]

@transformation
def horizontal_flip(img):
    return img[:,::-1]

@transformation
def transpose(array_t[uint8_t, ndim=3] img):
    shape = img.shape
    cdef int h = shape[0]
    cdef int w = shape[1]
    cdef array_t[uint8_t, ndim=3] img_ = cv233io.new_img(h, w)
    cdef int x, y
    for y in range(h):
        for x in range(w):
            for c in range(3):
                img_[x, y, c] = img[y, x, c]
    return img_

@transformation
def crop(array_t[uint8_t, ndim=3] img, int xmin, int xmax, int ymin, int ymax, int circular=0):
    shape = img.shape
    cdef int h = shape[0]
    cdef int w = shape[1]

    cdef int w_ = xmax - xmin
    cdef int h_ = ymax - ymin
    cdef array_t[uint8_t, ndim=3] img_ = cv233io.new_img(w_, h_)
    cdef float cx = (xmax + xmin) / 2
    cdef float cy = (ymax + ymin) / 2
    cdef float hh = h_ / 2
    cdef float hw = w_ / 2

    cdef int x, y, c

    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            if x >= 0 and x < w and y >= 0 and y < h and (
                not circular or (x - cx) ** 2 / hw ** 2 + (y - cy) ** 2 / hh ** 2 < 1.):
                for c in range(3):
                    img_[y - ymin, x - xmin, c] = img[y, x, c]
            else:
                for c in range(3):
                    img_[y - ymin, x - xmin, c] = 255

    return img_
