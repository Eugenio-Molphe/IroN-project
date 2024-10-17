#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 17.10.2024 ####
#### Find immunity genes in Escherichia (mchB, mchI, microcin) ####

# Arguments
EcoliDir=$1 # Directory with the genomes
outputDir=$2 # Output directory

# Function
find_immunity_genes () {
    # Find the immunity genes, and then if found, add the genome name in which they were find into the list.

    # The gene that we are looking for
    local gene=$1

    geneFound=$(grep -i "$gene" "$outputDir"/"$prefix"/"$prefix".gff)
    if [ -z "$geneFound" ]; then
        echo "$gene not found in $prefix"
    else
        echo "$prefix" >> "$outputDir"/"$gene"_list.txt
        echo "mchB found in $prefix"
    fi
}

# Create the output directory
mkdir -p "$outputDir"

# Since I'm dealing with a lot of genomes, I'll loop through them
for genome in "$EcoliDir"/*; do

# Get the name of the genomes to be use as Prokka output directory name and to be annotate in one of those lists
    baseName=$(basename "$genome")
    prefix=$(echo "$baseName" | cut -d'_' -f1-2)
    echo "Processing genome: $prefix"

# Run Prokka
    prokka --outdir "$outputDir"/"$prefix" --prefix "$prefix" "$genome"
    echo "Prokka finished annotating the genomes :D"

# Find the immunity genes, starting by mchB
    find_immunity_genes mchB
# Time to find mchI
    find_immunity_genes mchI
# Finally, let's find microcin
    find_immunity_genes microcin

done