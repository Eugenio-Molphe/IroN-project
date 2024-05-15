#!/bin/bash

#### Nicolas Naepflin and Eugenio Perez Molphe Montoya ####
#### 26.04.2024 and 8.05.2024 ####
#### Extract the annotated sequences by blasting against our IroN db ####

# The genomes' path ($1 in blast_iroN.sh and $2 in extract_iroN.sh) are hardcoded

in=$1 # Path to the genomes, forget about the last /
db=$2 # Path to the IroN db, forget about the last /
flankingbp=$3 # Number of flanking base pairs to extract
out=$4 # Path to the output fasta file (extension fa)

# Let's find the IroN genes with BlastN

parallel -j8 bash Scripts/blast_iroN.sh {} \
$db \
/mnt/mnemo5/eugenio/IroN_project/Files/02_iron_blast/{/.}.blast.tsv ::: $in/*

# Let's extract the sequences
parallel -j1 python Scripts/extract_sequence.py \
/mnt/mnemo5/eugenio/IroN_project/Files/02_iron_blast/{/.}.blast.tsv {} $flankingbp \
$out ::: $in/*

# Let's extract a list of the genomes that have IroN genes
grep -oP '(?<=\>)[0-9]+(?=\.)' $out > ${out%.fa}.taxonomy_identity_numbers.txt
