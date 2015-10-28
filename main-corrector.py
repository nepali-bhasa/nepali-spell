from distance import MinEdit, MaxPr, ConfusionMatrix
from generator import *
from benchmark import Benchmark
import re


b = Benchmark()
b.startlog('load')
g = Generator('data/eng/smalldict', 2)
c = ConfusionMatrix('data/eng/mistake')
b.endlog()
b.startlog('correction')

with open('data/eng/mistake-text', 'r') as f:
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
