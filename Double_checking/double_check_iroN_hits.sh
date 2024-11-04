#!/bin/bash

### Eugenio Perez Molphe Montoya & Nicolas Naepflin ###
### 31.10.2024 ###
### This script is used to double check the hits of the iroN gene in the genomes of the strains of interest ###
### Originally, we just did it on the fly in the command line ###

in=$1  # input query sequences (FASTA format .faa)
out=$2 # List of best hits per query

# create mmseqs sequence database
mmseqs createdb $in inDB

# search against reference database nrDB
mmseqs search inDB /mnt/mnemo6/nnaepf/databases/mmseqs_nr/nr resultDB tmpSalmo --start-sens 1 --sens-steps 3 -s 7 --max-accept 10000 --threads 64

# convert into tabular format
mmseqs convertalis inDB /mnt/mnemo6/nnaepf/databases/mmseqs_nr/nr resultDB resultDB.blast --threads 64 --format-output "query,target,evalue,bits,pident,nident,alnlen,mismatch,qstart,qend,tstart,tend,theader"

# keep best hit per query based on bitscore
awk -F' ' '{if ($1 in arr){split(arr[$1],x," "); if(x[4] < $4) arr[$1] = $0} else{arr[$1] = $0}}END{for (i in arr) print arr[i]}' resultDB.blast > $out