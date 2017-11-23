from contextlib import contextmanager
from timeit import default_timer

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
            result = func(*func_args, **func_kwargs)
            log.info("{} {} done at {:.0f} milliseconds".format(func.__name__, func_args[1:], elapsed() * 1000))
        return result
    return wrapper