# KEGG ontology

Download the kegg ontology from the MG-RAST database and build a table. All commands must be run in the same directory.

1.- Download the ontology using the MG-RAST API:
```
curl -O https://api.mg-rast.org/1/m5nr/ontology?source=KO
```

2.- Rename the downloaded file:
```
mv ontology\?source\=KO kegg_ont.json
```

3.- Run the keggont_table.py script:
```
python3 keggont_table.py
```

The output table will be stored in a file named ko_ont.tsv
