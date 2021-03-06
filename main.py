from lib import *

# TODO Generate all words from dictionary
# TODO Remove all possible unit length words from dictionary
# TODO Select best between direct and segmented approach (sum of edits*)
# TODO Find all (new-words, misspelled-words) from corpus
# TODO Extend the existing dictionary, Create Confusion Matrix

# TODO Merge (segmentation + correction), recursive

# FIXME too much segments बिवापछि , try correction along with segmentation
# FIXME too few segments, होम
# FIXME verbs राख्छु
# FIXME words not in dictionary

b = Benchmark()
b.startlog('load')
dictfile = 'data/vocabulary-dictionary'
p = ShelvePersist(dictfile)
# p = PicklePersist(dictfile)
g = VocabularyN(dictfile, p, 2)
b.endlog()

def trimlist(lst, l = 5):
    if len(lst) > 5:
        lst = lst[:5] + ['...']
    return lst

def getCorrect(word):
    candidates = g.candidates(word)
    if len(candidates) > 1:
        candidates = [(MinEdit(normalize(word), normalize(x)).value(), x) for x in candidates]
        minedit = min(candidates)[0]
        likely = [word for edit,word in candidates if edit == minedit]
    else:
        likely = [candidates[0]]
        minedit = MinEdit(normalize(word), normalize(candidates[0])).value()
    return(likely, minedit)
    print(word,'|', ' '.join(likely), minedit)


b.startlog('correction')
# with open('data/vocabulary-corpus', 'r') as f:
# with open('data/test/sampletext', 'r') as f:
# with open('data/test/corpus', 'r') as f:
# with open('data/test/dictionary', 'r') as f:
with open('data/test/segment', 'r') as f:
    content = f.read()
    words = tokenize(content)

for word in words:

    print(word)
    if not valid(word):
        continue

    # Direct Approach
    likely, minedit = getCorrect(word)
    if not isWrong(likely[0]):
        print(word, ':', ', '.join(trimlist(likely)),minedit)

    # Segmented Approach
    if isWrong(likely[0]) or minedit > 0:
        # XXX: minedit > 0
        # likely[0] is a hack, always wrong words have 1 likely element
        seg = segment(word, g)

        if len(seg) > 1:
            sumedit = 0
            for w in seg:
                if isWrong(w):
                    w = unmarkWrong(w)
                    print(' '*6+'#', end='')
                likely, minedit = getCorrect(w)
                sumedit += minedit

                print('\t', w, ':', ', '.join(trimlist(likely)),minedit)
            print('\t+', sumedit)
    print()

b.endlog()
