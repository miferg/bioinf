#!/usr/bin/env python3

"""
sam-coid
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to create a coverage - identity plot.
Usage:
sam-coid.py mapping.sam prefix
"""

import sys
import subprocess

try:
    mapp_name = sys.argv[1]
    prefix = sys.argv[2]

except:
    print("""
sam-coid
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to create a coverage - identity plot.
Usage:
sam-coid.py mapping.sam prefix
    """)
    sys.exit()

### Functions

def read_file(filename):
    """open files and save them as a list of lines"""
    handle = open(filename, 'r')
    content = handle.read().split('\n')[:-1]
    handle.close()
    return(content)
    
def parse_MD(md, matches, current_number, switch, mismatches):
    """read an MD string and count matches and mismatches"""
    if md[0] in '0123456789':
        current_number += md[0]
        if switch == 0:
            switch = 1
    else:
        if current_number!='':
            matches += int(current_number)
            current_number = ''
        if md[0] == '^':
            switch = 0
        else:
            if switch == 1:
                mismatches += 1
    if len(md[1:]) >= 1:
        return(parse_MD(md[1:], matches, current_number, switch, mismatches))
    else:
        if current_number!='':
            matches += int(current_number)
        return(matches, mismatches)

def alignment_2_coiv(line):
    """split a SAM file and write the position and identity"""
    md1 = line.split('MD:Z:')
    md = md1[1].split('\t')[0]
    matches, mismatches = parse_MD(md, 0, '', 1, 0)
    linesep = line.split('\t')
    columns = [linesep[2], linesep[3],str(matches/(matches + mismatches))]
    return('\t'.join(columns) +'\n')

### Main program

def main():

    print("""
sam-coid
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to create a coverage - identity plot.
""")

    print('Reading SAM input.\n')
    sam = read_file(mapp_name)
    
    print('Parsing alignments.\n')
    outlist = ''.join((map(alignment_2_coiv, sam)))
    
    print('Writing output file.\n')
    outfile = open(prefix +'.coid.tsv', 'w')
    outfile.write('ref\tpos\tid\n')
    outfile.write(outlist)
    outfile.close()
    
    print('Done!\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n(Terminating due to user interrupt signal)")
