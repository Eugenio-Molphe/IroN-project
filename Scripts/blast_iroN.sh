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
	-evalue 0.001 \
	-max_target_seqs 1000 \
	-outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sstrand" > $out