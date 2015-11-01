from lib import *

b = Benchmark()
b.startlog('load')
g = VocabularyN('data/nep/vocabularyD', 2)
b.endlog()

b.startlog('correction')
with open('data/nep/sampletextD', 'r') as f:
    content = f.read()
    words = tokenize(content)

for word in words:
    if not valid(word):
        print(word)
        continue
    candidates = g.candidates(word)
    if len(candidates) > 1:
        candidates = [(MinEdit(normalize(word), normalize(x)).value(), x) for x in candidates]
        minedit = min(candidates)[0]
        likely = [word for edit,word in candidates if edit == minedit]
        # TODO choose the one which has least edit distance when not-normalized
        print(word,'|', ' '.join(likely), minedit)
    else:
        print(word,'|' ,candidates[0], 0)
b.endlog()
