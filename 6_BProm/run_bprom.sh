#### Eugenio Perez Molphe Montoya ####
#### 25.06.2024 ####
#### This script allows me to use BProm for my files ####

# Arguments

inputDir=$1
outputDir=$2

# Run BProm

echo "BProm is running, please wait..."
for file in $inputDir/*; do
    filename=$(basename $file)
    name=${filename%.*}
    echo "Processing $name"
    /mnt/mnemo5/eugenio/IroN_project/bprom/bprom $file $outputDir/$name.out
done
echo "BProm has finished, how cute!"

# Now let's create a file with the overall results
