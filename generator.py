# cython: language_level=3
from collections import defaultdict
import pickle
import shelve
import os

class Generator:
    # Used to distinguish between correct and misspelled words
    # This helps avoid create another dictionary for correct words
    # _suffix is a random string that is unlikely to occur at end of word
    _suffix = '@&%$'

    # Return all the words in edit distance n (only delete)
    def _delete(self, myword, n):
        values = [myword]
        for i in range(n):
            values.extend([word[:x]+word[x+1:] for word in values[:]
                           for x in range(len(word))])
        return set(values)

    # Initialize Generator
    def __init__(self, wordfile, distance=2):
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

            # TODO: This consumes a lot of memory, try updating shelve itself
            candidatedb = defaultdict(list)
            for word in dictionarydb:
                # Interleave correct word and misspelled words in
                # candidate word dictionary
                candidatedb[word+self._suffix] = True
                for error in self._delete(word, self._distance):
                    candidatedb[error].append(word)

            # Write the resulting dictionary in shelve for persistance
            self._candidatedb = shelve.open(self._candidatefile, flag='c',
                                            protocol=pickle.HIGHEST_PROTOCOL)
            for (x, y) in candidatedb.items():
                self._candidatedb[x] = y
            self._candidatedb.close()

        print("Loading Candidatefile.")
        # Load the dictionary from shelve
        self._candidatedb = shelve.open(self._candidatefile, flag='r',
                                        protocol=pickle.HIGHEST_PROTOCOL)

    def candidates(self, word):
        delete = self._delete
        candidatedb = self._candidatedb
        distance = self._distance
        candidates = {}
        # If word is correct word, don't generate candidates
        if word+self._suffix not in candidatedb:
            # Else return candidate words such that their misspelling are near
            candidates = {x for error in delete(word, distance) if error in candidatedb
                    for x in candidatedb[error]}
        # if there are no candidates, then return the word itself
        return list(candidates) or [word]
