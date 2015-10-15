from generator import *
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

def cout(string, typ=FAIL):
    print(typ+string+ENDC)

class Benchmark:
    def __init__(self, desc='program'):
        self.desc = desc
        self.start = time()

    def startlog(self):
        self.start = time()
        self.log('Start '+self.desc)

    def endlog(self):
        end = time()
        elapsed = end-self.start
        self.log('End '+self.desc, elapsed)

    def log(self, s, elapsed=None):
        cout(s, OKGREEN)
        if elapsed:
            cout("Elapsed time: " + str(elapsed))

b = Benchmark('candidate selection')
g = Generator('data/smalldict', 2)
b.startlog()
print(g.candidates('porridge'))
b.endlog()
