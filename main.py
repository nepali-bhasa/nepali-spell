from distance import MinEdit, MaxPr, ConfusionMatrix
from generator import *
from time import time
from datetime import timedelta
import re


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
        cout(s, OKGREEN)
        if elapsed:
            cout("Elapsed time: " + str(elapsed))


b = Benchmark()
b.startlog('load')
g = Generator('data/smalldict', 2)
c = ConfusionMatrix('data/mistake')
b.endlog()
b.startlog('correction')

with open('data/mistake-text', 'r') as f:
    lines = [re.sub('[!.?",\'()]', '', x) for x in f.readlines()]
    words = [y for x in lines for y in x.split()]
# words = ['ou', 'goode', 'pencilz', 'good boy', 'acomodation', 'pomegrant', 'kdsjalfsad']
for word in words:
    candidates = g.candidates(word)
    if len(candidates) > 1:
        candidates = [(MaxPr(word, x, c).value(log=True), x) for x in candidates]
        likely = max(candidates)[1]
        print(word, ' | ', likely)
b.endlog()
