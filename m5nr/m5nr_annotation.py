#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if len(sys.argv[1:]) == 0:
    print("""
Get the annotations from a list of md5s.
usage: python3 m5nr_annotation.py database md5s.txt output
Miguel Romero github.com/miferg""")
    sys.exit()

argv = sys.argv[1:]

import pickle

print('''
Get the annotations from a list of md5s.
Miguel F. Romero github.com/miferg''')

print('Database: RefSeq')

print('Loading database, this may take a few minutes (and ~60 GBs of memory).')

try:
    database = pickle.load(open("INSERT_DATABASE_PATH_HERE", "rb")) ### <--- INSERT THE DATABASE PATH HERE!
except:
    print("Please make sure that you downloaded the database and declared it in this script!")
    sys.exit()

print('Loading input.')

handle = open(argv[1],'r')
md5s = handle.read().split('\n')[:-1]
handle.close()

print('Writing output in '+ argv[2])

outfile = open(argv[2], 'w')
for line in md5s:
    outfile.write(line +'\t'+ '\t'.join(list(database[line])) +'\n')
outfile.close()

print('Done!')
