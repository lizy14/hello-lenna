import math
import cv233io
from utils import elapsed_timer

def transformation(func):
    def wrapper(*func_args, **func_kwargs):
        with elapsed_timer() as elapsed:
            result = func(*func_args, **func_kwargs)
            print(func.__name__ + " done at %.2f seconds" % elapsed())
        return result
    return wrapper

@transformation
def rotate(img, degree):

    shape = img.shape

    h = shape[0]
    w = shape[1]
    hw = w // 2 # leading h: half
    hh = h // 2

    θ = (degree / 360) * 2 * math.pi
    cosθ = math.cos(θ)
    sinθ = math.sin(θ)

    # trailing underscore: after transformation
    w_ = int(w * cosθ + h * sinθ)
    h_ = int(w * sinθ + h * cosθ)
    hw_ = w_ // 2
    hh_ = h_ // 2

    img_ = cv233io.new_img(w_, h_)
    
    for y_ in range(h_):
        for x_ in range(w_):
            # leading underscore: relative to center
            
            _x_ = x_ - hw_
            _y_ = y_ - hh_
            _x = _x_ * cosθ + _y_ * sinθ
            _y = - _x_ * sinθ + _y_ * cosθ
            x = int(_x) + hw
            y = int(_y) + hh
            
            if x >= 0 and x < w and y >= 0 and y < h:
                pixel = img[y, x]
                img_[y_, x_] = pixel
        
    return img_

@transformation
def vertical_flip(img):
    return img[::-1]

@transformation
def horizontal_flip(img):
    return img[:,::-1]

@transformation
def transpose(img):
    shape = img.shape
    h = shape[0]
    w = shape[1]
    img_ = cv233io.new_img(h, w)
    for y in range(h):
        for x in range(w):
            img_[x, y] = img[y, x]
    return img_

@transformation
def crop(img, xmin, xmax, ymin, ymax):
    w_ = xmax - xmin
    h_ = ymax - ymin
    img_ = cv233io.new_img(w_, h_)
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            img_[y - ymin, x - xmin] = img[y, x]
    return img_