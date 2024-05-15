#### Eugenio Perez Molphe Montoya ####
#### 15.05.2024 ####
#### Extract the upstream sequences for further analysis ####

'''
Disclaimer: this is a raw starting script made by ChatGPT,
I'll check it, debug it (I count that ChatGPT has some errors) and improve it.
And I'll find a way to deal with the cases where we don't have 400 bp upstream.
'''

from Bio import SeqIO

# Load the genome sequence
genome = SeqIO.read("genome.fasta", "fasta")

# Length of upstream sequence to extract
upstream_length = 100

# Parse the GFF file and extract upstream sequences
with open("genome.genes", "r") as gff_file:
    for line in gff_file:
        if line.startswith("#"):
            continue
        parts = line.strip().split("\t")
        if parts[2] == "CDS":
            start = int(parts[3])
            end = int(parts[4])
            strand = parts[6]
            
            if strand == "+":
                upstream_start = max(0, start - upstream_length - 1)
                upstream_end = start - 1
                upstream_seq = genome.seq[upstream_start:upstream_end]
            else:
                upstream_start = end
                upstream_end = min(len(genome.seq), end + upstream_length)
                upstream_seq = genome.seq[upstream_start:upstream_end].reverse_complement()
            
            print(f">upstream_of_{parts[8].split(';')[0].split('=')[1]}\n{upstream_seq}")
