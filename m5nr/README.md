# M5NR annotation

Get the annotations from a list of md5 sequence identifiers. The output is a tsv file.

### Usage:

```python3 m5nr_annotation.py database_file input output_prefix```

Example:

```python3 m5nr_annotation.py m5nr_refseq.dict input.txt input```

The name of the output table would be `input.RefSeq.tsv`

#### Important:

Before using this script, download the database and unpack it.

Available databases:

- GenBank (https://drive.google.com/file/d/1Yv2bEQlke0okkx6tsCOCfnNyLSuUmM_v/view?usp=sharing)
- RefSeq (https://drive.google.com/file/d/1hdDHxnlmOXMlYdt3TSMCQbXg6toob255/view?usp=sharing)
- SEED (https://drive.google.com/file/d/1hdDHxnlmOXMlYdt3TSMCQbXg6toob255/view?usp=sharing)
- KEGG GENES (https://drive.google.com/file/d/1IrDR8oDxbA7Umfbb0DDfQItsNBQZShoG/view?usp=sharing)
- COG (https://drive.google.com/file/d/1ilqd8pYP9yxnGdkPeGLlr_CSpibp_GlS/view?usp=sharing)
