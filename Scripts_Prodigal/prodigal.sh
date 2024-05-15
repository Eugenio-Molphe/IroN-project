#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 15.05.2024 ####
#### Find the start codon of each gene with Prodigal ####

$fastaInput=$1
$output=$2 # Output file in GFF format
$proteinSequences=$3
$nucleotideSequencesORFs=$4

prodigal -i $fastaInput -o $output -a $proteinSequences -d $nucleotideSequencesORFs -f gff