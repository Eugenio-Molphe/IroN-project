#### Eugenio Perez Molphe Montoya ####
#### 25.06.2024 ####
#### This script allows me to use BProm for my files ####

# Arguments

inputDir=$1
outputDir=$2
threads=$3

# Run BProm

echo "BProm is running, please wait..."
parallel -j$threads bash /mnt/mnemo5/eugenio/IroN_project/bprom/bprom {} $outputDir/{/.}.out ::: $inputDir/*
echo "BProm has finished, how cute!"

# Now let's create a file with the overall results
