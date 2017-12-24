'''
assignment 6: artistic effect
'''

import numpy as np
import cv2
from utils import *
from assignment5 import freqBlurChannel

@transformation
def pencil(img, param):
    img_gray = rgb_to_gray(img)
    img_blur = freqBlurChannel(img_gray, 'Gaussian', param)
    img_blend = clip_to_byte(img_gray * 256. / img_blur)
    return gray_to_rgb(img_blend)
