import os
from collections import defaultdict
from misc import tokenize, valid

cand = defaultdict(int)
path = 'tmp/corpus'
for filename in os.listdir(path):
    if ".corpus" not in filename:
       continue
    with open(path+'/'+filename, 'r') as f:
        # Tokenization
        content = f.read()
        for key in tokenize(content):
            if valid(key):
                cand[key] += 1

with open('data/nep/vocabularyC', 'w') as f:
    for (key, val) in sorted(cand.items(), key=lambda x: (x[1], x[0])):
        if val > 30:
            f.write(key+'\n')
