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

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract the year and print it
 - Extract the names and rank numbers and just print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a single list starting
    with the year string followed by the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    names = []
    with open(filename, 'r') as file:
        
        find_year = re.search(r'Popularity\sin\s(\d\d\d\d)', file)
        if not find_year:
            sys.stderr.write("No year found")
            sys.exit(1)
        year = find_year.group(1)
        names.append(year)

        tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', file)

        name_ranks = {}
        for rank_tuple in tuples:
            (rank, boyname, girlname) = rank_tuple
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

    for filename in file_list:
        print("Working on file: {}".format(filename))
        names = extract_names(filename)

    text = '\n'.join(names)

    if create_summary:
        with open(filename + '.summary', 'w') as output_file:
            output_file.write(text + '\n')
    
    else:
        print(text)

    

if __name__ == '__main__':
    main(sys.argv[1:])
