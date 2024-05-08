#!/bin/bash

#### Nicolas Naepflin and Eugenio Perez Molphe Montoya ####
#### 26.04.2024 and 8.05.2024 ####
#### Blast our sequences against the iroN database ####

in=$1
db=$2
out=$3

blastn \
	-query $in \
	-db $db \
	-evalue  \
	-max_target_seqs 1000 \
	-qcov_hsp_perc 80 \
	-outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sstrand" | awk '$4 > min_length' | awk '$12 > min_bitscore' > $out

# Define evalue, qcov_hsp_perc, min_length, and min_bitscore