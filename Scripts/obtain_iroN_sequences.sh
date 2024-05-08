#!/bin/bash

#### Nicolas Naepflin and Eugenio Perez Molphe Montoya ####
#### 26.04.2024 and 8.05.2024 ####
#### Extract the annotated sequences by blasting against our IroN db ####

# The genomes' path ($1 in blast_iroN.sh and $2 in extract_iroN.sh) are hardcoded

in=$1 # Path to the genomes, forget about the last /
db=$2 # Path to the IroN db, forget about the last /
flankingbp=$3 # Number of flanking base pairs to extract
out=$4 # Path to the output fasta file

# Let's find the IroN genes with BlastN

parallel -j8 bash scripts/blast_iroN.sh {} \ 
                $db \
	            out/iron_blast/{/.}.blast.tsv ::: $in/*

# Let's extract the sequences
parallel -j1 bash scripts/extract_sequence.sh \
				out/iron_blast/{/.}.blast.tsv {} $flankingbp \
				$out ::: $in/*.fna

# Let's extract a list of the genomes that have IroN genes
sed -n 's/^>\([0-9]*\)_.*$/\1/p' $out > Taxonomy_identity_numbers.txt