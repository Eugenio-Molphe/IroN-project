#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 15.05.2024 ####
#### Find the start codon of each gene with Prodigal ####

fastaInput=$1
training=$2
output=$3 # Output file in GFF format (.gff)

prodigal -i $fastaInput -t $training -o $output -a ${output%.gff}.faa -d ${output%.gff}.fna -f gff