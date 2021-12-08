#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

if len(sys.argv[1:]) == 0:
    print("""
                Get the annotations from a list of md5s.
                usage: python3 m5nr_annotation.py database database.dict md5s.txt output
                Available databases: GenBank, RefSeq, SEED
                Miguel Romero github.com/miferg
                """
                )
    sys.exit()

argv = sys.argv[1:]

import pickle

print()
print('''
Get the annotations from a list of md5s.
Miguel Romero github.com/miferg
''')

if argv[0] in ['GenBank','RefSeq','SEED']:
    print('Database: '+ argv[0])
else:
    print('Please use one of the available databases: GenkBank, RefSeq, SEED\n')
    sys.exit()

print('Loading database, this may take a few minutes (and ~97 GBs of memory).')

database = pickle.load(open(os.path.abspath(argv[1]), "rb"))

print('Loading input.')

handle = open(argv[2],'r')
md5s = handle.read().split('\n')[:-1]
handle.close()

print('Writing output in '+ argv[3])
outfile = open(argv[3], 'w')

absent = []

if argv[0] == 'GenBank':
    for md5 in md5s:
        try:
            outfile.write(md5 +'\t'+ database[md5] +'\n')
        except:
            absent.append(md5)
    outfile.close()

if argv[0] == 'RefSeq':
    for md5 in md5s:
        try:
            outfile.write(md5 +'\t'+ '\t'.join(list(database[md5])) +'\n')
        except:
            absent.append(md5)
    outfile.close()

elif argv[0] == 'SEED':
    for md5 in md5s:
        try:
            ssids = database[md5]
            for line in ssids:
                outfile.write(md5 +'\t'+ line)
        except:
            absent.append(md5)
    outfile.close()

if len(absent) > 0:
    print('There were '+ str(len(absent)) +' md5s missing in the annotation database.')
    print('Check the m5nr_annotation_missing.txt file.')
    outfile = open('m5nr_annotation_missing.txt','w')
    outfile.write('\n'.join(absent) +'\n')
    outfile.close()

print('Done!\n')
