from lib import *

diction = VocabularyN('data/nep/vocabularyD', 2)

with open('data/nep/sample-segmentation', 'r') as f:
    test = f.read().split()
# test = ['गोरेहरूले']

for word in test:
    word = word.strip()
    s = segment(word, diction)
    print(' '.join(s))
