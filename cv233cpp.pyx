from libc cimport math
import cv233io
from utils import elapsed_timer
cimport numpy as cnp

def transformation(func):
    def wrapper(*func_args, **func_kwargs):
        with elapsed_timer() as elapsed:
            result = func(*func_args, **func_kwargs)
            print(func.__name__ + " done at %.2f seconds" % elapsed())
        return result
    return wrapper


@transformation
def changeHsv(cnp.ndarray[cnp.uint8_t, ndim=3] img, float h_degree, float s_percentage, float v_percentage):
    shape = img.shape
    cdef int height = shape[0]
    cdef int width = shape[1]

    cdef cnp.ndarray[cnp.uint8_t, ndim=3] img_ = cv233io.new_img(width, height)

    cdef int x, y
    
    cdef float h, s, v
    for y in range(height):
        for x in range(width):
            h = img[y, x, 0] / 180.
            s = img[y, x, 1] / 255.
            v = img[y, x, 2] / 255.
            h += h_degree
            if h > 1: h -= 1

            s += s_percentage
            if s > 1: s = 1
            if s < 0: s = 0
            v += v_percentage
            if v > 1: v = 1
            if v < 0: v = 0

            img_[y, x, 0] = <int>(h * 180)
            img_[y, x, 1] = <int>(s * 255)
            img_[y, x, 2] = <int>(v * 255)
    return img_

@transformation
def rotate(cnp.ndarray[cnp.uint8_t, ndim=3] img, float degree):

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
    cdef float hw_ = w_ / 2.
    cdef float hh_ = h_ / 2.

    cdef cnp.ndarray[cnp.uint8_t, ndim=3] img_ = cv233io.new_img(w_, h_)

    cdef int c    
    cdef int x_, y_
    cdef float x, y
    cdef int x1, x2, y1, y2
    cdef int q11, q12, q21, q22
    cdef float q_1, q_2, q__

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
def transpose(cnp.ndarray[cnp.uint8_t, ndim=3] img):
    shape = img.shape
    cdef int h = shape[0]
    cdef int w = shape[1]
    cdef cnp.ndarray[cnp.uint8_t, ndim=3] img_ = cv233io.new_img(h, w)
    cdef int x, y
    for y in range(h):
        for x in range(w):
            for c in range(3):
                img_[x, y, c] = img[y, x, c]
    return img_

@transformation
def crop(cnp.ndarray[cnp.uint8_t, ndim=3] img, int xmin, int xmax, int ymin, int ymax):
    shape = img.shape
    cdef int h = shape[0]
    cdef int w = shape[1]

    cdef int w_ = xmax - xmin
    cdef int h_ = ymax - ymin
    cdef cnp.ndarray[cnp.uint8_t, ndim=3] img_ = cv233io.new_img(w_, h_)
    
    cdef int x, y, c
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            if x >= 0 and x < w and y >= 0 and y < h:
                for c in range(3):
                    img_[y - ymin, x - xmin, c] = img[y, x, c]
            else:
                for c in range(3):
                    img_[y - ymin, x - xmin, c] = 255
                
    return img_
