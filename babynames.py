#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

__author__ = "Janelle Kuhns and class demo"

import sys
import re
import argparse

def extract_names(filename):
    names = []
    with open(filename) as f:
        text = f.read()

        find_year = re.search(r'Popularity\sin\s(\d\d\d\d)', text)
        if not find_year:
            sys.stderr.write("No year found")
            sys.exit(1)
        year = find_year.group(1)
        names.append(year)

        tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)

        name_ranks = {}
        for rank, boyname, girlname in tuples:
            if boyname not in name_ranks:
                name_ranks[boyname] = rank
            if girlname not in name_ranks:
                name_ranks[girlname] = rank

        sorted_names = sorted(name_ranks.keys())

        for name in sorted_names:
            names.append(name + ' ' + name_ranks[name])

        return names

def create_parser():
    parser = argparse.ArgumentParser(description="Extracts and alphabetizes baby names from HTML")
    parser.add_argument('--summaryfile', help='create a summary file', action="store_true")
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser

def main(args):
    parser = create_parser()
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    create_summary = ns.summaryfile

    for file in file_list:
        name_list = extract_names(file)
        text = '\n'.join(name_list)
        if create_summary:
            with open(file + '.summary', 'w') as output_file:
                output_file.write(text + '\n')
        else:
            print(text)

    

if __name__ == '__main__':
    main(sys.argv[1:])
