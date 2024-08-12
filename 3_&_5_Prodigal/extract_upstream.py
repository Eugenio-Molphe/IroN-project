#### Eugenio Perez Molphe Montoya ####
#### 15.05.2024 ####
#### Extract the upstream sequences for further analysis ####

### Load packages ###
import sys
from Bio.Seq import Seq

# Functions made by Nico
sys.path.append('/mnt/mnemo5/eugenio/IroN_project/Scripts/IroN-project/Scripts_BlastN/')
from extract_sequence import read_fasta_file

### Load th arguments ###
fasta = sys.argv[1] # The fasta file with the sequences (400 bp + blasted sequence + 400 bp)
gff = sys.argv[2] # The gff file with the ORFs (Prodigal output)
flankingbp = sys.argv[3] # The number of flanking bp to extract
out = sys.argv[4] # The output

### Functions ###

def get_ORFs(gff_file):
    '''
    Extract the ORFs with the best score per sequence from a gff file
    The output is a dictionary: the key will be sequences name and the values will be a tuple with the start, end, strand and score of the ORF
    '''
    ORFs = {}
    with open(gff_file, 'r') as gff:
        for line in gff:
            if line.startswith("#"):
                continue
            else:
                parts = line.strip().split()
            if parts[2] == "CDS":
                # Get the important features of the ORF and its gene
                seq_id = parts[0]
                start = int(parts[3])
                end = int(parts[4])
                strand = parts[6]
                score = float(parts[5])

                # If the sequence is not in the dictionary, add it
                if seq_id not in ORFs:
                    ORFs[seq_id] = (start, end, strand, score)
                else:
                    # If the sequence is in the dictionary, check if the score is better than the one in the dictionary
                    if score > ORFs[seq_id][3]:
                        ORFs[seq_id] = (start, end, strand, score)
    return ORFs


def extract_upstream(fasta, ORFs, flankingbp, out):
    '''
    Extract the upstream sequences of the genes in the gff file in the following manner:
    1. Read the fasta file as dictionary, the keys will be the sequence names and the values the sequences
    2. Load the ORFs dictionary and extract the upstream sequences of the genes in the gff file
    3. Replace the old sequences with the upstream sequence as the values in the dictionary
    4. Write the upstream sequences to a file
    '''
    # flankingbp is the number of bp to extract upstream of the gene
    # Since it's an argument, it's an string, so let's convert it to an integer
    flankingbp = int(flankingbp)
    
    # Let's transform the fasta file into a dictionary with keys as the sequence names and values as the sequences
    sequences = read_fasta_file(fasta)
    upstream_sequences = {}

    # Extract sequence with flankingbp
    for seq_id, (start, end, strand, score) in ORFs.items():
        # Let's obtain the sequence by first getting the sequence of the gene iroN
        # of the correct genome (this is where loading the sequences as a dict becomes useful)
        # And then replace the old item (seq) of the dictionary with the upstream sequence

        seq = sequences[seq_id]
        if strand == "+":
            # Let's obtain the start and ending of the upstream sequence
            upstream_start = max(0, start - flankingbp - 1)
            upstream_end = start - 1

            upstream_seq = seq[upstream_start:upstream_end]
            upstream_sequences[seq_id] = upstream_seq
        else:
            # Let's obtain the start and ending of the upstream sequence (for negative strands)
            upstream_start = end
            upstream_end = min(len(seq), end + flankingbp)

            upstream_seq = seq[upstream_start:upstream_end]
            
            # Since the sequence is in the negative strand, we need to reverse complement it
            upstream_seq = Seq(upstream_seq).reverse_complement()
            upstream_seq = str(upstream_seq)
            upstream_sequences[seq_id] = upstream_seq
        
        print(seq_id)
        print(upstream_seq)
        print(start, end, strand, score)

        # Write the upstream sequences to a file
        with open(out, 'w') as f:
            for key, value in upstream_sequences.items():
                f.write(f">{key}_upstream_seq\n{value}\n")

### Run the functions ###

# LEt's get the ORFs
if __name__ == "__main__":
    ORFs = get_ORFs(gff)

# And now, let's extract the upstream sequences
extract_upstream(fasta, ORFs, flankingbp, out)