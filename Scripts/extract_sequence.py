"""
Nicolas Naepflin and Eugenio Perez Molphe Montoya
09.05.2024
Extract sequences from fasta file based on blast information
Usage like python extract_sequence.py blast_in seq_in flankingbp out
"""

### Libraries ###

from Bio import SeqIO
from Bio.Seq import Seq
import logging
import sys
import pandas as pd

### Functions ###

def read_fasta_file(fasta_in):
    """
    Read fasta file
    Input: path to fasta file (str)
    Output: dictionary with sequence name as key and sequence as value
    """
    fasta_dict = {}
    fasta_sequences = SeqIO.parse(open(fasta_in),'fasta')
    
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        fasta_dict[name] = sequence
    return fasta_dict

def extract_sequence_from_blast(blast_in, seq_in, flankingbp):
    """
    Extract sequences with lowest evalue from blast file with flankingbp
    Input: blast file (str), sequence file (str), flankingbp (int)
    Output: sequence (str), contig (str), strand (str), flanking_upstream (int), flanking_downstream (int)
    """
    ## setup logging
    logger = logging.getLogger('my logger')

    ## read blast file
    blast = pd.read_csv(blast_in, sep='\t', header=None)
    blast.columns = ['qseqid','sseqid','pident','length','mismatch','gapopen','qstart','qend','sstart','send','evalue','bitscore','sstrand']

    # get hit with lowest evalue
    tophit =  blast.sort_values('evalue').head(1).values[0]

    ## read sequence file
    seq = read_fasta_file(seq_in)

    ## extract sequence with flankingbp
    contig = tophit[1]
    strand = tophit[12]

    # change start and end, depending on strand
    if strand == 'plus':
        start = int(tophit[8])
        end = int(tophit[9])
    else:
        start = int(tophit[9])
        end = int(tophit[8])

    startpos = start - flankingbp
    endpos = end + flankingbp
    
    # get length of sequence
    contig_length = len(seq[tophit[1]])


    # check if start and end are within contig length
    if (startpos < 0) and (endpos < contig_length):
        startpos_new = 0
        endpos_new = endpos

    elif (startpos > 0) and (endpos > contig_length):
        startpos_new = startpos
        endpos_new = contig_length

    elif (startpos < 0) and (endpos > contig_length):
        startpos_new = 0
        endpos_new = contig_length
    else:
        startpos_new = startpos
        endpos_new = endpos

    logging.info(f"{blast_in} - Upstream: {start - startpos_new}. Downstream: {endpos_new - end}")
    seq_to_write = seq[contig][startpos_new:endpos_new]

    # write sequence to output file
    return seq_to_write, contig, strand, start - startpos_new, endpos_new - end

def write_sequence_to_fasta(seq,id,strand,upstream_flank,downstream_flank,out):
    """
    Write sequence to fasta file. If minus strand, reverse complement
    Input: sequence (str), strand (str), id (str), output file (str, appends output file)
    Output: None, writes to fasta file
        >ID total_length upstream_flank downstream_flank
        Sequence
    """
    with open(out, 'a') as f:
        f.write(f'>{id} {len(seq)} {upstream_flank} {downstream_flank}\n')
        if strand == 'minus':
            f.write(f'{str(Seq(seq).reverse_complement())}\n')
        else:
            f.write(f'{seq}\n')



def main():

    ## arguments
    blast_in = sys.argv[1]
    seq_in = sys.argv[2]
    flankingbp = int(sys.argv[3])
    out = sys.argv[4]


    ## logging
    log_file = f"extract_sequences.log"
    
    logging.FileHandler(log_file, mode='a')
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('my logger')
    # print(f'Generate log file {log_file}')


    seq_to_write, contig, strand, upstream_flank, downstream_flank = extract_sequence_from_blast(blast_in, seq_in, flankingbp)
    write_sequence_to_fasta(seq_to_write, contig, strand,upstream_flank, downstream_flank, out)

    print(f'Finished writing sequence from {blast_in} to {out}')


### Main ###

if __name__ == "__main__":

    main()