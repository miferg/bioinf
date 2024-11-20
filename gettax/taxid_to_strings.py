#!/usr/bin/env python3

import sys
import os

try:
    namesfile = sys.argv[1]
    nodesfile = sys.argv[2]
    infilename = sys.argv[3]
    outprefix = sys.argv[4]
    
except:
    print("""
Get taxonomy strings from ncbi taxon codes.
Input is a list of tax IDs separated by dashes. Last (or only) should be the most specific.
Needs the names.dmp and nodes.dmp downloaded from NCBI.
Usage:
taxid_to_strings.py names.dmp nodes.dmp INPUT OUTPUT_prefix
    """)
    sys.exit()
    
# FUNCTION DEFINITION

def parse_nodes(nodesfile):
    """Create a dictionary in which each node points to its parent"""
    nodes_dict = {}    # current -> parent, rank
    print('Parsing nodes')
    with open(nodesfile) as infile:
        for line in infile:
            linesep = line.split("\t|\t")
            nodes_dict[linesep[0]] = [linesep[1], linesep[2]]
    return nodes_dict
        
def parse_names(namesfile):
    """Create a dictionary in which each node points to its scientific name"""
    id_2_name = {}    # node -> name, name nr, name class
    print('Parsing names')
    with open(namesfile) as infile:
        for line in infile:
            line = line.split("\t|\n")[0]
            linesep = line.split("\t|\t")
            if linesep[3] == 'scientific name':
                id_2_name[linesep[0]] = [linesep[1], linesep[2], linesep[3]]
    return id_2_name
    
def search_parents(queryid, fullname, nodes_dict, id_2_name):
    """Search for a taxonomy code and return the full taxonomy path"""
    parent = nodes_dict[queryid][0]
    #print(parent)
    if parent == '1':
        fullname = 'root; '+ id_2_name[queryid][0] +'; '+ fullname[:-2]
        #print(fullname)
        return fullname
    else:
        #if nodes_dict[queryid][1] in ['genus', 'family','order','class','phylum','superkingdom']: ### Add this if only standard ranks are required!
        fullname =  id_2_name[queryid][0] +'; '+ fullname
        return search_parents(parent, fullname, nodes_dict, id_2_name)
    
# MAIN PROGRAM

# parse nodes
nodes_dict = parse_nodes(nodesfile)

#parse names
id_2_name = parse_names(namesfile)

print('Extracting strings')

with open(outprefix + '.tax_strings.txt', 'w') as outfile:
    with open(infilename, 'r') as infile:
        for line in infile:
            #print(line.strip())
            lowest = line.strip().split('-')[-1]
            outfile.write(search_parents(lowest, '', nodes_dict, id_2_name) +'\n')
