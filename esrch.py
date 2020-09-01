infilename = 'filenames'
handle = open(infilename,'r')
files = handle.read().split('\n')[:-1]
handle.close()

edge_list = []

# load all files and make a list of bbh pairs of tuples (edges)
# each touple has the database and peptide
for filename in files:
    handle = open(filename,'r')
    bbh_list = handle.read().split('\n')[:-1]
    dbs = filename.split('-')
    for line in bbh_list:
        pair = line.split('\t')
        edge_list.append([(dbs[0],pair[0]),(dbs[1],pair[1])])
    #print(edge_list)

print(edge_list)

# EdgeSearch algorythm
i = 0
while i < len(edge_list):
    seed = edge_list[0]
    edge_list = edge_list[1:]
    output = [seed]
    ii = 0
    while ii < len(edge_list):
        subject = edge_list[ii]
        if seed[0] in subject or seed[1] in subject:
            output.append(edge_list.pop(ii))
            ii += -1
        ii += 1
    i += 1
    print(output)
