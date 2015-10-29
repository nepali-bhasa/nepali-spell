import os
import ntokenizer
from collections import defaultdict

cand = defaultdict(int)
path = 'data/nep/corpus'
for filename in os.listdir(path):
    if ".corpus" not in filename:
       continue
    with open(path+'/'+filename, 'r') as f:
        # Tokenization
        content = f.read()
        for key in ntokenizer.tokenize(content):
            if ntokenizer.valid(key):
                cand[key] += 1

with open('data/nep/vocabulary', 'w') as f:
    for (key, val) in sorted(cand.items(), key=lambda x: (x[1], x[0])):
        if val > 30:
            f.write(key+'\n')
