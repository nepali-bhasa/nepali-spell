from distance import MinEdit, MaxPr, ConfusionMatrix
from generator import GeneratorE
from benchmark import Benchmark
import re


b = Benchmark()
b.startlog('load')
g = GeneratorE('data/eng/vocabulary', 2)
c = ConfusionMatrix('data/eng/mistake')
b.endlog()

b.startlog('correction')
with open('data/eng/sampletext', 'r') as f:
    lines = [re.sub('[!.?",\'()]', '', x) for x in f.readlines()]
    words = [y for x in lines for y in x.split()]

for word in words:
    candidates = g.candidates(word)
    if len(candidates) > 1:
        candidates = [(MaxPr(word.lower(), x.lower(), c).value(log=True), x) for x in candidates]
        minedit = max(candidates)[0]
        likely = [word for edit,word in candidates if edit == minedit]
        # TODO choose the one which has least edit distance when not-normalized
        print(word,'|', likely, minedit)
    else:
        print(word,'|' ,candidates[0], 'inf')
b.endlog()
