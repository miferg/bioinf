#!/usr/bin/env python3
"""
sam-coid
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to create coverage and identity plots.
Usage:
sam-coid.py mapping.sam reference.fasta prefix
"""

import sys
import subprocess

try:
    mapp_name = sys.argv[1]
    genom_name = sys.argv[2]
    prefix = sys.argv[3]

except:
    print("""
sam-coid
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to create coverage and identity plots.
Usage:
sam-coid.py mapping.sam reference.fasta prefix
    """)
    sys.exit()

### Functions

def read_file(filename):
    """open files and save them as a list of lines"""
    handle = open(filename, 'r')
    content = handle.read().split('\n')[:-1]
    handle.close()
    return(content)

def count_contigs(genome):
    """"get the ID of each contig and its size"""
    contigs = {}
    for line in genome:
        if '>' in line:
            current = line[1:].split(' ')[0]
            contigs[current] = 0
        else:
             contigs[current] += len(line)
    return(contigs)

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

def alignment_2_coid(line):
    """split a SAM file and write the position, identity and length of each alignment"""
    md1 = line.split('MD:Z:')
    md = md1[1].split('\t')[0]
    matches, mismatches = parse_MD(md, 0, '', 1, 0)
    linesep = line.split('\t')
    columns = [linesep[2], linesep[3],str(matches/(matches + mismatches)), str(matches + mismatches)]
    return('\t'.join(columns) +'\n')

def rscript_mapposrel(prefix):
    """build the R script to generate the plots"""
    script = """
options(scipen=5)
coid <- read.table('"""+ prefix +""".coid.tsv', sep='\t', header=T)
contigs <- read.table('"""+ prefix +""".contigs.tsv', sep='\t', header=T)
for (i in 1:length(levels(coid$ref))) {
 current <- levels(coid$ref)[i]
 print(current)
 iddf <- coid[coid$ref == current,]
 seqlen <- as.integer(contigs[contigs$contig==current,][2])
 if (seqlen/10000 >= mean(coid$length)){
  barnum <- 10000
 } else {
  barnum <- round(seqlen/mean(coid$length)) + 1
 }
 classlen <- as.integer(round(seqlen/barnum))
 reference <- seq(1,as.integer(seqlen),as.integer(classlen))
 abundance <- as.integer(lapply(reference, function(x) { dim(subset(iddf,pos>=x & pos<=(x+classlen)))[1]}))
 abdf <- data.frame(reference,abundance)
 outfilename <- paste('"""+ prefix +"""',current,'coid.pdf', sep='.')
 pdf(outfilename)
 par(mfrow=c(2,1), mar=c(2,3,2,1))
 plot(abdf, type='l', xlim = c(0, seqlen), main='"""+ prefix +"""')
 par(mar=c(5,3,1,1))
 plot(id~pos, data=iddf, ylim = c(0.5,1), xlim = c(0, seqlen), xlab=current, pch='.')
 dev.off()
}
    """
    return(script)

### Main program

def main():

    print("""
sam-coid
Miguel F. Romero, 2021
github.com/miferg
Format genomic mapping information to create coverage and identity plots.
""")

    print(' '.join(sys.argv) +'\n')

    print('Loading files.\n')
    genom, sam = map(read_file, (genom_name, mapp_name))
    
    print('Parsing alignments.\n')
    outlist = ''.join((map(alignment_2_coid, sam)))
    
    print('Counting contig sizes.\n')
    contigs = count_contigs(genom)

    print('Creating R script.\n')
    rscript = rscript_mapposrel(prefix)

    outfile = open(prefix +'.coid.R', 'w')
    outfile.write(rscript)
    outfile.close()

    print('Writing output files.\n')
    outfile = open(prefix +'.coid.tsv', 'w')
    outfile.write('ref\tpos\tid\tlength\n')
    outfile.write(outlist)
    outfile.close()
    
    outfile = open(prefix +'.contigs.tsv', 'w')
    outfile.write('contig\tsize\n')
    for key in contigs.keys():
        line = key +'\t'+ str(contigs[key]) +'\n'
        outfile.write(line)
    outfile.close()

    print('Running R script.\n')
    command = ["Rscript", prefix +'.coid.R']
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if output.returncode != 0:
        print('Error:')
        print(output.stderr)
        sys.exit()

    print('Done!\n')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n(Terminating due to user interrupt signal)")
