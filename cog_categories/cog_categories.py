# Define dictionaries for COG categories

# highest categories
coghcat_d = {}

for ccat in ['J','A','K','L','B']:
    coghcat_d[ccat] = 'INFORMATION STORAGE AND PROCESSING'
for ccat in ['D','Y','V','T','M','N','Z','W','U','O']:
    coghcat_d[ccat] = 'CELLULAR PROCESSES AND SIGNALING'
for ccat in ['C','G','E','F','H','I','P','Q']:
    coghcat_d[ccat] = 'METABOLISM'
for ccat in ['R','S']:
    coghcat_d[ccat] = 'POORLY CHARACTERIZED'

# specific categories
cogscat_d = {'J': 'Translation, ribosomal structure and biogenesis',
    'A': 'RNA processing and modification',
    'K': 'Transcription',
    'L': 'Replication, recombination and repair',
    'B': 'Chromatin structure and dynamics',
    'D': 'Cell cycle control, cell division, chromosome partitioning',
    'Y': 'Nuclear structure',
    'V': 'Defense mechanisms',
    'T': 'Signal transduction mechanisms',
    'M': 'Cell wall/membrane/envelope biogenesis',
    'N': 'Cell motility',
    'Z': 'Cytoskeleton',
    'W': 'Extracellular structures',
    'U': 'Intracellular trafficking, secretion, and vesicular transport',
    'O': 'Posttranslational modification, protein turnover, chaperones',
    'C': 'Energy production and conversion',
    'G': 'Carbohydrate transport and metabolism',
    'E': 'Amino acid transport and metabolism',
    'F': 'Nucleotide transport and metabolism',
    'H': 'Coenzyme transport and metabolism',
    'I': 'Lipid transport and metabolism',
    'P': 'Inorganic ion transport and metabolism',
    'Q': 'Secondary metabolites biosynthesis, transport and catabolism',
    'R': 'General function prediction only',
    'S': 'Function unknown'}
