#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def greet():
    print(
    """
    Get a taxonomy table from a list of species names
    usage: python3 gettax.py
    Miguel Romero github.com/romeromig
    """
    )
    sys.exit()

def read_lines(filename):
    handle = open(filename,'r')
    linelist = handle.read().split('\n')[:-1]
    handle.close()
    return linelist

def main():

    if len(sys.argv[1:]) == 0:
        greet()

    # load the input file
    spfilename = sys.argv[1]
    species = read_lines(spfilename)

    print('Loading database.')
    # load node file
    nodesraw = read_lines('nodes.dmp')

    # each taxid points to its parental node
    nodesdict = {}
    for line in nodesraw:
        linesep = line.split('\t|\t')
        nodesdict[linesep[0]] = linesep[1]

    # scientific name file
    namesraw = read_lines('scnames.dmp')

    # each name points to its taxid
    namesdict = {}
    for line in namesraw:
        linesep = line.split('\t|\t')
        namesdict[linesep[1]] = linesep[0]

    # create dictionaries for each rank
    phylaraw = read_lines('nn_phyla.txt')

    phyladict = {}
    for line in phylaraw:
        linesep = line.split('\t')
        phyladict[linesep[0]] = linesep[1]

    classraw = read_lines('nn_class.txt')

    classdict = {}
    for line in classraw:
        linesep = line.split('\t')
        classdict[linesep[0]] = linesep[1]

    ordraw = read_lines('nn_order.txt')

    orddict = {}
    for line in ordraw:
        linesep = line.split('\t')
        orddict[linesep[0]] = linesep[1]

    famraw = read_lines('nn_family.txt')

    famdict = {}
    for line in famraw:
        linesep = line.split('\t')
        famdict[linesep[0]] = linesep[1]


    # correct troublesome names
    namesdict['Aster yellows witches-broom phytoplasma'] = '322098'
    namesdict['Blochmannia endosymbiont of Camponotus Colobopsis obliquus'] = '1505597'
    namesdict['Blochmannia endosymbiont of Polyrhachis Hedomyrma turneri'] = '1505596'
    namesdict['Didymococcus colitermitum'] = '278957'
    namesdict['endosymbiont TC1 of Trimyema compressum'] = '243899'
    namesdict['Haloplasma contractile'] = '1033810'
    namesdict['Kinetoplastibacterium blastocrithidii'] = '233181'
    namesdict['Massiliomicrobiota timonensis'] = '1776392'
    namesdict['Monashia flava'] = '1428657'
    namesdict['Oceanibulbus indolifex'] = '391624'
    namesdict['Peanut witches-broom phytoplasma'] = '1163385'
    namesdict['Spongiibacterium flavum'] = '570519'
    namesdict['Thermobaculum terrenum'] = '525904'
    namesdict['Thiobacimonas profunda'] = '1229727'
    namesdict['Turicella otitidis'] = '883169'
    namesdict['Xuhuaishuia manganoxidans'] = '1267768'
    namesdict['Bacillus clarkii'] = '79879'
    namesdict['Bacillus selenitireducens'] = '439292'
    namesdict['Bacillus xerothermodurans'] = '1977292'

    # search names in ncbi
    print('Searching names')
    error = [] # view species in list but not in ncbi names
    taxiddict = {}
    for spec in species:
        sp = spec
        sp = ' '.join(sp.split('_'))
        try:                             # if the species is absent, look for the genus
            node = namesdict[sp]
        except:
            try :
                sp = sp.split(' ')[0]
                node = namesdict[sp]
            except :
                error.append(spec)
                pass
        taxch = [node]
        while node != '1':
            node = nodesdict[node]
            taxch.append(node)
        taxiddict[spec] = taxch
    #print(error)

    # create the taxonomy dictionary
    print('Merging taxonomy')
    taxdict = {}
    for spec in list(taxiddict.keys()):
        taxdict[spec] = {}
        for taxid in taxiddict[spec]:
            if taxid in list(phyladict.keys()):
                taxdict[spec]['phy'] = phyladict[taxid]
                # print (taxdict[spec]['phy'])
            if taxid in list(classdict.keys()):
                taxdict[spec]['class'] = classdict[taxid]
                # print (taxdict[spec]['class'])
            if taxid in list(orddict.keys()):
                taxdict[spec]['ord'] = orddict[taxid]
                # print (taxdict[spec]['ord'])
            if taxid in list(famdict.keys()):
                taxdict[spec]['fam'] = famdict[taxid]
                # print (taxdict[spec]['fam'])



    # correct tax dict for unassigned categories
    print('Generating dummy categories')
    check = ''
    categories = ['phy','class','ord','fam']
    for spec in species:
        for cat in categories:
            try:
                check = taxdict[spec][cat]
            except:
                try:
                    taxdict[spec][cat] = 'undef_'+ cat +'_'+ taxdict[spec]['phy']
                except:
                    taxdict[spec]['phy'] = 'unclassified'
                    taxdict[spec][cat] = 'undef_'+ cat +'_'+ taxdict[spec]['phy']

    print('Writing to '+ spfilename +'.tax.tsv')
    outfile = open(spfilename +'.tax.tsv','w')
    error = [] # view species with errors
    for spec in species:
        try:
            outfile.write(spec+'\t'+taxdict[spec]['phy']+'\t'+taxdict[spec]['class']+'\t'+taxdict[spec]['ord']+'\t'+taxdict[spec]['fam']+'\t'+'\n')
        except:
            error.append(spec)
    #print(error)
    outfile.close()

    print('Done!')

if __name__ == '__main__':
    main()
