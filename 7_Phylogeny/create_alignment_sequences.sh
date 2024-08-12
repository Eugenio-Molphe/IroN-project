#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 23.07.2024 ####
#### Create alignment sequences from our Salmonella genomes ####

# Input arguments
in=$1 # Input directory
out=$2 # Output directory (will contain both the alignment and the orf positions)
threads=$3 # Number of CPUs

# Identify the marker genes of my sequence
gtdbtk identify --genome_dir $in --out_dir "$out/Marker_genes" --cpus $threads --force

# Extract the marker genes and align them for a phylogenetic tree
gtdbtk align --identify_dir "$out/Marker_genes" --out_dir "$out/Alignment" --skip_gtdb_refs --cpus $threads