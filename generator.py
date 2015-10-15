# cython: language_level=3
from collections import defaultdict
import pickle
import shelve
import os

class Generator:
    def _delete(self, myword, n):
        values = [myword]
        for i in range(n):
            values.extend([word[:x]+word[x+1:] for word in values[:]
                       for x in range(len(word))])
        return set(values)

    def __init__(self, wordfile='data/smalldict', distance=2):
        self._distance = distance
        self._wordfile = wordfile
        self._candidatefile = wordfile+'.candidate'
        self._initcandidatefile()

    def _initcandidatefile(self):
        if not os.path.isfile(self._candidatefile):
            print("Generating Candidatefile.")

            # NOTE: This should be after if
            with open(self._wordfile, 'r') as db:
                dictionarydb = {x.strip() for x in db.readlines()}

            candidatedb = defaultdict(list)
            for word in dictionarydb:
                for error in self._delete(word, self._distance):
                    candidatedb[error].append(word)

            self._candidatedb = shelve.open(self._candidatefile)
            for (x, y) in candidatedb.items():
                self._candidatedb[x] = y
            self._candidatedb.sync()
        else:
            print("Loading Candidatefile.")
            self._candidatedb = shelve.open(self._candidatefile)

        print("Done")

    def candidates(self, word):
        delete = self._delete
        candidatedb = self._candidatedb
        distance = self._distance
        return {x for error in delete(word, distance) if error in candidatedb
                for x in candidatedb[error]}
