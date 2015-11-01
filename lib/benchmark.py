# cython: language_level=3
from time import time
from datetime import timedelta

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def _cout(string, typ=FAIL):
    print(typ+string+ENDC)

class Benchmark:
    def __init__(self):
        self.desc = 'program'
        self.start = time()

    def startlog(self, desc=''):
        if desc:
            self.desc = desc
        self.start = time()
        self.log('Start '+self.desc)

    def endlog(self):
        end = time()
        elapsed = end-self.start
        self.log('End '+self.desc, elapsed)

    def log(self, s, elapsed=None):
        _cout(s, OKGREEN)
        if elapsed:
            _cout("Elapsed time: " + str(elapsed))
