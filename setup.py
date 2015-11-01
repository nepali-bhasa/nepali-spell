from distutils.core import setup
from Cython.Build import cythonize

lib = ["lib/*.py"]

setup(
  name = 'spellchecker',
  ext_modules = cythonize(lib),
)
