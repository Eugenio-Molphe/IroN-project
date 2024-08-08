Hey!

This is the repository of the bioinformatics part of the IroN research done by ..., and that its results are presented in the following paper: ... . This analysis was done to uncover how the iroN gene is distributed across Enterobacteriaceae, what are the promoters for this gene, and how they are distributed across Enterobacteriaceae and Salmonella sp. We paid especial attention to the promoter ArgR, since we made outstanding discoveries on this promoter in vitro and in vivo systems.

The drawio workflow IroN-project.drawio explains visually the steps we took to make this analysis. But if you prefer to read, here we go:

1. As shown in the diagram, this work flow starts with annotating in Bakta the potential iroN genes (it's not here, it's in other place if you were wondering). Then we double check the Bakta sequences (iron_seqs_enterobacteriaceae.fa) in Kegg to make sure they're what we are looking for (results of this manual annotation: Annotation_75_reference_sequences.tsv). We remove the sequences that didn't make it and use the rest as our reference sequences (To see the original file with all the sequences, go back in time with GitHub).

2. 

To do the next step, we need to create a blastN database, in order to do that, we need to run the following line:
    make_iroN_db.sh fasta_w_reference_sequences output_balstN_db

This is followed by using BlastN to find out who has the gene we are looking for (a file that is a list of species that have it) and the sequences with a certain number of bp flanking our gene. To do tha, you just need to run the following line:
    obtain_iroN_sequences.sh The_path_to_your_genomes Blast__iroN_db Number_bp_flanking_sequences Output_fasta_file