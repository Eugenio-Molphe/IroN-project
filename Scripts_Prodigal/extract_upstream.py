#### Eugenio Perez Molphe Montoya ####
#### 15.05.2024 ####
#### Extract the upstream sequences for further analysis ####

### Load packages ###
import sys

# Functions made by Nico
sys.path.append('/mnt/mnemo5/eugenio/IroN_project/Scripts/IroN-project/Scripts_BlastN/')
from extract_sequence import read_fasta_file

### Load th arguments ###
fasta = sys.argv[1]
gff = sys.argv[2]
flankingbp = sys.argv[3]
out = sys.argv[4]

### Functions ###

def extract_upstream(fasta, gff_file, flankingbp, out):
    '''
    Extract the upstream sequences of the genes in the gff file in the following manner:
    1. Read the fasta file as dictionary, the keys will be the seqeunce names and the values the sequences
    2. Read the gff file and extract the upstream sequences of the genes in the gff file
    3. Replace the old sequences with the upstream sequence as the values in the dictionary
    4. Write the upstream sequences to a file
    '''
    # Read blasta file
    sequences = read_fasta_file(fasta)

    # Extract sequence with flankingbp
    with open(gff, 'r') as gff_file:
        for line in gff_file:
            if line.startswith("#"):
                continue
            else:
                # Here I obtain the characteristics of the ORFs of each sequence
                parts = line.strip().split()
                if parts[2] == "CDS":
                    # Time to get the important features of the ORF and its gene
                    start = int(parts[3]) # The start of the gene iroN sequence
                    end = int(parts[4]) # The end of the gene iroN sequence
                    strand = parts[6] # If the strand is + or -

                    if strand == "+":
                        # Let's obtain the start and ending of the upstream sequence
                        upstream_start = max(0, start - flankingbp - 1)
                        upstream_end = start - 1

                        # Let's obtain the sequence by first getting the sequence of the gene iroN
                        # of the correct genome (this is where loading the sequences as a dict becomes useful)
                        # And then replace the old item (seq) of the dictionary with the upstream sequence
                        seq = sequences[parts[0]]
                        upstream_seq = seq[upstream_start:upstream_end]
                        sequences[parts[0]] = upstream_seq
                    else:
                        # Let's obtain the start and ending of the upstream sequence (for negative strands)
                        upstream_start = end
                        upstream_end = min(len(seq), end + flankingbp)

                        # Let's obtain the sequence by first getting the sequence of the gene iroN
                        # of the correct genome (this is where loading the sequences as a dict becomes useful)
                        # And then replace the old item (seq) of the dictionary with the upstream sequence
                        seq = sequences[parts[0]]
                        upstream_seq = seq[upstream_start:upstream_end].reverse_complement()
                        sequences[parts[0]] = upstream_seq
        
        # Write the upstream sequences to a file
        with open(out, 'w') as f:
            for key, value in sequences.items():
                f.write(f">{key}_upstream_seq\n{value}")
