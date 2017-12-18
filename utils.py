from contextlib import contextmanager
from timeit import default_timer
import numpy as np
import logging
log = logging.getLogger(__name__)

@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

def transformation(func):
    def wrapper(*func_args, **func_kwargs):
        with elapsed_timer() as elapsed:
            log.info("{} {} in progress ...".format(func.__name__, func_args[1:]))
            result = func(*func_args, **func_kwargs)
            log.info("{} {} done at {:.0f} milliseconds".format(func.__name__, func_args[1:], elapsed() * 1000))
        return result
    return wrapper

def split_channels(img):
    return img[:, :, 0], img[:, :, 1], img[:, :, 2]

def concat_channels(r, g, b):
    rgb = (r[..., np.newaxis], g[..., np.newaxis], b[..., np.newaxis])
    return np.concatenate(rgb, axis=-1)

def clip_to_byte(a):
    return np.minimum(np.maximum(a, 0), 255)