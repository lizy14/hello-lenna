# Cython compile instructions

from distutils.core import setup
from Cython.Build import cythonize
import numpy

# Use python setup.py build_ext --inplace
# to compile
setup(
  name = "cs233cython",
  ext_modules = cythonize('*.pyx'),
  include_dirs=[numpy.get_include()]
)
