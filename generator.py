# cython: language_level=3
import os
import pickle
from collections import defaultdict

class Generator:
    def __init__(self, wordfile='data/smalldict', distance=2):
        self._distance = distance
        self._wordfile = wordfile
        self._candidatefile = wordfile+'.candidate'
        self._dictionaryfile = wordfile+'.dict'

        #FIXME: dictionarydb may not be required
        self._dictionarydb = set()
        self._initdictionaryfile()
        self._candidatedb = defaultdict(list)
        self._initcandidatefile()

    def _initdictionaryfile(self):
        if not os.path.isfile(self._dictionaryfile):
            print("Generating Dictionaryfile.")
            with open(self._wordfile, 'r') as db:
                self._dictionarydb = {x.strip() for x in db.readlines()}
            with open(self._dictionaryfile, 'wb') as db:
                pickle.dump(self._dictionarydb, db)
        else:
            print("Loading Dictionaryfile.")
            with open(self._dictionaryfile, 'rb') as db:
                self._dictionarydb = pickle.load(db)
        print("Done")

    def _initcandidatefile(self):
        if not os.path.isfile(self._candidatefile):
            print("Generating Candidatefile.")
            for word in self._dictionarydb:
                for error in self._delete(word, self._distance):
                    self._candidatedb[error].append(word)
            with open(self._candidatefile, 'wb') as db:
                pickle.dump(self._candidatedb, db)
        else:
            print("Loading Candidatefile.")
            with open(self._candidatefile, 'rb') as db:
                self._candidatedb = pickle.load(db)
        print("Done")

    def _delete(self, myword, n):
        values = [myword]
        for i in range(n):
            values.extend([word[:x]+word[x+1:] for word in values[:]
                       for x in range(len(word))])
        return set(values)

    def candidates(self, word):
        delete = self._delete
        candidatedb = self._candidatedb
        distance = self._distance
        return [x for error in delete(word, distance) for x in
                candidatedb[error] if error in candidatedb]
