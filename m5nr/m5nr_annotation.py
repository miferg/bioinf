#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get annotations from a list of md5s.
"""

import pickle
import sys
import os

try:
    db_file = sys.argv[1]
    m5_file = sys.argv[2]
    outprefix = sys.argv[3]
    
except:
    print("""
                Get the annotations from a list of md5s.
                usage: python3 m5nr_annotation.py database.dict md5s.txt output_prefix
                Available databases: 
                m5nr_genbank.dict = GenBank
                m5nr_refseq.dict = RefSeq
                m5nr_seed.dict = SEED
                m5nr_kegg.dict = KEGG GENES
                m5nr_cog.dict = COG
                Miguel F. Romero github.com/miferg
                """
                )
    sys.exit()

argv = sys.argv[1:]

### DEFINITIONS

db_dict = {
        'm5nr_genbank.dict':['GenBank','97'],
        'm5nr_refseq.dict':['RefSeq','60'],
        'm5nr_seed.dict':['SEED','20'],
        'm5nr_kegg.dict':['KEGG','6'],
        'm5nr_cog.dict':['COG','0.005']
        }

def greet():
'''
Say hi
'''
    print()
    print('''
    Get the annotations from a list of md5s.
    Miguel F. Romero github.com/miferg
    ''')
    return 0

def check_db(dbfile, dbdict):
'''
Check if the database file is supported
'''
    if dbfile in db_dict.keys():
        print('Database: '+ db_dict[dbfile][0])
        print('Loading database, this may take a few minutes (and ~'+ db_dict[dbfile][1] +' GBs of memory).')
        return 0
    
    else:
        print('Please use one of the available databases.\n')
        sys.exit()
        
def genbank(m5_file, database, outfile, absent):
'''
Write the genbank annotations
'''
    with open(m5_file, 'r') as infile:
        for line in infile:
            md5 = line.strip()
            try:
                outfile.write(md5 +'\t'+ database[md5] +'\n')
            except:
                absent.append(md5)
    return outfile, absent

def refseq(m5_file, database, outfile, absent):
'''
Write the refseq annotations
'''
    with open(m5_file, 'r') as infile:
        for line in infile:
            md5 = line.strip()
            try:
                outfile.write(md5 +'\t'+ '\t'.join(list(database[md5])) +'\n')
            except:
                absent.append(md5)
    return outfile, absent
        
def seed(m5_file, database, outfile, absent):
'''
Write the seed annotations
'''
    with open(m5_file, 'r') as infile:
        for line in infile:
            md5 = line.strip()
            try:
                ssids = database[md5]
                for line in ssids:
                    outfile.write(md5 +'\t'+ line)
            except:
                absent.append(md5)
    return outfile, absent

def kegg(m5_file, database, outfile, absent):
'''
Write the kegg annotations
'''
    with open(m5_file, 'r') as infile:
        for line in infile:
            md5 = line.strip()
            try:
                outfile.write(md5 +'\t'+ database[md5] +'\n')
            except:
                absent.append(md5)
    return outfile, absent

def cog(m5_file, database, outfile, absent):
'''
Write the cog annotations
'''
    with open(m5_file, 'r') as infile:
        for line in infile:
            md5 = line.strip()
            try:
                outfile.write(md5 +'\t'+ database[md5]) +'\n')
            except:
                absent.append(md)
    return outfile, absent
    
def get_table(m5_file, database, dbfile, outfile, absent):
'''
Set the database to use and run the dedicated function
''' 
    if dbfile == 'm5nr_genbank.dict':
        return genbank(m5_file, database, outfile, absent)
                
    if dbfile == 'm5nr_refseq.dict':
        return refseq(m5_file, database, outfile, absent)
                
    if dbfile == 'm5nr_seed.dict':
        return seed(m5_file, database, outfile, absent)
                
    if dbfile == 'm5nr_kegg.dict':
        return kegg(m5_file, database, outfile, absent)
                
    if dbfile == 'm5nr_cog.dict':
        return cog(m5_file, database, outfile, absent)

def check_absents(absent):
'''
Write the absent md5s if any
'''
    if len(absent) > 0:
        print('There were '+ str(len(absent)) +' md5s missing in the annotation database.')
        print('Check the '+ outprefix+'.'+db_dict[dbfile][0]+'. missing.txt file.')
        with open(outprefix+'.'+db_dict[dbfile][0]+'. missing.txt','w') as outfile:
            outfile.write('\n'.join(absent) +'\n')
    return 0
    
### MAIN PROGRAM

def main():
    
    greet()

    dbfile = os.path.abspath(db_file).split('/')[-1]

    check_db(dbfile, dbdict)

    with open(os.path.abspath(db_file), "rb") as infile:
        database = pickle.load(infile)

    print('Writing output in '+ outprefix+'.'+db_dict[dbfile][0]+'.tsv')
    
    outfile = open(outprefix+'.'+db_dict[dbfile][0]+'.tsv', 'w')

    absent = []
    
    outfile, absent = get_table(m5_file, database, dbfile, outfile, absent)

    outfile.close()

    check_absents(absent)

    print('Done!\n')
    
    return 0

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n(Terminating due to user interrupt signal)")
