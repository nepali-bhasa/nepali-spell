import os
import pickle
import re
import math
from abc import ABCMeta, abstractmethod
from collections import defaultdict

class EditDistance(metaclass=ABCMeta):
    '''A class to return non-word spelling errors.
    '''

    # Selction function: max or min
    @abstractmethod
    def _select(self, lst):
        pass

    # Cost function: const or var
    @abstractmethod
    def _cost(self, x):
        pass

    # Constructor
    def __init__(self, x, y):
        self.x, self.y = x.lower(), y.lower()
        self._lx, self._ly = len(x), len(y)
        # MinEdit matrix which holds edit MinEdit for each point
        self._d = []
        # Populate the MinEdit matrix
        self._populate()

    # Populate the difference matrix
    def _populate(self):
        x, y = "^"+self.x, "^"+self.y
        # Create a difference matrix of size _lx * _ly
        self._d = [[0 for y in range(self._ly+1)] for x in range(self._lx+1)]
        # Initialize difference matrix for deletions and insertions
        # at the starting position of the string
        self._d[0][0] = 0
        for i in range(1, self._lx+1):
            self._d[i][0] = (self._d[i-1][0] +
                             self._cost((x[i-1]+x[i], x[i-1])))
        for j in range(1, self._ly+1):
            self._d[0][j] = (self._d[0][j-1] +
                             self._cost((y[j-1], y[j-1]+y[j])))
        # Iterate over every combination
        for j in range(1, self._ly+1):
            for i in range(1, self._lx+1):
                choice = []
                # Substitution or No action
                choice.append(
                    self._d[i-1][j-1] +
                    (self._cost((x[i], y[j]))
                     if x[i] != y[j] else 0)
                )
                # Deletion
                choice.append(
                    self._d[i-1][j] +
                    self._cost((x[i-1]+x[i], x[i-1]))
                )
                # Insertion
                choice.append(
                    self._d[i][j-1] +
                    self._cost((y[j-1], y[j-1]+y[j]))
                )
                # Transposition
                if (i > 1 and j > 1 and x[i] == y[j-1] and x[i-1] == y[j] and
                        x[i] != y[j]):
                    choice.append(
                        self._d[i-2][j-2] +
                        self._cost((x[i-1]+x[i], x[i]+x[i-1]))
                    )
                # Selection of least costly candidate
                self._d[i][j] = self._select(choice)

    def difference(self):
        '''Returns the edits required in first string to get to second
        string with minimum cost.'''
        # lst contains actions performed in form 'action before after'
        lst = []
        x, y = "^"+self.x, "^"+self.y
        i, j = self._lx, self._ly
        while i != 0 or j != 0:
            choice = []
            # Substitution or No action
            if i > 0 and j > 0:
                choice.append((
                    self._d[i-1][j-1], i-1, j-1,
                    (x[i], y[j]) if x[i] != y[j] else None
                ))
            # Deletion
            if i > 0:
                choice.append((
                    self._d[i-1][j], i-1, j,
                    (x[i-1]+x[i], x[i-1])
                ))
            # Insertion
            if j > 0:
                choice.append((
                    self._d[i][j-1], i, j-1,
                    (y[j-1], y[j-1]+y[j])
                ))
            # Transposition
            if (i > 1 and j > 1 and x[i] == y[j-1] and x[i-1] == y[j] and
                    x[i] != x[i-1]):
                choice.append((
                    self._d[i-2][j-2], i-2, j-2,
                    (x[i-1]+x[i], x[i]+x[i-1])
                ))
            # Select tuple with max cost, also update i and j
            cost, i, j, action = self._select(choice)
            # Adding new actions at the beginning of list
            # because we are iterating from the end of string
            if action:
                lst.insert(0, action)
        return lst

    # Display the difference matrix
    def _display(self):
        # Only a styling function specific for floats
        def _style(value):
            return ("{:<10.4}".format(value)
                    if isinstance(value, float) else "{:<10}".format(value))

        x, y = "^"+self.x.upper(), "^"+self.y.upper()
        for j in range(len(y)-1, -1, -1):
            print(_style(y[j]), end='')
            for i in range(len(x)):
                print(_style(self._d[i][j]), end='')
            print()
        print(_style('#'), end='')
        for i in x:
            print(_style(i), end='')
        print()

    # Validate the inputs
    def _validate(self, m, n):
        if not m or m > self._lx:
            m = self._lx
        if not n or n > self._ly:
            n = self._ly
        return (m, n)


class MinEdit(EditDistance):
    # Selction function: max or min
    def _select(self, lst):
        return min(lst)

    # Cost function: const or var
    def _cost(self, x):
        return 1

    # edit distance of _lx[:m] and _ly[:n]
    def value(self, m=None, n=None, normalized=False):
        '''Return the MinEdit value between the strings x and y upto m and n
        characters, post-normalized.
        '''
        m, n = self._validate(m, n)
        if normalized:
            return 1-self._d[m][n]/max(m, n)
        else:
            return self._d[m][n]



class ConfusionMatrix:

    def __init__(self, fname):
        self._error_words_fname = fname
        self._chars_count_fname = fname + '.ccount'
        self._chars_total_fname = fname + '.ctotal'

        # Count of correct char(s), Count of correct char(s) as
        # incorrect char(s), Count of total correct char(s)
        self.pxy = {}
        self.px = {}
        self.total = 0

        if (not os.path.isfile(self._chars_count_fname)
                or not os.path.isfile(self._chars_total_fname)):
            print("Generating ConfusionMatrix.")
            self.pxy, self.px = self._generate()
        else:
            print("Loading ConfusionMatrix.")
            self.pxy, self.px = self._load()
        self.total = sum(self.pxy.values())

    def _load(self):
        with open(self._chars_count_fname, 'rb') as f:
            chars_count = pickle.load(f)
        with open(self._chars_total_fname, 'rb') as f:
            chars_total = pickle.load(f)
        return chars_count, chars_total

    def _generate(self):
        # Create directory if it doesn't exist
        chars_count = defaultdict(int)
        words_count = defaultdict(int)
        # Get all lines
        with open(self._error_words_fname, 'r') as f:
            lines = [line.strip().lower() for line in f.readlines()]

        for line in lines:
            correct, incorrects = [part.strip() for part in line.split('|')]
            for incorrect in incorrects.split(','):
                pair = [part.strip() for part in incorrect.split('*')]
                word, value = pair[0], int(pair[1]) if len(pair) > 1 else 1
                # Get values for words with edit distance 1
                edit = MinEdit(correct, word)
                if edit.value() > 1:
                    continue
                # Get mistake actions and their count
                for diff in edit.difference():
                    # TODO split correct here
                    chars_count[diff] += value
                # Get one edit distance mistakes and their count
                words_count[correct] += value

        # Get total count of chars in correct words in _error_words file.
        chars_total = defaultdict(int)
        for key in chars_count.keys():
            correct = key[0]
            for word, val in words_count.items():
                chars_total[correct] += len(re.findall(correct, word))*val

        # Write to files
        with open(self._chars_count_fname, 'wb') as f:
            pickle.dump(chars_count, f)
        with open(self._chars_total_fname, 'wb') as f:
            pickle.dump(chars_total, f)

        # Return tuple value
        return chars_count, chars_total


class MaxPr(EditDistance):
    '''A class to return non-word spelling errors using
    weighted MaxPr distance.
    '''

    # NOTE: pxy(x, y) != pxy(y, x) so in MaxPr(x, y)
    # x, y should be correct and incorrect word respectively.
    def __init__(self, x, y, confusion_mat):
        self.confusion = confusion_mat
        super(MaxPr, self).__init__(x, y)

    def _select(self, lst):
        return max(lst)

    def _cost(self, x):
        return 0.90*math.log10(self.confusion.pxy.get(x, 1) /
                          self.confusion.px.get(x[0],
                                                self.confusion.total))

    def value(self, m=None, n=None, log=False):
        '''Return the MaxPr value between the strings x and y upto m and n
        characters.
        '''
        m, n = self._validate(m, n)
        if log:
            return self._d[m][n]
        return math.pow(10, self._d[m][n])
