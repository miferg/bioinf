#!/usr/bin/env python3

"""
Miguel F. Romero, 2021
github.com/miferg
cgv_build.py formats genomic mapping information to be read by the CGView software.
Requires R >= 3
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
Miguel F. Romero, 2021
github.com/miferg
cgv_build.py formats genomic mapping information to be read by the CGView software.
Usage:
cgv_build.py genomic.fna annotation.gff mapping.sam prefix
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
    complete = ''
    for line in genome:
        if '>' in line:
            current = line[1:].split(' ')[0]
            contigs[current] = len(complete)
        else:
            complete += line
    return(contigs, complete)

def format_gff(gff, contigs):
    """get the desired annotations with the new coordinates"""
    annot_cgv = 'name\ttype\tstart\tstop\tstrand\n'
    for line in gff:
        if line[0] != '#':
            linesep = line.split('\t')
            if linesep[2] in ('CDS','tRNA','rRNA'):
                annotation = []
                annotation.append(linesep[8].split(';')[0][3:])
                annotation.append(linesep[2])
                annotation.append(str(contigs[linesep[0]] + int(linesep[3])))
                annotation.append(str(contigs[linesep[0]] + int(linesep[4])))
                annotation.append(linesep[6])
                annot_cgv += '\t'.join(annotation) + '\n'
    return(annot_cgv)

def get_mappos(sam, contigs):
    """get the corrected mapping positions"""
    mappos = ''
    for line in sam:
        linesep = line.split('\t')
        mappos += str(contigs[linesep[2]] + int(linesep[3])) +'\n'
    return(mappos)

def rscript_mapposrel(prefix, complete, barnum):
    script = """
hits <- read.table('"""+ prefix +""".mappos.txt', header = F)
barnum <- """+ str(barnum) +"""
seqlen <- """+ str(len(complete)) +"""
classlen <- round(seqlen/barnum)
reference <- seq(1,seqlen,classlen)
abundance <- as.integer(lapply(reference, function(x) { dim(subset(hits,V1>=x & V1<=(x+classlen)))[1]}))
df <- data.frame(reference,abundance)
png('"""+ prefix +""".mappos.png')
plot(df, type='l', main='"""+ prefix +"""')
dev.off()
df.rel <- df
colnames(df.rel) <- c('start','score')
df.rel$score <- df.rel$score/max(df.rel$score)
write.table(df.rel, file='"""+ prefix +""".mapposrel.tsv', sep = '\\t', row.names = F)
    """
    return(script)

### main script

def main():

    print("""
Miguel F. Romero, 2021
github.com/miferg
cgv_build.py
    """)
  
    print('Loading files.\n')
    genom, annot, mapp = map(read_file, (genom_name, annot_name, mapp_name))

    print('Counting contig sizes.\n')
    contigs, complete_genome = count_contigs(genom)

    print('Building new annotation.\n')
    annot_cgv = format_gff(annot, contigs)

    print('Getting new mapping positions.\n')
    mappos = get_mappos(mapp, contigs)

    print('Creating R script.\n')
    rscript = rscript_mapposrel(prefix, complete_genome, 5000)

    print('Writing output files.\n')

    outfile = open(prefix +'.mappos.R', 'w')
    outfile.write(rscript)
    outfile.close()

    outfile = open(prefix +'.cgv_gff.tsv', 'w')
    outfile.write(annot_cgv)
    outfile.close()

    outfile = open(prefix +'.complete.fna', 'w')
    outfile.write('>'+ prefix +'\n')
    outfile.write(complete_genome +'\n')
    outfile.close()

    outfile = open(prefix +'.mappos.txt', 'w')
    outfile.write(mappos)
    outfile.close()

    print('Running R script.\n')
    command = ["Rscript", prefix +'.mappos.R']
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if output.returncode != 0:
        print('Error:')
        print(output.stderr)
        sys.exit()

    print('Done!.\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n(Terminating due to user interrupt signal)")

