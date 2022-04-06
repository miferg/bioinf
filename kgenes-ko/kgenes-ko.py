#!/usr/bin/env python3

import sys
import subprocess

try:
    infile = sys.argv[1]

except:
    print("""
Miguel F. Romero, 2022
github.com/miferg
Get the KO numbers from a list of KEGG GENES ids using the KEGG API.
Usage:
get_table.py gene-ids.txt > ko-ids.csv
    """)
    sys.exit()


handle = open(infile, 'r')
ids = handle.read().split('\n')[:-1]
handle.close()

for i in ids:
    process = subprocess.Popen("curl -s curl http://rest.kegg.jp/link/orthology/"+ i, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    keggout = str(stdout)
    if 'ko:' in keggout:
        ko = keggout.split('ko:')[1]
        ko = ko.split('\\n')[0]
        print(i +','+ ko)
    else:
        print(i +',not_found')
