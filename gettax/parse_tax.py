nodes_dict = {}

with open('nodes.dmp') as infile:
    for line in infile:
        linesep = line.split("\t|\t")
        nodes_dict[linesep[0]] = [linesep[1], linesep[2]]
        
# current -> parent, rank

name_2_id = {}
id_2_name = {}

with open('names.dmp') as infile:
    for line in infile:
        line = line.split("\t|\n")[0]
        linesep = line.split("\t|\t")
        name_2_id[linesep[1]] = [linesep[0], linesep[2], linesep[3]]
        if linesep[3] == 'scientific name':
            id_2_name[linesep[0]] = [linesep[1], linesep[2], linesep[3]]
        
# name ->> node, name nr, name class
# node -> name, name nr, name class


def search_parents(name, fullname):
    queryid = name_2_id[name][0]
    if nodes_dict[queryid][1] in ['genus', 'family','order','class','phylum','superkingdom']:
        fullname =  id_2_name[queryid][0] +'|'+ fullname
    parent = nodes_dict[queryid][0]
    if parent == '1':
        return fullname[:-1]
    else:
        print(id_2_name[parent][0])
        return search_parents(id_2_name[parent][0], fullname)
      
# PURGE FOR EUKS 

euk_nodes_dict = {}
euk_name_2_id = {}
euk_id_2_name = {}

for node in nodes_dict.keys():
    if 'Eukaryota' in search_parents(node, ''):
        while node != '1':
            euk_nodes_dict[node] = nodes_dict[node]
            euk_id_2_name[node] = id_2_name[node]
            euk_name_2_id[euk_id_2_name[node][0]] = node
            node = nodes_dict[node][0]
            
