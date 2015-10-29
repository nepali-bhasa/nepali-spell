# cython: language_level=3
import re
from multiplere import Mreplace, Mmatch

_matches = {
    '.*[a-zA-Z0-9]+.*',
    '[-+]?[०-९]+(\.[०-९]+)?'
}
_validator = Mmatch(_matches)

def valid(mystr):
    return not _validator.match(mystr)


_replacements = {
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
    '-':' - ',
    '—':' — ',
    '–':' – ',
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
     'ई':'इ',
     'ऊ':'उ',
     'श':'स',
     'ष':'स',
     'व':'ब',
     'ी':'ि',
     'ू':'ु'
}
_normalizer = Mreplace(_phonics)

# Normalize word (
def normalize(word):
    return _normalizer.replace(word)
