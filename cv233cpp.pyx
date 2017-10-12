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
def rotate(cnp.ndarray[cnp.uint8_t, ndim=3] img, float degree):

    shape = img.shape

    cdef int h = shape[0]
    cdef int w = shape[1]
    cdef int hw = w // 2 # leading h: half
    cdef int hh = h // 2

    cdef float theta = (degree / 360) * 2 * math.pi
    cdef float costheta = math.cos(theta)
    cdef float sintheta = math.sin(theta)

    # trailing underscore: after transformation
    cdef int w_ = <int>(w * costheta + h * sintheta)
    cdef int h_ = <int>(w * sintheta + h * costheta)
    cdef int hw_ = w_ // 2
    cdef int hh_ = h_ // 2

    cdef cnp.ndarray[cnp.uint8_t, ndim=3] img_ = cv233io.new_img(w_, h_)
    
    cdef int _x_, _y_, x_, y_, _x, _y, x, y
    cdef int c

    for y_ in range(h_):
        for x_ in range(w_):
            # leading underscore: relative to center
            
            _x_ = x_ - hw_
            _y_ = y_ - hh_
            _x = <int>(_x_ * costheta + _y_ * sintheta)
            _y = <int>(- _x_ * sintheta + _y_ * costheta)
            x = _x + hw
            y = _y + hh
            
            if x >= 0 and x < w and y >= 0 and y < h:
                for c in range(3):
                    img_[y_, x_, c] = img[y, x, c]
                
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
