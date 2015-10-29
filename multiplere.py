# cython: language_level=3
import re

class Mreplace:
    def __init__(self, mydict):
        self._mydict = mydict
        self._rx = re.compile('|'.join(map(re.escape, self._mydict)))

    def replace(self, text):
        return self._rx.sub(lambda x: self._mydict[x.group(0)], text)

class Mmatch:
    def __init__(self, mylist):
        self._rx = re.compile('|'.join(mylist))

    def match(self, text):
        return self._rx.match(text)
