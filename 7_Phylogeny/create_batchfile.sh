#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 23.07.2024 ####
#### Create a batchfile for GTDB-tk (the alignment tool) ####

# Input arguments
pathName=$1
genomesArgR=$2
outputFile=$3

# Function to check if an array contains a value, in this case if the genome of the file is already in the array of genomes with argR
contains() {
    local arr=("$@")
    local value="${arr[-1]}"
    unset 'arr[${#arr[@]}-1]'
    for item in "${arr[@]}"; do
        if [[ "$item" == "$value" ]]; then
            return 0
        fi
    done
    return 1
}

### Main ###
# Let's extract the file name
fileName=$(basename "$pathName")

# Let's extract the genomes name from the file name
genomeName=$(echo $fileName | cut -d '.' -f 1) # awk '{print $0".1"}' # Make an if statement to make look cool

# Read the file with the genomes with argR into a array
mapfile -t genomes < $genomesArgR

# Check if genomeName is in genome_names and append '-argR' if it matches
if contains "${genomes[@]}" "$genomeName"; then
    genomeName="${genomeName}-argR"
fi

# Print the resulting thing
echo "The genome name is: $genomeName"

# Let's create the line for the batchfile
echo "$fileName    $genomeName" >> $outputFile