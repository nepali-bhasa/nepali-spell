from distutils.core import setup
from Cython.Build import cythonize

lib = ["generator.py", "benchmark.py", "distance.py",
        "multiplere.py", "ntokenizer.py"]

setup(
  name = 'spellchecker',
  ext_modules = cythonize(lib),
)
