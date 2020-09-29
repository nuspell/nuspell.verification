# Verification of Nuspell

Verification spelling for Nuspell with Hunspell and speedup reporting

# Goals

This repository has the following goals. To verify the correctness of the spell
checking of Nuspell with regard to Hunspell using dictionaries available on
Ubuntu This reports on true and false positives and negatives in terms of
accuracy and precision. Additionally reporting is done on the speedup.

Secondly, these tests need to run on all platforms and in CI. For that, the
programming for this is done in platform-independent Python scripts. All data
needed in terms of dictionaries and word lists is stored in this publicly
available repository to be used easily anywhere.

# Organization

This repository is organized in the following way.

As GitHub can only hold a maximum of 100 MB, the data needed for verification
testing are stored in the compressed files `dict.zip` for the dictionaries,
`list.zip` for existing word lists (often made by dictionary maintainers) and
`word.zip` for word lists generated from `.dic` dictionary files where word
lists were not available for. These files need to be uncompressed in the
respective directories `dict`, `list` and `word` before being used.

In `.gitignore` are all temporary directories used during the creation of the
test data. The `scripts` directory contains the software needed to generate
or update the dictionaries and word lists, to run the verification and report on
it. Verification results can be found in the `verification` directory and an
overall report is found in `report.md`.

## Dictionaries

These are found in the `dict` directory. The subdirectory is the name and
version of the package. In there are pairs of a `.aff` and `.dic` files. E.g.

    dict/
    ├── hunspell-fr-classical_1%3a6.4.1-1
    │   ├── fr.aff
    │   └── fr.dic
    ├── hunspell-fr-comprehensive_1%3a6.4.1-1
    │   ├── fr.aff
    │   └── fr.dic
    ├── myspell-fr_1.4-27
    │   ├── fr.aff
    │   └── fr.dic
    ...
    ├── hunspell-no_1%3a6.4.3-1
    │   ├── nb_NO.aff
    │   ├── nb_NO.dic
    │   ├── nn_NO.aff
    │   └── nn_NO.dic
    ...
    ├── hunspell-ca_3.0.4+repack1-1
    │   ├── ca.aff
    │   ├── ca.dic
    │   ├── ca_ES-valencia.aff
    │   └── ca_ES-valencia.dic
    ...
    ├── hunspell-sr_1%3a6.4.3-1
    │   ├── sr_Latn_RS.aff
    │   ├── sr_Latn_RS.dic
    │   ├── sr_RS.aff
    │   └── sr_RS.dic
    ...

Note a package can have multiple dictionaries, for various reasons, and multiple
packages can offer identical dictionary names. This is normally guarded with
package dependencies, here all dictionaries are referred to relative to the
package they originate from. Not only the have unique path but also to track
changes in versions when those occur.

## Word lists

Word lists offered by dictionary maintainers are organized in a similar way.

    list
    ├── wcatalan_0.20111230b-12
    │   └── catalan
    ...
    ├── wngerman_20161207-7
    │   └── ngerman
    ├── wswiss_20161207-7
    │   └── swiss
    ...
    ├── wnorwegian_2.2-4
    │   ├── bokmaal
    │   └── nynorsk
    ...

## Generated word lists

Word lists were generated for dictionaries that did not have a separate word
list.

    word
    ├── hunspell-ca_3.0.4+repack1-1
    │   └── ca_ES-valencia
    ...
    ├── hunspell-de-at_20161207-7
    │   └── de_AT
    ├── hunspell-de-at-frami_1%3a6.4.3-1
    │   └── de_AT_frami
    ...
    ├── hunspell-kmr_1%3a6.4.3-1
    │   └── kmr_Latn
    ...

Note that for dictionaries from the same dictionary package, it can happen that
one can use a provided word list and another needs to use a generated word list.

# Analysis

Dictionary files and word list files have been analyzed thoroughly with also
examination of the character histograms. Overview reports from previous analysis
can be found at in the directory `doc`.

From investigating the dictionaries closely, issues came forward. These were
reported and are monitored in
https://github.com/nuspell/nuspell/wiki/Dictionaries-and-Contacts

Issues are getting resolved by the upstream authors or package maintainers.
In some cases, due to long lead times before a package becomes available in
Ubuntu, an upstream url is used to retrieve the latest files. See the files
`dict-package-urls` and `list-package-urls` where the download actions is
described below.

In the past, an analysis was done on Myspell dictionary packages, see
https://github.com/nuspell/nuspell/wiki/Ubuntu-legacy-Myspell-packages

For the verification test here, these are not included due two reasons. First is
the size limitation of the repository, but more importantly, they are no longer
maintained or relevant as newer Hunspell dictionaries are meant to be used.
However, they have been tested successfully and have similar accuracy and
precision as Hunspell packages. They can easily be retested, but for now they
are excluded from the verification tests.

In order to analyze character histograms of files, see `scripts/histogram.py`.

# Scripts

In the script directory is the main script called `run.py` but also some helper
scripts and files such as `langauges.py`, which uses `languages.json`. As the
codes, names and abbreviations of languages, countries, regions and scripts is at
times very irregular in the names of packages and files for dictionaries and
word lists. This helper script solved this challenge. Running `languages.py`
will print help for manual use, but that is normally not needed as script is
called by `run.py`.

## Prerequisites

Before using `run.sh`, install the following:

    sudo apt-get install python3-pip
    sudo pip3 install -U python-magic

If dictionaries and word lists are going to be extracted from downloaded
packages, follow also additional instructions from
https://github.com/ahupp/python-magic#installation

Also a version of Nuspell needs to be made available in a directory called
`nuspell`. This is ignored by git here. Nuspell needs to be build according to
the usual build instructions in order to have access to
`nuspell/build/tests/verification`. Note that a version of the verification
script which report on the following is needed:
- `Total Words`
- `Accuracy`
- `Precision`
- `Speedup`
- `Maximum Speedup`

## Download

Downloading dictionary and word list packages is done with:

    cd scripts
    ./run.py download

Temporary files that are involved (and ignored by git) are:
- `packages-dict` downloaded Debian packages for dictionaries (~35 MB)
- `packages-list` downloaded Debian packages for word lists (~26 MB)
- `script/dict-package-names` dictionary names to find new or removed packages
- `script/list-package-names` word list names to find new or removed packages

In case of conflict, the files `script/*-package-names` can be removed before a
new download is done. This file exist to warn about packages that have been
dropped from Ubuntu or have been added to Ubuntu.

Configuration files are:
- `scripts/languages.json` for looking up language names, etc.
- `scripts/dict-package-skip` dictionary packages to skip
- `scripts/dict-package-urls` additional dictionary packages to download
- `scripts/list-package-urls` additional word list packages to download

Any additional dictionary package will replace packages from the normal
download.

The download action only works on a system with access to:
- `apt-cache`
- `apt-get`
- `wget`

The download action typically takes less then a minute to complete.

## Extract

Downloaded packages are extracted and processed in the extract action. This is
done with:

    cd scripts
    ./run.py extract

Temporary files that are involved (and ignored by git) are:
- `files-dict` extracted dictionary packages (40 MB)
- `files-list` extracted word list packages (25 MB)

Usable files (and ignored by git) are found in:
- `dict` (~200 MB)
- `list` (~200 MB)
- `word` (~100 MB)

This currently only works on a GNU/Linux machine. Note that the extracted
packages also take up more than 100 MB to be stored in git.

The extract action only works on a system with access to `dpkg`. Simply
unzipping a `.deb` file is not sufficient as the packages contain one or more
patches that fix issues with the upstream files.

Note that word list are only generated from `.dic` files when no word list
package was available. Generation of these lists uses complete words or
unsuffixed words stripped from flags and comments.

The extract action typically takes less then a minute to complete.

## Compress

The directories `dict`, `list` and `word` can be compressed to `dict.zip`,
`list.zip` and `word.zip` with:

    cd scripts
    ./run.py compress

Before pushing new `.zip` files to the repository, make sure the total size of
the repository does not exceed 100 MB. The compress action typically takes less
then a minute to complete.

## Uncompress

The files `dict.zip` (~41 MB), `list.zip` (~36 MB) and `word.zip` (~20 MB) can
be uncompressed to the directories `dict`, `list` and `word` with:

    cd scripts
    ./run.py uncompress

Existing uncompressed directories will not be overridden, then the uncompression
for that file will be skipped. The uncompress action typically takes less then
a minute to complete.

## Verify

To run the verification on all dictionaries and word lists do:

    cd scripts
    ./run.py verify

This will call the executable `verify` that resides in `nuspell/build/tests`.
Output of each test is written to the directory `verification`. Verification
takes typically 15 minutes to run. Note that all tests are not run in parallel.

## Report

The file `report.md` is created with:

    cd scripts
    ./run.py report

It will process all the `.out` files in the directory `verification`. The report
file will have links to the analyzed files for a drill down to more details.
This script takes typically a second to complete.

## Default

By default, the script `run.py` will do the following actions:
1. uncompress
2. verify
3. report

This is useful for automated verification testing in .e.g. CI. Note that the
download, extract and compress actions are only needed once so that the data
needed for the tests can be stored in this repository.

# Other

All typical processing times here are from an i7-10510U CPU @ 1.80GHz.
