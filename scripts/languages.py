#!/usr/bin/env python3
'''Convert language codes and names, dictionary names and more'''

__author__ = 'Sander van Geloven'
__license__ = 'https://github.com/nuspell/nuspell/blob/master/COPYING.LESSER'

from json import load
from os import path
import sys

def error(verbose):
    '''Error'''
    if verbose:
        print('''ERROR: Provide command and optional argument: command [dict_name|language]
    Supported are:
        langs                       print all languages
        dicts                       print all dict names
        packages                    print all word list packages
        wordlists                   print all word list files
        dict2lang dict_name         converts dict name to language
        dict2package dict_name      converts dict name to word list package
        dict2wordlist dict_name     converts dict name to word list file
        lang2dicts language         converts language to dict names
    Where dict_name can be e.g. en_US and language e.g. Dutch''')
    sys.exit(1)

def lookup(args, verbose=False):
    '''Lookup requested values'''
    if len(args) < 1 or len(args) > 2:
        error(verbose)
    command = args[0]
    argument = None
    if '2' in command:
        if len(args) != 2:
            error(verbose)
        argument = args[1]
    else:
        if len(args) == 2:
            error(verbose)
    file = path.join(path.dirname(path.realpath(__file__)), 'languages.json')
    data = load(open(file))

    # lists all languages
    if command == 'langs':
        if data['languages'].keys():
            return '\n'.join(sorted(data['languages'].keys()))
            # print all dict names
    elif command == 'dicts':
        dicts = set()
        for lang, values in data['languages'].items():
            if 'dicts' not in values:
                continue
            for dikt in values['dicts']:
                dicts.add(dikt)
        if dicts:
            return '\n'.join(sorted(dicts))

    # lists all word list packages
    elif command == 'packages':
        packages = set()
        for lang, values in data['languages'].items():
            if 'package' not in values:
                continue
            packages.add(values['package'])
        if packages:
            return '\n'.join(sorted(packages))

    # lists all word list files
    elif command == 'wordlists':
        wordlists = set()
        for lang, values in data['languages'].items():
            if 'wordlist' not in values:
                continue
            wordlists.add(values['wordlist'])
        if wordlists:
            return '\n'.join(sorted(wordlists))

    # converts dict name to language
    elif command == 'dict2lang':
        for lang, values in data['languages'].items():
            if 'dicts' not in values:
                continue
            for dikt in values['dicts']:
                if dikt == argument:
                    return lang

    # converts dict name to word list package
    elif command == 'dict2package':
        for lang, values in data['languages'].items():
            if 'dicts' not in values:
                continue
            for dikt in values['dicts']:
                if dikt == argument and 'package' in values:
                    return values['package']

    # converts dict name to word list file
    elif command == 'dict2wordlist':
        for lang, values in data['languages'].items():
            if 'dicts' not in values:
                continue
            for dikt in values['dicts']:
                if dikt == argument and 'wordlist' in values:
                    return values['wordlist']

    # converts language to dict names
    elif command == 'lang2dicts':
        for lang, values in data['languages'].items():
            if argument == lang and 'dicts' in values:
                return '\n'.join(sorted(values['dicts']))

    return ''

def main(args):
    '''Main'''
    print(lookup(args, verbose=True))

if __name__ == "__main__":
    main(sys.argv[1:])
