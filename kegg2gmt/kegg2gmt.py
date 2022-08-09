"""
Reformat the KEGG orthology htext to gmt. Can be used to perform a GSEA.
https://github.com/miferg/bioinf
"""

def main():
    kdict = {}

    with open('ko00001.keg') as f:
        for i in f:
            isep = i.split("\t")
            ko = isep[-1].split()[0]
            if isep[2] not in kdcit.keys():
                kdict[isep[2]] = []
                kdict[isep[2]].append(ko)
            else:
                kdict[isep[2]].append(ko)
            
    outfile = open('kegg.gmt', 'w')

    for i in kdict.keys():
        text = i +'\t'+ i + '\t' + '\t'.join(kdict[i]) + '\n'
        outfile.write(text)
    
    outfile.close()
    return 0

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n(Terminating due to user interrupt signal)")
