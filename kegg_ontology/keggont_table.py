import json

handle = open('kegg_ont.json','r')
json_raw = handle.read()
handle.close()

json_string = json.loads(json_raw)
ko_json = json_string['data']

fail = []
ko_dict = {}

print('Parsing data.')

for ko in ko_json:
    try:
        ko_dict[ko['accession']] = [ko['level1'],ko['level2'],ko['level3'],ko['level4']]
    except:
        fail.append(ko)

if len(fail) > 0:
    print('There were '+ str(len(fail)) +' errors. Check that all accessions have four levels.')

print('Writing table')

outfile = open('ko_ont.tsv','w')
foo = outfile.write('KO\tlevel1\tlevel2\tlevel3\tlevel4\n')

for key in list(ko_dict.keys()):
    foo = outfile.write(key +'\t'+ '\t'.join(ko_dict[key]) +'\n')

outfile.close()
print('Done!')
