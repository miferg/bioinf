infilename = 'filenames'
handle = open(infilename,'r')
files = handle.read().split('\n')[:-1]
handle.close()

edge_list = []

# load all files and make a list of bbh pairs of tuples (edges)
# each touple has the database and sequence
for filename in files:
    handle = open(filename,'r')
    bbh_list = handle.read().split('\n')[:-1]
    dbs = filename.split('-')
    for line in bbh_list:
        pair = line.split('\t')
        edge_list.append([(dbs[0],pair[0]),(dbs[1],pair[1])])
    #print(edge_list)

print(edge_list)

# EdgeSearch algorithm
i = 0
while i < len(edge_list):
    seed = edge_list[0]
    print('seed:')
    print(seed)
    edge_list = edge_list[1:]
    output = [seed]
    ii = 0
    while ii < len(edge_list):
        subject = edge_list[ii]
        print('subject:')
        print(subject)
        for vertex in seed:
            if vertex in subject:
                print('success')
                output.append(edge_list.pop(ii))
                seed = seed+subject
                seed = list(set(seed))
                ii += -1
                break
        ii += 1
    i += 1
    print('output:')
    print(output)
