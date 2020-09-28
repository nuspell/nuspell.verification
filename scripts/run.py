#!/usr/bin/env python3
'''Preparing, testing and reporting of dictionaries on word lists'''

__author__ = 'Sander van Geloven'
__license__ = 'https://github.com/nuspell/nuspell/blob/master/COPYING.LESSER'

from operator import itemgetter
from os import chdir, listdir, mkdir, path, remove, replace, walk, getcwd
import re
from shutil import copyfile, rmtree
from subprocess import Popen, PIPE
import sys
from zipfile import ZipFile, ZIP_DEFLATED

from magic import from_file

from languages import lookup

def error():
    '''Error'''
    print('''ERROR: Provide only one of the following optional arguments
    Supported are:
        download        download debian package and other resources
        extract         extract packages and convert files
        compress        compress files for storage in repository
        uncompress      uncompresses files for running verification test
        verify          run verification test on available dictionaries
        report          aggregate verification results in MarkDown
    No argument results in execution of uncompress, verify and report.''')
    sys.exit(1)

def conv(infilename, inencoding, outfilename, outencoding='utf-8', pat=None, rep=''):
    '''Convert file from one encoding to another encoding'''
    if infilename == outfilename:
        print('ERROR: Input and output file may not be the same.')
        return -1
    # See https://docs.python.org/3/library/codecs.html?#standard-encodings
    lines = 0
    with open(infilename, mode='r', encoding=inencoding) as infile, \
         open(outfilename, mode='w', encoding=outencoding) as outfile:
        if pat:
            for line in infile:
                line = pat.sub(rep, line)
                if infilename.endswith('an_ES.dic') \
                    and line.startswith('no/ '):
                    #LATER would not fit in regex and line `no` already exists
                    continue
                if infilename.endswith('lv_LV.dic') \
                    and line.startswith('Nagīni/'):
                    #LATER would not fit in regex
                    line = line.replace('Nagīni/', 'Nagīni')
                if line != '\n': #LATER also support \r\n? was not needed now
                    outfile.write(line)
                    lines += 1
        else:
            for line in infile:
                outfile.write(line)
                lines += 1
    return lines

def dos2unix(infilename, outfilename):
    '''Convert DOS file with CRLF linefeeds to Unix with LF linefeeds'''
    if infilename == outfilename:
        print('ERROR: Input and output file may not be the same.')
        return -1
    lines = 0
    with open(infilename, 'br') as infile, \
         open(outfilename, 'bw') as outfile:
        for line in infile:
            outfile.write(line.replace(b'\r\n', b'\n'))
            lines += 1
    return lines

def execute(command, fatal=False):
    '''Execute a command by the operating system'''
    out = None
    err = None
    pipes = None
    try:
        pipes = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = pipes.communicate()
    except FileNotFoundError:
        if fatal:
            print(f'ERROR: Could not execute unavailable command {command}')
            sys.exit(1)
        else:
            print('WARNING: Skipping execution of unavailable command' \
                  f' {command}')
    if pipes.returncode != 0:
        if fatal:
            print('ERROR: Could not execute unavailable command' \
                  f' {command}, return code={pipes.returncode},' \
                  f' error={err.strip()}')
            sys.exit(1)
        else:
            print('WARNING: Skipping execution of unavailable command' \
                  f' {command}, return code={pipes.returncode},' \
                  f' error={err.strip()}')
    return out.decode('utf-8'), err.decode('utf-8')

def mk_or_clear_dir_and_cd(top):
    '''Make or clear directory and change into it'''
    if not path.isdir(top):
        mkdir(top)
    chdir(top)
    for file in listdir():
        try:
            rmtree(file)
        except NotADirectoryError:
            remove(file)

def compress_archive(basename):
    '''Compress directory'''
    # Remove existing compressed files
    if path.isfile(f'{basename}.zip'):
        remove(f'{basename}.zip')
    print(f'  {basename}')
    zip_ref = ZipFile(f'{basename}.zip', 'w', ZIP_DEFLATED)
    for root, dirs, files in walk(basename):
        for file in files:
            zip_ref.write(path.join(root, file))
    zip_ref.close()

def uncompress_archive(basename):
    '''Uncompress file if target directory does not exists'''

    if path.isdir(f'{basename}'):
        print(f'WARNING: Directory {basename} already exists, skipping')
        return
    print(f'  {basename}.zip')
    with ZipFile(f'{basename}.zip') as zip_ref:
        zip_ref.extractall('.')

def download_dict():
    '''Download dict packages'''
    print('INFO: Download dict packages')
    org = getcwd()

    # Get alternative downloads
    filename = 'dict-package-urls'
    alt_urls = []
    alt_names = []
    if path.isfile(filename):
        file = open(filename)
        for line in file:
            line = line.strip()
            alt_urls.append(line)
            alt_names.append(line[line.rfind('/')+1:line.find('_')])

    # Get dict package names to skip
    skip_names = []
    filename = 'dict-package-skip'
    if path.isfile(filename):
        file = open(filename)
        for name in file:
            if '#' not in name:
                skip_names.append(name.strip())

    # Get dict package names from apt-get
    output = execute(["apt-cache", "search", "'myspell|hunspell|nuspell'"])[0]
    packages = sorted(list(filter(None, output.split('\n'))))
    names = []
    for package in packages:
        if 'transitional' in package.lower() or 'dummy' in package.lower():
            continue
        name = package.split(' ')[0]
        if (name.startswith('myspell-') \
            or name.startswith('hunspell-') \
            or name.startswith('nuspell-')) \
           and not name.endswith('-tools') \
           and name not in skip_names:
#            code = name[name.index('-') + 1:]
            names.append(name)
    names = sorted(names)

    # Compare with previous run and write names to file
    filename = 'dict-package-names'
    if path.isfile(filename):
        file = open(filename)
        prev_names = []
        for name in file:
            prev_names.append(name.strip())
        prev_names = sorted(prev_names)
        added = False
        for name in names:
            if name not in prev_names:
                added = True
                print(f'WARNING: Dictionary package name {name} has been added')
        removed = False
        for name in prev_names:
            if name not in names:
                removed = True
                print(f'ERROR: Dictionary package name {name} has been removed')
        if removed:
            sys.exit(1)
        if added:
            file = open(filename, 'w')
            for name in names:
                file.write(f'{name}\n')
    else:
        file = open(filename, 'w')
        for name in names:
            file.write(f'{name}\n')

    # Prepare download directory
    dest = path.join('..', 'packages-dict')
    mk_or_clear_dir_and_cd(dest)

    # Download packages
    for alt_name in alt_names:
        if alt_name in names:
            names.remove(alt_name)
    execute(["apt-get", "download"] + names)
    for alt_url in alt_urls:
        if alt_url.strip()[0] != '#':
            execute(["wget", "--quiet", alt_url])

    # Return to original path
    chdir(org)

def download_list():
    '''Download word list packages'''
    print('INFO: Download word list packages')
    org = getcwd()

    # Get alternative downloads
    filename = 'list-package-urls'
    alt_urls = []
    alt_names = []
    if path.isfile(filename):
        file = open(filename)
        for line in file:
            line = line.strip()
            alt_urls.append(line)
            alt_names.append(line[line.rfind('/')+1:line.find('_')])

    # Get word list package names from languages.py and apt-get
    names = []
    package_names = lookup(['packages']).split('\n')
    for package_name in package_names:
        output = execute(["apt-cache", "search", package_name])[0]
        packages = sorted(list(filter(None, output.split('\n'))))
        for package in packages:
            if package.split(' ')[0] == package_name:
                names.append(package_name)
    names = sorted(names)

    # Compare with previous run and write names to file
    filename = 'list-package-names'
    if path.isfile(filename):
        file = open(filename)
        prev_names = []
        for name in file:
            prev_names.append(name.strip())
        prev_names = sorted(prev_names)
        added = False
        for name in names:
            if name not in prev_names:
                added = True
                print(f'WARNING: word list package name {name} has been added')
        removed = False
        for name in prev_names:
            if name not in names:
                removed = True
                print(f'ERROR: Word list package name {name} has been removed')
        if removed:
            sys.exit(1)
        if added:
            file = open(filename, 'w')
            for name in names:
                file.write(f'{name}\n')
    else:
        file = open(filename, 'w')
        for name in names:
            file.write(f'{name}\n')

    # Prepare download directory
    dest = path.join('..', 'packages-list')
    mk_or_clear_dir_and_cd(dest)

    # Download packages
    for alt_name in alt_names:
        if alt_name in names:
            names.remove(alt_name)

    execute(["apt-get", "download"] + names)
    for alt_url in alt_urls:
        if alt_url.strip()[0] != '#':
            execute(["wget", "--quiet", alt_url])

    # Return to original path
    chdir(org)

def extract_dict():
    '''Extract and convert dict packages'''
    print('INFO: Extract dict packages')
    org = getcwd()

    # Prepare extract directory and empty it
    tmp_dest = path.join('..', 'files-dict')
    mk_or_clear_dir_and_cd(tmp_dest)

    # Prepare word directory and empty it
    word_dest = path.join('..', 'word')
    mk_or_clear_dir_and_cd(word_dest)

    # Prepare convert directory and empty it
    dest = path.join('..', 'dict')
    mk_or_clear_dir_and_cd(dest)

    src = path.join('..', 'packages-dict')
    dict_report = []
    list_report = []
    dict_report.append('Overview of word lists')
    list_report.append('Overview of dictionaries')
    chdir(src)
    for package in sorted(listdir()):
        name = package[:package.find('_all.deb')] # expected file name ending
        print(f'  {name}')
        tmp_dest_dir = path.join(tmp_dest, name)
        mkdir(tmp_dest_dir)
        execute(["dpkg", "-x", package, tmp_dest_dir])

        dest_dir = path.join(dest, name)
        mkdir(dest_dir)
        tmp_dest_dir_path = path.join(tmp_dest_dir, 'usr', 'share', 'hunspell')
        word_package_path = path.join(word_dest, name)
        set_types = {}
        for file in sorted(listdir(tmp_dest_dir_path)):
            file_path = path.join(tmp_dest_dir_path, file)
            if file.endswith('.aff') and not file.startswith('hyph') and not path.islink(file_path):
                # Get SET type
                dikt = file[:-4]
                set_type = None
                try:
                    aff = open(file_path)
                    for line in aff:
                        if 'SET' in line:
                            set_type = line.strip().replace('\t', ' ').split(' ')[1].lower()
                            break
                except UnicodeDecodeError:
                    # using this encoding is enough to only! get SET
                    aff = open(file_path, encoding='iso8859-1')
                    for line in aff:
                        if 'SET' in line:
                            set_type = line.strip().replace('\t', ' ').split(' ')[1].lower()
                            break
                set_types[dikt] = set_type

                # Convert file
                dest_file_path = path.join(dest_dir, file)
                copyfile(file_path, dest_file_path)

        for file in sorted(listdir(tmp_dest_dir_path)):
            file_path = path.join(tmp_dest_dir_path, file)
            if file.endswith('.dic') and not file.startswith('hyph') and not path.islink(file_path):
                # Get SET type
                dikt = file[:-4]
                set_type = set_types[dikt]

                # Convert file
                dest_file_path = path.join(dest_dir, file)
                if dikt in ('an_ES', 'ca', 'ca_ES-valencia', 'nb_NO', 'kmr_Latn', 'oc_FR'):
                    conv(file_path, set_type, dest_file_path, set_type, re.compile('/$'))
                elif dikt == 'eu':
                    conv(file_path, set_type, dest_file_path, set_type, re.compile('/None$'))
                elif dikt == 'gl_ES':
                    conv(file_path, set_type, dest_file_path, set_type, re.compile(' po:.+$'))
                elif dikt == 'lv_LV':
                    conv(file_path, set_type, dest_file_path, set_type, re.compile('/ po:.+$'))
                else:
                    copyfile(file_path, dest_file_path)

                wordlist = lookup(['dict2wordlist', dikt])
                if wordlist != '':
                    continue

                # Generate words from .dic file
                if not path.isdir(word_package_path):
                    mkdir(word_package_path)
                conv(file_path, set_type, dest_file_path+'.tmp')
                file_type = from_file(dest_file_path+'.tmp')
                if 'line terminators' in file_type:
                    dos2unix(dest_file_path+'.tmp', dest_file_path + '.txt')
                else:
                    replace(dest_file_path+'.tmp', dest_file_path + '.txt')

                word_file_path = path.join(word_package_path, dikt)
                words_set = set() # Prevents duplicate words
                txt = open(dest_file_path + '.txt')
                first = True
                #LATER Refactor below to use regex
                for line in txt:
                    if first:
                        first = False
                        continue
                    index = line.find('#')
                    if index != -1:
                        line = line[:index]
                    if line != '' and line[0] == ' ':
                        continue
                    line = line.strip()
                    if line == '' or line[0] == '/' or line[0] == '[':
                        continue
                    index = line.find('\\/') # one backslash and one slash
                    if index != -1:
                        pos = line.find('/', index+2)
                        if pos != -1:
                            line = line[:pos]
                    else:
                        line = line.split('/')[0]
                    line = line.replace('\t', ' ').replace('  ', ' ').replace('  ', ' ')
                    if ' /' in line:
                        continue
                    line = line.split(' po:')[0]
                    line = line.split(' [')[0]
                    line = line.split(' 0')[0]
                    line = line.split(' 1')[0]
                    line = line.split(' 2')[0]
                    line = line.split(' 3')[0]
                    line = line.split(' 4')[0]
                    line = line.split(' 5')[0]
                    line = line.split(' 6')[0]
                    line = line.split(' 7')[0]
                    line = line.split(' 8')[0]
                    line = line.split(' 9')[0]
                    words_set.add(line)
                words = open(word_file_path, 'w')
                for word in sorted(words_set):
                    words.write(f'{word}\n')
                if path.isfile(dest_file_path+'.tmp'):
                    remove(dest_file_path+'.tmp')
                if path.isfile(dest_file_path + '.txt'):
                    remove(dest_file_path + '.txt')

    # Return to original path
    chdir(org)

def extract_list():
    '''Extract and convert list packages'''
    print('INFO: Extract list packages')
    org = getcwd()

    # Prepare extract directory and empty it
    tmp_dest = path.join('..', 'files-list')
    mk_or_clear_dir_and_cd(tmp_dest)

    # Prepare convert directory and empty it
    dest = path.join('..', 'list')
    mk_or_clear_dir_and_cd(dest)

    src = path.join('..', 'packages-list')
    chdir(src)
    for package in sorted(listdir()):
        name = package[:package.find('_all.deb')] # expected file name ending
        print(f'  {name}')
        tmp_dest_dir = path.join(tmp_dest, name)
        mkdir(tmp_dest_dir)
        execute(["dpkg", "-x", package, tmp_dest_dir])

        dest_dir = path.join(dest, name)
        mkdir(dest_dir)
        tmp_dest_dir_path = path.join(tmp_dest_dir, 'usr', 'share', 'dict')
        for file in sorted(listdir(tmp_dest_dir_path)):
            file_path = path.join(tmp_dest_dir_path, file)
            if not path.islink(file_path):
                # Convert file
                file_type = from_file(file_path)
                if 'UTF-8 Unicode text' in file_type:
                    file_type = 'utf-8'
                elif 'ISO-8859 text' in file_type:
                    file_type = 'iso8859-1'
                elif 'ASCII text' in file_type:
                    file_type = 'ascii'
                else:
                    print(f'ERROR: Unsupported file type {file_type} for file f{file}')
                dest_file_path = path.join(dest_dir, file)
                copyfile(file_path, dest_file_path)

    # Return to original path
    chdir(org)


def download():
    '''Download'''

    # help option prevents non-zero return
    execute(["apt-cache", "--help"], True)
    execute(["apt-get", "--help"], True)
    execute(["wget", "--help"], True)
    download_dict()
    download_list()

def extract():
    '''Extract'''

    # help option prevents non-zero return
    execute(["dpkg", "--help"], True) # Simple uncompress omits patches
    extract_dict()
    extract_list()

def histogram_dict():
    '''Histrogram dict'''
    print('INFO: Histogram dictionaries')
    org = getcwd()

    #LATER

    # Return to original path
    chdir(org)

def histogram_list():
    '''Histrogram list'''
    print('INFO: Histogram word lists')
    org = getcwd()

    #LATER

    # Return to original path
    chdir(org)

def histogram_word():
    '''Histrogram word'''
    print('INFO: Histogram generated word lists')
    org = getcwd()

    #LATER

    # Return to original path
    chdir(org)

def histogram():
    '''Histogram'''
    histogram_dict()
    histogram_list()
    histogram_word()

def test():
    '''Test dictionaries'''
    print('INFO: Test dictionaries')
    org = getcwd()

#    # Short non-existing word that doesn't trigger compounding
#    word = 'qqqq'
#    #echo $WORD | hunspell -d ./$LANG
#    #echo $WORD | nuspell -d ./$LANG

    # Return to original path
    chdir(org)

def verify():
    '''Verify'''
    print('INFO: Verify')
    org = getcwd()

    # Prepare result directory and empty it
    dest = path.join('..', 'verification')
    mk_or_clear_dir_and_cd(dest)

    src = path.join('..', 'dict')
    chdir(src)
    # Some path juggling to have short paths in verification/*.out files
    verify_path = path.join('..', 'nuspell', 'build', 'tests', 'verify')
    for package in sorted(listdir()):
        chdir(package)
        for dikt in sorted(listdir()):
            if dikt[-4:] != '.aff':
                continue
            dikt = dikt[:-4]
            print(f'  {package} {dikt}')
            wordlist = lookup(['dict2wordlist', dikt])
            wordlist_package = lookup(['dict2package', dikt])
            output_path = path.join('..', dest, package + '=' + dikt)
            input_path = None
            if wordlist == '':
                input_path = path.join(package, dikt)
                chdir(path.join('..', '..', 'word'))
            else:
                for file in sorted(listdir(path.join('..', '..', 'list'))):
                    # search as version number is unknown
                    if file.startswith(wordlist_package):
                        input_path = path.join(file, wordlist)
                        continue
                chdir(path.join('..', '..', 'list'))
            dict_path = path.join('..', 'dict', package, dikt)
#            print(f'DEBUG: Running {verify_path} -d {dict_path} {input_path}')
            out, err = execute([verify_path, "-d", dict_path, input_path])
            chdir(path.join('..', 'dict', package))

            outfile = open(output_path + '.out', 'w')
            errfile = open(output_path + '.err', 'w')
            outfile.write(out)
            errfile.write(err)

        chdir('..')

    # Return to original path
    chdir(org)

def compress():
    '''Compress dict, list and word directories'''
    print('INFO: Compress')
    org = getcwd()

    # Compress
    chdir('..')
    compress_archive('dict')
    compress_archive('list')
    compress_archive('word')

    # Return to original path
    chdir(org)

def uncompress():
    '''Uncompress dict, list and word directories'''
    print('INFO: Uncompress')
    org = getcwd()

    # Uncompress
    chdir('..')
    uncompress_archive('dict')
    uncompress_archive('list')
    uncompress_archive('word')

    # Return to original path
    chdir(org)

def report():
    '''Report verification in MarkDown file with links'''
    print('INFO: Report')
    org = getcwd()

    # Read output files
    results = []
    min_accuracy = sys.float_info.max
    min_precision = sys.float_info.max
    min_speedup = sys.float_info.max
    min_speedup_max = sys.float_info.max
    max_accuracy = 0.0
    max_precision = 0.0
    max_speedup = 0.0
    max_speedup_max = 0.0
    ave_accuracy = 0.0
    ave_precision = 0.0
    ave_speedup = 0.0
    ave_speedup_max = 0.0
    input_path = path.join('..', 'verification')
    for file in sorted(listdir(input_path)):
        if file.endswith('.out'):
            dikt = file[:-4]
            print(f'  {dikt}')
            result = open(path.join(input_path, file))
            words = None
            accuracy = None
            precision = None
            speedup = None
            speedup_max = None
            for line in result:
                line = line.strip()
                if line.startswith('Total Words'):
                    words = line.split(' ')[-1]
                elif line.startswith('Accuracy'):
                    accuracy = float(line.split(' ')[-1])
                    if accuracy < min_accuracy:
                        min_accuracy = accuracy
                    if accuracy > max_accuracy:
                        max_accuracy = accuracy
                    ave_accuracy += accuracy
                elif line.startswith('Precision'):
                    precision = float(line.split(' ')[-1])
                    ave_precision += precision
                    if precision < min_precision:
                        min_precision = precision
                    if precision > max_precision:
                        max_precision = precision
                elif line.startswith('Speedup'):
                    speedup = float(line.split(' ')[-1])
                    ave_speedup += speedup
                    if speedup < min_speedup:
                        min_speedup = speedup
                    if speedup > max_speedup:
                        max_speedup = speedup
                elif line.startswith('Maximum Speedup'):
                    speedup_max = float(line.split(' ')[-1])
                    ave_speedup_max += speedup_max
                    if speedup_max < min_speedup_max:
                        min_speedup_max = speedup_max
                    if speedup_max > max_speedup_max:
                        max_speedup_max = speedup_max
            results.append({'d':dikt, 'w':words, 'a':accuracy, 'p':precision,
                            's':speedup, 'm':speedup_max})

    ave_accuracy /= len(results)
    ave_precision /= len(results)
    ave_speedup /= len(results)
    ave_speedup_max /= len(results)

    output = open(path.join('..', 'report.md'), 'w')

    output.write('## Verification test results\n')

    output.write('\n')
    output.write(f'\nThe results below are measured on {len(results)}' \
                 ' dictionaries for very large word lists. Word frequency' \
                 ' histograms of text typically have a long tail, hence' \
                 ' speedup maximum is also reported on. Nuspell is more' \
                 ' thorough than Hunspell and infrequent compounded words ' \
                 ' result sometimes in a lower average speedup. Frequently ' \
                 ' used words however have a much higher speedup.\n\n')

    output.write('\n')
    output.write('| metric | average | minimum | maximum |\n')
    output.write('|--------|--------:|--------:|--------:|\n')
    output.write('| Accuracy        | {:.3f} | {:.3f} | {:.3f} |\n'
                 .format(ave_accuracy, min_accuracy, max_accuracy))
    output.write('| Precision       | {:.3f} | {:.3f} | {:.3f} |\n'
                 .format(ave_precision, min_precision, max_precision))
    output.write('| Speedup         | {:.1f} | {:.1f} | {:.1f} |\n'
                 .format(ave_speedup, min_speedup, max_speedup))
    output.write('| Speedup Maximum | {:.1f} | {:.1f} | {:.1f} |\n'
                 .format(ave_speedup_max, min_speedup_max, max_speedup_max))

    output.write('\n')
    output.write('| speedup | speedup max. | dictionary |' \
                 ' package | accuracy |\n')
    output.write('|--------:|-------------:|------------|' \
                 '---------|---------:|\n')
    results = sorted(results, key=itemgetter('s'), reverse=True)
    for result in results:
        dik = result['d']
        package, dikt = dik.split('=')
        package = package.replace('hunspell-', '').replace('myspell-', '')
        dik = dik.replace('%', '%25')
        acc = result['a']
        spe = result['s']
        max_spe = result['m']
        output.write('| {:.1f} | {:.1f} | [{}](verification/{}.out)| {} |' \
                     ' {:.3f} |\n'
                     .format(spe, max_spe, dikt, dik, package, acc))

    # Return to original path
    chdir(org)

def main(args):
    '''Main'''
    if len(args) == 0:
        uncompress()
        verify()
        report()
    elif len(args) == 1:
        if args[0] == 'download':
            download()
        elif args[0] == 'extract':
            extract()
        elif args[0] == 'histogram':
            histogram()
        elif args[0] == 'compress':
            compress()
        elif args[0] == 'uncompress':
            uncompress()
        elif args[0] == 'test':
            test()
        elif args[0] == 'verify':
            verify()
        elif args[0] == 'report':
            report()
        else:
            error()
    else:
        error()

if __name__ == "__main__":
    chdir(path.dirname(path.realpath(__file__)))
    main(sys.argv[1:])
    
