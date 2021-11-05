# M5NR annotation

Get the annotations from a list of md5 sequence identifiers. The output is a tsv file.

### Usage:

```python3 m5nr_annotation.py database_name database_file input output```

Example:

```python3 m5nr_annotation.py RefSeq m5nr_refseq.dict input.txt output.tsv```

#### Important:

Before using this script, download the database and unpack it.

Available databases:

- RefSeq (https://drive.google.com/file/d/1hdDHxnlmOXMlYdt3TSMCQbXg6toob255/view?usp=sharing)
- SEED (https://drive.google.com/file/d/1hdDHxnlmOXMlYdt3TSMCQbXg6toob255/view?usp=sharing)
