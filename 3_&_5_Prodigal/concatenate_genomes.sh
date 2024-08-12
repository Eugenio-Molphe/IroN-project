#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 17.05.2024 ####
#### Concatenate 10 random genomes to create the input for create_training_file.sh ####

dir=$1
seed=69 # I hardcoded the seed
output=$2

# Let's create a function that provided a seeded random source for shuf
get_seeded_random() {
    seed="$1"
    openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt </dev/zero 2>/dev/null
}

# List the files in the directory and shuffle them with the seed
ls "$dir" | shuf --random-source=<(get_seeded_random "$seed") | head -n 10 | xargs -I {} cat $dir/{} >> "$output"