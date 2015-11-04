# cython: language_level=3
import re

class Mreplace:
    def __init__(self, mydict):
        self._mydict = mydict
        self._rx = re.compile('|'.join(map(re.escape, self._mydict)))

    def replace(self, text):
        return self._rx.sub(lambda x: self._mydict[x.group(0)], text)

class Mmatch:
    def __init__(self, mylist):
        self._rx = re.compile('|'.join(mylist))

    def match(self, text):
        return self._rx.match(text)



_matches = {
    '.*[?{}(),/\\"\';+=_*&^$#@!~`|\[\]]+.*',
    '.*[a-zA-Z0-9]+.*',
    '[-+]?[०-९]+(\.[०-९]+)?'
}
_validator = Mmatch(_matches)

def valid(mystr):
    return not _validator.match(mystr)


_replacements = {
    '﻿':'',

    '-':'-',
    '—':'-',
    '–':'-',

    ' :':' : ',
    '।':' । ',
    '’':' " ',
    '‘':' " ',
    '“':' " ',
    '”':' " ',
    '"':' " ',
    "'":' " ',
    '?':' ? ',
    '!':' ! ',
    ',':' , ',
    '/':' / ',
    '÷':' ÷ ',
    '…':' … ',
    '{':' { ',
    '}':' } ',
    '[':' [ ',
    ']':' ] ',
    '(':' ( ',
    ')':' ) ',
    '=': ' = ',
    '***': ' ',
    '**':' ',
    '*':' ',
    '~': ' ',
    '`': ' ',
    '#': ' ',
    '...': ' ... ',
    '..': ' ... ',
    '.': ' . '
}
_tokenizer = Mreplace(_replacements)

def tokenize(mystr):
    return _tokenizer.replace(mystr).split()


# Dictionary of characters that have similar phonics, normalized words
# will have zero edit distance if they differ in only _phonics
_phonics = {
     'ा':'आ',
     'ो':'ओ',

     'ी':'इ',
     'ि':'इ',
     'ई':'इ',

     'ू':'उ',
     'ु':'उ',
     'ऊ':'उ',

     'े':'ए',

     '्':'',

     'श':'स',
     'ष':'स',
     'व':'ब',

     '‍':'', # Contains a non-joiner
}
_normalizer = Mreplace(_phonics)

# Normalize word (
def normalize(word):
    return _normalizer.replace(word)


# TODO use regex to match
# 'ं'
# fix tokenizer and valid such that tokenizer will split all the
# non-valid words
