# cython: language_level=3
from abc import ABCMeta, abstractmethod
from collections import defaultdict
import pickle
import shelve
import os
from lib.misc import normalize

# Dictionary of arbitrary string that is unlikely to occur at end of word,
# used to distinguish type of key (correct, misspelled, prefix, suffix)
# This helps avoid create another dictionary for correct words
_suffix = {
    'correct' : '?c', # correct_word : list of correct words
    # 'incorrect' : '', # incorrect_word : list of candidate words
    # 'prefix': '?p',
    # 'suffix': '?s',
}

class Vocabulary(metaclass=ABCMeta):
    # Return all the words in edit distance n (only delete)
    def _delete(self, myword, n):
        values = [myword]
        for i in range(n):
            values.extend([word[:x]+word[x+1:] for word in values[:]
                           for x in range(len(word))])
        return set(values)

    # Initialize Vocabulary
    def __init__(self, wordfile, distance=2):
        self._distance = distance
        self._wordfile = wordfile
        self._vocabulary_file = wordfile+'.shelve'
        self._init_vocabulary_file()

    def _init_vocabulary_file(self):
        if not os.path.isfile(self._vocabulary_file):
            print("Generating vocabulary_file.")
            with open(self._wordfile, 'r') as db:
                dictionarydb = {x.strip() for x in db.readlines()}
            # Optionally read for '+' file
            if os.path.isfile(self._wordfile+'+'):
                with open(self._wordfile+'+', 'r') as db:
                    dictionarydb |= {x.strip() for x in db.readlines()}

            # TODO: This consumes a lot of memory, try updating shelve itself
            candidatedb = defaultdict(list)
            for word in dictionarydb:
                nword = self._normalize(word)
                # Interleave correct word and misspelled words in
                # candidate word dictionary
                if word not in candidatedb[nword+_suffix['correct']]:
                    candidatedb[nword+_suffix['correct']].append(word)
                # NOTE: Don't add the correct word (nword) as it is already added
                for error in self._delete(nword, self._distance)-{nword}:
                    candidatedb[error].append(word)

            # Write the resulting dictionary in shelve for persistance
            self._candidatedb = shelve.open(self._vocabulary_file, flag='c',
                                            protocol=pickle.HIGHEST_PROTOCOL)
            for (x, y) in candidatedb.items():
                # if _suffix['correct'] in x and len(y) > 1:
                #     print(x, y)
                self._candidatedb[x] = y
            self._candidatedb.close()

        print("Loading vocabulary_file.")
        # Load the dictionary from shelve
        self._candidatedb = shelve.open(self._vocabulary_file, flag='r',
                                        protocol=pickle.HIGHEST_PROTOCOL)

    # For 'in'
    def __contains__(self, word):
        # return word+_suffix['correct'] in self._candidatedb
        # return self._normalize(word)+_suffix['correct'] in self._candidatedb

        # First find key then find word in list of candidates
        # NOTE: list will be okay because there are few candidates
        key = self._normalize(word)+_suffix['correct']
        if key in self._candidatedb:
            if word in self._candidatedb[key]:
                return True
        return False

    def candidates(self, word):
        nword = self._normalize(word)
        delete = self._delete
        candidatedb = self._candidatedb
        distance = self._distance
        candidates = {}
        # If word is correct word, don't generate candidates
        # else return candidate words such that their misspelling are near
        if not nword+_suffix['correct'] in self._candidatedb:
            candidates = {x for error in delete(nword, distance) if error in candidatedb
                    for x in candidatedb[error]}
        else:
            candidates = self._candidatedb[nword+_suffix['correct']]
        # if there are no candidates, then return the word itself
        return list(candidates) or [word]

    # TODO handle adding of new words in vocabulary
    def add(self, word):
        pass

    @abstractmethod
    def _normalize(self, word):
        pass

class VocabularyE(Vocabulary):
    def _normalize(self, word):
        return word.lower()

class VocabularyN(Vocabulary):
    def _normalize(self, word):
        return normalize(word)
