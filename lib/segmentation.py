# cython: language_level=3

def _magnitude(x, y):
    return len(x)**2 + len(y)**2

def isWrong(word):
    return word[-1] == '*'

def markWrong(word):
    return (word+'*') if word else ''

def unmarkWrong(word):
    return word[:-1]

def segment(word, dictionary):
    if not word:
        return []
    if word in dictionary:
        return [word]

    #lw: length of word
    lw = len(word)
    # of: offset front, ob: offset back
    # Requires 'of' and 'ob' because traversal may not be symmetric
    of = 0
    ob = lw-1

    # TODO Put cutoff, get from dictionary model (+2 of longest word)

    # Lookup in dictionary is expensive if it is loaded from disk,
    # so, when back='' or front='' it won't change until an offset
    # thats why no need to recalculate it in next iteration
    # 'xxx' because it needs to run for the first time and after offset change
    lastback = 'xxx'
    lastfront = 'xxx'
    while True:
        # 'front' is longest word from front in text
        # which is also in dictionary
        front = ''
        if lastfront:
            i = 0
            while i < lw:
                # Fix traversal
                while i+1<lw and word[i+1] in dependent:
                    i += 1
                # Replace older shorter word with longer one if it exits in dict
                if word[of:i+1] in dictionary:
                    front = word[of:i+1]
                # Traversal
                i += 1
            lastfront = front

        # 'back' is longest word from back in text
        # which is also in dictionary
        back = ''
        if lastback:
            j = lw-1
            while j > -1:
                # Fix traversal
                while word[j] in dependent:
                    j -= 1
                # Replace older shorter word with longer one if it exits in dict
                if word[j:ob+1] in dictionary:
                    back = word[j:ob+1]
                # Traversal
                j -= 1
            lastback = back

        # Try using an offset if no match is found from front and back
        if not front and not back:
            # front offset traversal
            of += 1
            while of<lw and word[of] in dependent:
                of += 1
            # back offset traversal
            while ob>-1 and word[ob] in dependent:
                ob -= 1
            ob -= 1
            # If offset exceeds limit then return
            if of > lw or ob < 0:
                return [markWrong(word)]
            # Don't go down
            lastback = 'xxx'
            lastfront = 'xxx'
            continue

        lf = len(front)
        lb = len(back)
        offsetfront = markWrong(word[:of])
        offsetback = markWrong(word[ob+1:])
        output = []

        if lf+lb <= ob-of+1:
            mremain = word[of+lf:ob-lb+1]
            output = [front] + segment(mremain, dictionary) + [back]
        else:
            fremain = word[of:ob-lb+1]
            bremain = word[of+lf:ob+1]
            fremaincorrect = fremain in dictionary
            bremaincorrect = bremain in dictionary

            if fremaincorrect and bremaincorrect:
                # XXX magnitude is arbitrary function
                if _magnitude(front, bremain) < _magnitude(fremain, back):
                    output = [front , bremain]
                else:
                    output = [fremain, back]
            elif fremaincorrect:
                output = [fremain, back]
            elif bremaincorrect:
                output = [front, bremain]
            else:
                if lf >= lb:
                    output = [front] + segment(bremain, dictionary)
                else:
                    output = segment(fremain, dictionary) + [back]

        output = [offsetfront] + output + [offsetback]
        # NOTE: connect() is used in each iteration
        # Used connect here so that smaller groups are connected first
        return connect([x for x in output if x])


def connect(wordlist, joinwhen=3):
    # XXX: joinwhen = 3
    output = []

    for i in range(len(wordlist)):
        # 'stk' is the element at end of list
        stk = output[-1] if output else ''
        # 'eml' is the element to add to list
        eml = wordlist[i]

        if stk and isWrong(stk) and isWrong(eml):
            output[-1] = markWrong(unmarkWrong(stk)+unmarkWrong(eml))
        elif stk and isWrong(stk) and (len(eml) < joinwhen or
                len(unmarkWrong(stk)) < joinwhen):
            output[-1] = markWrong(unmarkWrong(stk)+eml)
        elif stk and isWrong(eml) and (len(stk) < joinwhen or
                len(unmarkWrong(eml)) < joinwhen):
            output[-1] = markWrong(stk+unmarkWrong(eml))
        else:
            output.append(eml)

    return output

dependent = {
            'ँ',
            'ं',
            'ः',
            'ा',
            'ि',
            'ी',
            'ु',
            'ू',
            'ृ',
            'े',
            'ै',
            'ो',
            'ौ',
            '्',
           '‍',
            }
