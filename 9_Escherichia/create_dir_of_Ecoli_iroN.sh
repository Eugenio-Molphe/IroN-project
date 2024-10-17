#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 17.10.2024 ####
#### This script creates a directory for the genomes of Escherichia coli with iroN ####

# Arguments
newDir=$1
dbEcoliIroN=$2
EColiDir=$3


# Create a directory for the genomes of Escherichia coli with iroN if it doesn't exist
if [ ! -d $newDir ]; then
    mkdir $newDir
    echo "Directory $newDir created"
else
    for file in $newDir/*; do
        rm $file
    done
    echo "Directory $newDir emptied"
fi

while IFS= read -r string; do
    # Find and copy files that start with the string
    for file in $EColiDir/*; do
        if [[ $file == *$string* ]]; then
            cp $file $newDir
            echo "File $file copied"
        fi
    done
done < "$dbEcoliIroN"

echo "Files copied to $newDir :D"