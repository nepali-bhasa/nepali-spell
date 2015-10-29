import ntokenizer
from distance import MinEdit
from generator import GeneratorN
from benchmark import Benchmark
import re


b = Benchmark()
b.startlog('load')
g = GeneratorN('data/nep/vocabulary', 2)
b.endlog()

b.startlog('correction')
with open('data/nep/sampletext', 'r') as f:
    content = f.read()
    words = ntokenizer.tokenize(content)

for word in words:
    if not ntokenizer.valid(word):
        print(word)
        continue
    candidates = g.candidates(word)
    if len(candidates) > 1:
        candidates = [(MinEdit(ntokenizer.normalize(word), ntokenizer.normalize(x)).value(), x) for x in candidates]
        minedit = min(candidates)[0]
        likely = [word for edit,word in candidates if edit == minedit]
        # TODO choose the one which has least edit distance when not-normalized
        print(word,'|', likely, minedit)
    else:
        print(word,'|' ,candidates[0], 0)
b.endlog()
