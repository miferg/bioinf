# bioinf
My housekeeping bioinformatics scripts 

## cheatsheet

- make sequential

```bash
awk 'BEGIN{RS=">";FS="\n"}NR>1{seq="";for (i=2;i<=NF;i++) seq=seq""$i; print ">"$1"\n"seq}' $1
```
