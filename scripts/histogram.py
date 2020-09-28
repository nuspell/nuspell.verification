#!/usr/bin/env python3
'''Generating histogram of TODO'''

__author__ = 'Sander van Geloven'
__license__ = 'https://github.com/nuspell/nuspell/blob/master/COPYING.LESSER'

from datetime import datetime
from operator import itemgetter
import sys
from unicodedata import category, name

def stamp_time():
    '''Get formatted date and time'''
    return datetime.now().strftime('%Y-%m-%d at %H:%M:%S')

categories = {
    'C': 'control',
    'L': 'letter',
    'M': 'mark',
    'N': 'number',
    'P': 'punctuation',
    'S': 'symbol',
    'Z': 'whitespace',
}

def decode_category(value):
    '''Decode abbreviated Unicode category'''
    cat = category(value)
    first = cat[0]
    if first in categories:
        return categories[first]
    print(f'ERROR: Illegal or unsupported abbreviated Unicode category {cat}')
    sys.exit(1)

#bug si_LK has invalid unicode character U+0DFE


def slashes(chars):
    '''Report slash-like characters'''
    result = ''
    if '/' in chars:
        result += '| slash character | / |'
    if '\\' in chars:
        result += '| backslash character | \\ |'
    return result

def hyphens(chars, starts_hyphen):
    '''Report hyphen-like characters'''
    result = ''
    if '-' in chars:
        if starts_hyphen:
            result += '| hyphen character and some lines start with this | - |'
        else:
            result += '| hyphen character | - |'
    if '‑' in chars:
        result += '| non-breaking hyphen character | ‑ |'
    if '­' in chars:
        result += '| soft hyphen character |   |'
    if '_' in chars:
        result += '| underscore character | _ |'
    if '–' in chars:
        result += '| en-dash character | – |'
    if '—' in chars:
        result += '| em-dash character | — |'
    return result

def apostrophes(chars):
    '''Report apostrophe-like characters'''
    result = ''
    if '\'' in chars:
        result += '| apostrophe character | \' |'
    if '`' in chars:
        result += '| grave accent character | ` |'
    if '’' in chars:
        result += '| single right quotation mark character | ’ |'
    return result

def whitespaces(chars):
    '''Report whitespace-like characters'''
    result = ''
    if '\t' in chars:
        result += '| tab character | ↹ |'
    if ' ' in chars:
        result += '| space character | ␣ |'
    if ' ' in chars:
        result += '| figure space character | ␣ |'
    if ' ' in chars:
        result += '| punctuation space character | ␣ |'
    if ' ' in chars:
        result += '| thin space character | ␣ |'
    if '‌' in chars:
        result += '| zero width non-joiner character |   |'
    if '‍' in chars:
        result += '| zero width joiner character |   |'
    if '‏' in chars:
        result += '| narrow no-break space character | ␣ |'
    return result

def puntuations(chars):
    '''Report puntuation characters'''
    result = ''
    if '.' in chars:
        result += '| period character | . |'
    if ',' in chars:
        result += '| comma character | , |'
    if ':' in chars:
        result += '| colon character | : |'
    if ';' in chars:
        result += '| semicolon character | ; |'
    return result

def mathematics(chars):
    '''Report mathematical characters'''
    result = ''
    if '+' in chars:
        result += '| plus character | + |'
    if '&' in chars:
        result += '| ampersand character | & |'
    if '=' in chars:
        result += '| equals character | = |'
    if '(' in chars:
        result += '| bracket opening character | ( |'
    if ')' in chars:
        result += '| bracket closing character | ) |'
    return result

def scripts(chars):
    '''Report superscripts and subscript characters'''
    result = ''
    if '¹' in chars:
        result += '| superscript 1 | ¹ |'
    if '²' in chars:
        result += '| superscript 2 | ² |'
    if '³' in chars:
        result += '| superscript 3 | ³ |'
    if '₁' in chars:
        result += '| subscript 1 | ₁ |'
    if '₂' in chars:
        result += '| subscript 2 | ₂ |'
    if '₃' in chars:
        result += '| subscript 3 | ₃ |'
    if '·' in chars:
        result += '| centered dot | · |'
    return result

def specifics(chars):
    '''Report language-specific characters'''
    result = ''
    if 'ß' in chars:
        result += '| sharp s character | ß |'
    if 'ẞ' in chars:
        result += '| sharp S character, upper case | ẞ |'
    if 'ĳ' in chars:
        result += '| ij character | ĳ |'
    if 'Ĳ' in chars:
        result += '| IJ character, upper case | Ĳ |'
    if 'İ' in chars:
        result += '| dotted I character, upper case | İ |'
    return result

def histogram(args):
    '''TODO histogram'''
    if len(args) != 1:
        print('ERROR: Missing filename')
        sys.exit(1)

    chars = {}
    starts_hyphen = False
    for line in open(args[0]):
        line = line[:-1]
        if len(line) > 0 and line[0] == '-':
            starts_hyphen = True
        for char in line:
            if char in chars:
                chars[char] += 1
            else:
                chars[char] = 1

    path = args[0].split('/')
    result = ''
    result += '# Histogram {}'.format(path[len(path) - 1])
    result += ''
    result += '| special characters ocurring |   |'
    result += '|---|---|'

    # order below is partly optimized by overall frequency in dic files

    result += slashes(chars)
    result += hyphens(chars, starts_hyphen)
    result += apostrophes(chars)
    result += whitespaces(chars)
    result += puntuations(chars)
    result += mathematics(chars)
    result += scripts(chars)
    result += specifics(chars)

    result += ''
    result += '| count | char | code | category | name |'
    result += '|--:|---|--:|---|---|'
    for char, count in sorted(chars.items(), key=itemgetter(1)):
        try:
            if char == '|':
                result += '| {} | <code>&#124;</code> | `{}` | {} | {} |' \
                .format(count, hex(ord(char)), decode_category(char), name(char).lower())
            else:
                result += '| {} | `{}` | `{}` | {} | {} |' \
                .format(count, char, hex(ord(char)), decode_category(char), name(char).lower())
        except ValueError:
            if char == '\t':
                result += '| {} | `{}` | `{}` | {} | character tabulation |' \
                .format(count, char, hex(ord(char)), decode_category(char))
            else:
                result += '| {} | `{}` | `{}` | {} | VALUE ERROR |' \
                .format(count, char, hex(ord(char)), decode_category(char))

    return result

def main(args):
    '''Main'''
    print(histogram(args))

if __name__ == "__main__":
    main(sys.argv[1:])
