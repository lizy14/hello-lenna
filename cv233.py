import math
import cv233io
from utils import elapsed_timer

def rotate(img, degree):
    with elapsed_timer() as elapsed:
        shape = img.shape

        w = shape[0]
        h = shape[1]
        hw = w / 2 # trailing h: half
        hh = h / 2

        θ = (degree / 360) * 2 * math.pi
        cosθ = math.cos(θ)
        sinθ = math.sin(θ)

        # trailing underscore: after transformation
        w_ = math.ceil(w * cosθ + h * sinθ)
        h_ = math.ceil(w * sinθ + h * cosθ)
        hw_ = w_ / 2
        hh_ = h_ / 2

        img_ = cv233io.new_img(w_, h_)

        for x_ in range(w_):
            for y_ in range(h_):
                # leading underscore: relative to center
                _x_ = x_ - hw_
                _y_ = y_ - hh_
                _x = _x_ * cosθ + _y_ * sinθ
                _y = - _x_ * sinθ + _y_ * cosθ
                x = math.floor(_x + hw)
                y = math.floor(_y + hh)
                if x >= 0 and x < w and y >= 0 and y < h:
                    img_[y_][x_] = img[y, x]

        print( "all done at %.2f seconds" % elapsed() )

    return img_


def vertical_flip(img):
    return img[::-1]


def horizontal_flip(img):
    return [i[::-1] for i in img]


def transpose(img):
    return list(map(list, zip(*img)))
