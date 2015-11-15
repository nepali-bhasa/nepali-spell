# cython: language_level=3
from abc import ABCMeta, abstractmethod
from collections import defaultdict
import pickle
import shelve
import os
from lib.misc import normalize

class PicklePersist():
    def __init__(self, filename):
        self.persistfilename = filename + '.pickle'

    def exists(self):
        return os.path.isfile(self.persistfilename)

    def save(self, candidatedb):
        with open(self.persistfilename, 'wb') as db:
            pickle.dump(candidatedb, db)

    def load(self):
        with open(self.persistfilename, 'rb') as db:
            self.persistfile = pickle.load(db)
            return self.persistfile

class ShelvePersist():
    def __init__(self, filename):
        self.persistfilename = filename + '.shelve'

    def exists(self):
        return os.path.isfile(self.persistfilename)

    def save(self, candidatedb):
        # Write the resulting dictionary in shelve for persistance
        self.persistfile = shelve.open(self.persistfilename, flag='c',
                                        protocol=pickle.HIGHEST_PROTOCOL)
        for (x, y) in candidatedb.items():
            # if _suffix['correct'] in x and len(y) > 1:
            #     print(x, y)
            self.persistfile[x] = y
        self.persistfile.close()

    def load(self):
        # Load the dictionary from shelve
        self.persistfile = shelve.open(self.persistfilename, flag='r',
                                        protocol=pickle.HIGHEST_PROTOCOL)
        return self.persistfile


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
    def __init__(self, wordfile, persistfile, distance=2):
        self._distance = distance
        self._wordfile = wordfile
        self._vocabulary_file = persistfile
        self._init_vocabulary_file()

    def _init_vocabulary_file(self):
        if not self._vocabulary_file.exists():
            print("Generating vocabulary_file.")
            with open(self._wordfile, 'r') as db:
                dictionarydb = {x.strip() for x in db.readlines()}
            # Optionally read for '+' file
            if os.path.isfile(self._wordfile+'+'):
                with open(self._wordfile+'+', 'r') as db:
                    dictionarydb |= {x.strip() for x in db.readlines()}
            # FIXME: This consumes a lot of memory, try updating shelve itself
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

            self._vocabulary_file.save(candidatedb)

        self._candidatedb = self._vocabulary_file.load()

    # For 'in'
    def __contains__(self, word):
        # return word+_suffix['correct'] in self._candidatedb
        return self._normalize(word)+_suffix['correct'] in self._candidatedb

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
        return list(candidates) or [word+'*']

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
