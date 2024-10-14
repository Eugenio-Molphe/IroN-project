#### Eugenio Perez Molphe Montoya ####
#### 30.05.2024 ####
#### So BProm expects one sequence, so I should make a directory and 
# divide my usptream sequence fasta file into a lot of smaller fasta files 
# with only one sequence per file  ####

# Import packages and functions
import os
import sys

# Functions made by Nico
sys.path.append('/mnt/mnemo5/eugenio/IroN_project/Scripts/IroN-project/2_BlastN/')
from extract_sequence import read_fasta_file

# Define the path to the fasta file
fasta = sys.argv[1] # The fasta file with the upstream sequences
outputDir = sys.argv[2] # The output directory

# Read the fasta file
sequences = read_fasta_file(fasta)

# Create the output directory
os.makedirs(outputDir, exist_ok=True)

# Write the sequences to the output directory
for seq_id, seq in sequences.items():
    with open(f"{outputDir}/{seq_id}.fa", "w") as out:
        out.write(f">{seq_id}\n{seq}\n")

print('Done :D')