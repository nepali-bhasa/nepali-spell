import re
from helper import Mreplace, Mmatch

_matches = {
    '.*[a-zA-Z0-9]+.*',
    '[-+]?[०-९]+(\.[०-९]+)?'
}
matcher = Mmatch(_matches)

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
replacer = Mreplace(_replacements)

def tokenize(mystr):
    return replacer.replace(mystr).split()

def valid(mystr):
    return not matcher.match(mystr)
