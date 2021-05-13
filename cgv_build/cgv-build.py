#!/usr/bin/env python3

"""
cgv-build
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to be read by the CGView software.
Usage:
cgv_build.py genomic.fna annotation.gff mapping.sam prefix
"""

import sys
import subprocess

try:
    genom_name = sys.argv[1]
    annot_name = sys.argv[2]
    mapp_name = sys.argv[3]
    prefix = sys.argv[4]

except:
    print("""
cgv-build
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to be read by the CGView software.
Usage:
cgv-build.py genomic.fna annotation.gff mapping.sam prefix
    """)
    sys.exit()

### functions

def read_file(filename):
    """open files and save them as a list of lines"""
    handle = open(filename, 'r')
    content = handle.read().split('\n')[:-1]
    handle.close()
    return(content)

def count_contigs(genome):
    """"get the ID of each contig and its starting coordinate and the complete sequence"""
    contigs = {}
    lens = {}
    complete = ''
    for line in genome:
        if '>' in line:
            current = line[1:].split(' ')[0]
            contigs[current] = len(complete)
            lens[current] = 0
        else:
            complete += line
            lens[current] += len(line)
    return(contigs, complete, lens)

def format_gff(gff, contigs):
    """get the desired annotations with the new coordinates"""
    annot_cgv = 'seqname\tsource\tfeature\tstart\tend\tscore\tstrand\tframe\n'
    for line in gff:
        if line[0] != '#':
            linesep = line.split('\t')
            if linesep[2] in ('CDS','tRNA','rRNA'):
                annotation = []
                annotation.append(linesep[8].split(';')[0][3:])
                annotation.append('.')
                annotation.append(linesep[2])
                annotation.append(str(contigs[linesep[0]] + int(linesep[3])))
                annotation.append(str(contigs[linesep[0]] + int(linesep[4])))
                annotation.append('.')
                annotation.append(linesep[6])
                annotation.append('.')
                annot_cgv += '\t'.join(annotation) + '\n'
    return(annot_cgv)

def sam_2_mappos(mapp, prefix, barnum, genomlen, cont_lens):
    """create the map table from the sam input"""
    mappos_dict = {}
    ticklen = round(genomlen/barnum)
    for key in cont_lens.keys():
        ticks_in_cont = round(cont_lens[key]/ticklen)
        for i in range (1, ticks_in_cont + 1):
            mappos_dict[(key,i*ticklen)] = 0
    for line in mapp:
        linesep = line.split('\t')
        mappos_dict[(linesep[2], ((int(linesep[3])//ticklen) + 1)* ticklen)] += 1
    outable = "seqname\tsource\tfeature\tstart\tend\tscore\tstrand\tframe\n"
    for key in mappos_dict.keys():
        columns = []
        columns += [key[0], prefix,'.', str(1 +(key[1]-ticklen)), str(key[1]), str(mappos_dict[key]/len(mapp)), '+','.']
        outable += '\t'.join(columns) +'\n'
    return(outable)    

### main script

def main():

    print("""
cgv-build
Miguel F. Romero, 2021
github.com/miferg
    """)
  
    print('Loading files.\n')
    genom, annot, mapp = map(read_file, (genom_name, annot_name, mapp_name))

    print('Counting contig sizes.\n')
    contigs, complete_genome, cont_lens = count_contigs(genom)

    print('Building new annotation.\n')
    annot_cgv = format_gff(annot, contigs)

    print('Getting new mapping positions.\n')
    mappos = sam_2_mappos(mapp, prefix, 3600, len(complete_genome), cont_lens)

    print('Writing output files.\n')

    outfile = open(prefix +'.cgv-genes.tsv', 'w')
    outfile.write(annot_cgv)
    outfile.close()

    outfile = open(prefix +'.cgv-analysis.tsv', 'w')
    outfile.write(mappos)
    outfile.close()

    print('Done!\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n(Terminating due to user interrupt signal)")
