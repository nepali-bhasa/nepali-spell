from distutils.core import setup
from Cython.Build import cythonize

lib = ["generator.py"]

setup(
  name = 'spellchecker',
  ext_modules = cythonize(lib),
)
