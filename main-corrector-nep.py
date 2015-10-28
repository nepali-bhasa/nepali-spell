import tokenizer
from distance import MinEdit
from generator import *
from benchmark import Benchmark
import re


b = Benchmark()
b.startlog('load')
g = Generator('data/nep/smalldict', 2)
b.endlog()
b.startlog('correction')

with open('data/nep/mistake-text', 'r') as f:
    content = f.read()
    words = tokenizer.tokenize(content)

for word in words:
    if not tokenizer.valid(word):
        print(word)
        continue
    candidates = g.candidates(word)
    if len(candidates) > 1:
        candidates = [(MinEdit(normalize(word), normalize(x)).value(), x) for x in candidates]
        minedit = min(candidates)[0]
        likely = [word for edit,word in candidates if edit == minedit]
        # TODO choose the one which has least edit distance when not-normalized
        print(word,'|', likely, minedit)
    else:
        print(word,'|' ,candidates[0], 0)
b.endlog()
