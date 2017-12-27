'''
assignment 6: artistic effect
'''

import numpy as np
import cv2
from utils import *
from assignment5 import freqChannel
import logging
log = logging.getLogger(__name__)

@transformation
def pencil(img, param):
    img_gray = rgb_to_gray(img)
    img_blur = freqChannel(img_gray, 'Blur', 'Gaussian', param)
    img_blend = clip_to_byte(img_gray * 256. / img_blur)
    return gray_to_rgb(img_blend)

@transformation
def dehaze(img):
    (dark, rawt, refinedt, rawrad, rerad) = dehaze_internal(img)
    return rerad

'''
ref: https://github.com/joyeecheung/dark-channel-prior-dehazing
'''

from itertools import combinations_with_replacement
from collections import defaultdict
from numpy.linalg import inv

R, G, B = 0, 1, 2  # index for convenience
L = 256  # color depth




def get_atmosphere(I, darkch, p):
    """Get the atmosphere light in the (RGB) image data.

    Parameters
    -----------
    I:      the M * N * 3 RGB image data ([0, L-1]) as numpy array
    darkch: the dark channel prior of the image as an M * N numpy array
    p:      percentage of pixels for estimating the atmosphere light

    Return
    -----------
    A 3-element array containing atmosphere light ([0, L-1]) for each channel
    """
    # reference CVPR09, 4.4
    M, N = darkch.shape
    flatI = I.reshape(M * N, 3)
    flatdark = darkch.ravel()
    searchidx = (-flatdark).argsort()[:int(M * N * p)]  # find top M * N * p indexes
    log.info('atmosphere light region: {}'.format([(i / N, i % N) for i in searchidx]))

    # return the highest intensity for each channel
    return np.max(flatI.take(searchidx, axis=0), axis=0)


def get_transmission(I, A, darkch, omega, w):
    """Get the transmission esitmate in the (RGB) image data.

    Parameters
    -----------
    I:       the M * N * 3 RGB image data ([0, L-1]) as numpy array
    A:       a 3-element array containing atmosphere light
             ([0, L-1]) for each channel
    darkch:  the dark channel prior of the image as an M * N numpy array
    omega:   bias for the estimate
    w:       window size for the estimate

    Return
    -----------
    An M * N array containing the transmission rate ([0.0, 1.0])
    """
    return 1 - omega * get_dark_channel(I / A, w)  # CVPR09, eq.12


def dehaze_raw(I, tmin=0.2, Amax=220, w=15, p=0.0001,
               omega=0.95, guided=True, r=40, eps=1e-3):
  """Get the dark channel prior, atmosphere light, transmission rate
       and refined transmission rate for raw RGB image data.

    Parameters
    -----------
    I:      M * N * 3 data as numpy array for the hazy image
    tmin:   threshold of transmission rate
    Amax:   threshold of atmosphere light
    w:      window size of the dark channel prior
    p:      percentage of pixels for estimating the atmosphere light
    omega:  bias for the transmission estimate

    guided: whether to use the guided filter to fine the image
    r:      the radius of the guidance
    eps:    epsilon for the guided filter

    Return
    -----------
    (Idark, A, rawt, refinedt) if guided=False, then rawt == refinedt
    """
  with elapsed_timer() as elapsed:
    m, n, _ = I.shape
    Idark = get_dark_channel(I, w)
    log.info(elapsed())

    A = get_atmosphere(I, Idark, p)
    A = np.minimum(A, Amax)  # threshold A
    
    log.debug('atmosphere {}'.format(A))
    log.info(elapsed())    

    rawt = get_transmission(I, A, Idark, omega, w)
    log.debug('raw transmission rate between [{}, {}]'.format(rawt.min(), rawt.max()))
    log.info(elapsed())

    rawt = refinedt = np.maximum(rawt, tmin)  # threshold t
    if guided:
        normI = (I - I.min()) / (I.max() - I.min())  # normalize I
        refinedt = guided_filter(normI, refinedt, r, eps)
    
    log.debug('refined transmission rate between [{}, {}]'.format(refinedt.min(), refinedt.max()))
    log.info(elapsed())
    return Idark, A, rawt, refinedt


def get_radiance(I, A, t):
    """Recover the radiance from raw image data with atmosphere light
       and transmission rate estimate.

    Parameters
    ----------
    I:      M * N * 3 data as numpy array for the hazy image
    A:      a 3-element array containing atmosphere light
            ([0, L-1]) for each channel
    t:      estimate fothe transmission rate

    Return
    ----------
    M * N * 3 numpy array for the recovered radiance
    """
    tiledt = np.zeros_like(I)  # tiled to M * N * 3
    tiledt[:, :, R] = tiledt[:, :, G] = tiledt[:, :, B] = t
    return (I - A) / tiledt + A  # CVPR09, eq.16


def dehaze_internal(im, tmin=0.2, Amax=220, w=15, p=0.0001,
           omega=0.95, guided=True, r=40, eps=1e-3):
    """Dehaze the given RGB image.

    Parameters
    ----------
    im:     the Image object of the RGB image
    guided: refine the dehazing with guided filter or not
    other parameters are the same as `dehaze_raw`

    Return
    ----------
    (dark, rawt, refinedt, rawrad, rerad)
    Images for dark channel prior, raw transmission estimate,
    refiend transmission estimate, recovered radiance with raw t,
    recovered radiance with refined t.
    """
    I = np.asarray(im, dtype=np.float64)
    Idark, A, rawt, refinedt = dehaze_raw(I, tmin, Amax, w, p,
                                          omega, guided, r, eps)
    white = np.full_like(Idark, L - 1)

    def to_img(raw):
        # threshold to [0, L-1]
        cut = np.maximum(np.minimum(raw, L - 1), 0).astype(np.uint8)
        return cut

    return [to_img(raw) for raw in (Idark, white * rawt, white * refinedt,
                                    get_radiance(I, A, rawt),
                                    get_radiance(I, A, refinedt))]

def get_dark_channel(I, w):
    """Get the dark channel prior in the (RGB) image data.

    Parameters
    -----------
    I:  an M * N * 3 numpy array containing data ([0, L-1]) in the image where
        M is the height, N is the width, 3 represents R/G/B channels.
    w:  window size

    Return
    -----------
    An M * N array for the dark channel prior ([0, L-1]).
    """
    M = I.shape[0]
    N = I.shape[1]
    padded = np.pad(I, ((w // 2, w // 2), (w // 2, w // 2), (0, 0)), 'edge')
    darkch = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            darkch[i, j] = np.min(padded[i:i + w, j:j + w, :])  # CVPR09, eq.5
    return darkch

def boxfilter(I, r):
    """Fast box filter implementation.

    Parameters
    ----------
    I:  a single channel/gray image data normalized to [0.0, 1.0]
    r:  window radius

    Return
    -----------
    The filtered image data.
    """
    M, N = I.shape
    dest = np.zeros((M, N))

    # cumulative sum over Y axis
    sumY = np.cumsum(I, axis=0)
    # difference over Y axis
    dest[:r + 1] = sumY[r: 2 * r + 1]
    dest[r + 1:M - r] = sumY[2 * r + 1:] - sumY[:M - 2 * r - 1]
    dest[-r:] = np.tile(sumY[-1], (r, 1)) - sumY[M - 2 * r - 1:M - r - 1]

    # cumulative sum over X axisP
    sumX = np.cumsum(dest, axis=1)
    # difference over Y axis
    dest[:, :r + 1] = sumX[:, r:2 * r + 1]
    dest[:, r + 1:N - r] = sumX[:, 2 * r + 1:] - sumX[:, :N - 2 * r - 1]
    dest[:, -r:] = np.tile(sumX[:, -1][:, None], (1, r)) - \
        sumX[:, N - 2 * r - 1:N - r - 1]

    return dest


def guided_filter(I, p, r=40, eps=1e-3):
    """Refine a filter under the guidance of another (RGB) image.

    Parameters
    -----------
    I:   an M * N * 3 RGB image for guidance.
    p:   the M * N filter to be guided
    r:   the radius of the guidance
    eps: epsilon for the guided filter

    Return
    -----------
    The guided filter.
    """
    M, N = p.shape
    base = boxfilter(np.ones((M, N)), r)

    # each channel of I filtered with the mean filter
    means = [boxfilter(I[:, :, i], r) / base for i in range(3)]
    # p filtered with the mean filter
    mean_p = boxfilter(p, r) / base
    # filter I with p then filter it with the mean filter
    means_IP = [boxfilter(I[:, :, i] * p, r) / base for i in range(3)]
    # covariance of (I, p) in each local patch
    covIP = [means_IP[i] - means[i] * mean_p for i in range(3)]

    # variance of I in each local patch: the matrix Sigma in ECCV10 eq.14
    var = defaultdict(dict)
    for i, j in combinations_with_replacement(range(3), 2):
        var[i][j] = boxfilter(
            I[:, :, i] * I[:, :, j], r) / base - means[i] * means[j]

    a = np.zeros((M, N, 3))
    for y, x in np.ndindex(M, N):
        #         rr, rg, rb
        # Sigma = rg, gg, gb
        #         rb, gb, bb
        Sigma = np.array([[var[R][R][y, x], var[R][G][y, x], var[R][B][y, x]],
                          [var[R][G][y, x], var[G][G][y, x], var[G][B][y, x]],
                          [var[R][B][y, x], var[G][B][y, x], var[B][B][y, x]]])
        cov = np.array([c[y, x] for c in covIP])
        a[y, x] = np.dot(cov, inv(Sigma + eps * np.eye(3)))  # eq 14

    # ECCV10 eq.15
    b = mean_p - a[:, :, R] * means[R] - \
        a[:, :, G] * means[G] - a[:, :, B] * means[B]

    # ECCV10 eq.16
    q = (boxfilter(a[:, :, R], r) * I[:, :, R] + boxfilter(a[:, :, G], r) *
         I[:, :, G] + boxfilter(a[:, :, B], r) * I[:, :, B] + boxfilter(b, r)) / base

    return q
