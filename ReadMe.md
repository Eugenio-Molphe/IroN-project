Hey!

This is the repository of the bioinformatics part of the IroN research done by ..., and that its results are presented in the following paper: ... . This analysis was done to uncover how the iroN gene is distributed across Enterobacteriaceae, what are the promoters for this gene, and how they are distributed across Enterobacteriaceae and Salmonella sp. We paid especial attention to the promoter ArgR, since we made outstanding discoveries on this promoter in vitro and in vivo systems.

The drawio workflow IroN-project.drawio explains visually the steps we took to make this analysis. But if you prefer to read, here we go:

1. As shown in the diagram, this work flow starts with annotating in Bakta the potential iroN genes (it's not here, it's in other place if you were wondering). Then we double check the Bakta sequences (iron_seqs_enterobacteriaceae.fa) in Kegg to make sure they're what we are looking for (results of this manual annotation: Annotation_75_reference_sequences.tsv). We remove the sequences that didn't make it and use the rest as our reference sequences (To see the original file with all the sequences, go back in time with GitHub) [The scripts for this are in the repository for the analysis of Cherrak et al (in press)].

2. BlastN: To do the next step, we needed to create a blastN databasee, in order to do that, we need to run the following script: make_iroN_db.sh.
This is followed by using BlastN to find out who has the gene we are looking for (a file that is a list of species that have it) and the sequences with a certain number of bp flanking our hit. To do thay, we need to run the following script: obtain_iroN_sequences.sh

3. and 5. Prodigal: Later, we needed to find the start codon in each hit + upstream and downstream bp for the following steps. We needed to train Prodigal with a customized training file, this training file was created based on a series of Salmonella concatenated genomes with the script: concatenate_genomes.sh. The training file was created with: create_training_file.sh. Then, we used Prodigal to find it with the following script: prodigal.sh. We then extracted the upstream sequences with the script: extract_upstream.py, and then we removed the upstream sequences with <40 bp with the script: trimm_upstream_sequences.ipynb.

4. We verified the iroN hits with BlastN against the NR db and preserved only the ones with a verified iroN sequence [The scripts for this are in the repository for the analysis of Cherrak et al (in press)].

6. BProm: we used BProm to annotate the putative promoters in each iroN hit. To do that, we needed to get one fasta file per upstream sequence with the script: get_one_seq_per_file.py. Then two attempts were made, the first one by using the online version of BProm with the script BProm.py. It didn't work: there was a limit in samples analysed per day, it would take a long time, so we decided to purchase the software. The script that we used to get the promoters with the software installed in the server/local computer was: run_bprom.sh. We removed the result reports of the iroN hits that had no detected promoters with: trimm_bprom_results.py. And finally we created a presense-absence summary dataframe of the promoters found in each genome with: create_presence_absence_df_promoters.py.

7. Phylogeny: we made a small phylogenetic analysis with GTDBtk and RAxML-NG to see if there's a phylogenetic signal for the presence of the ArgR promoter in Salmonella. The batchfile for the alignment sequence was created by: create_batchfile.sh, and the alignment sequence was created with create_alignment_sequences.sh. RAxML was run on the fly in the terminal, the log file contains the parameters that we used.

8. To get the results, we needed to create a file with the taxonomic codes and taxonomic names of the Salmonella genomes with the help of get_taxonomic_codes_salmonella.ipynb. We then used those codes and the ones of Enterobacteriaceae alongside with our results to make summary tables of precentage of genomes with iroN hits per genus and percentage of genomes with certain promoter per genus, and their respective graphs with: get_taxonomic_information_and_figures.ipynb. The script that we used to get different graphs that visualized different aspects of the data like a histogram of the precentage identity in the iroN hits was get_methodological_data.ipynb.



References

Alexey M. Kozlov, Diego Darriba, Tomáš Flouri, Benoit Morel, and Alexandros Stamatakis (2019) RAxML-NG: A fast, scalable, and user-friendly tool for maximum likelihood phylogenetic inference. Bioinformatics, 35 (21), 4453-4455 doi:10.1093/bioinformatics/btz305

Altschul, S. F., Gish, W., Miller, W., Myers, E. W., & Lipman, D. J. (1990). Basic local alignment search tool. Journal of Molecular Biology, 215(3), 403–410. https://doi.org/10.1016/S0022-2836(05)80360-2

Chaumeil PA, et al. 2022. GTDB-Tk2: memory friendly classification with the genome taxonomy database. Bioinformatics, btac672.

Chaumeil PA, et al. 2019. GTDB-Tk: A toolkit to classify genomes with the Genome Taxonomy Database. Bioinformatics, btz848.

Cherrak et al. 2024. Non-canonical start codons confer competitive advantage in carbohydrate
utilization for commensal E. coli in the murine gut. In press

Fullam, A., Letunic, I., Schmidt, T. S. B., Ducarmon, Q. R., Karcher, N., Khedkar, S., Kuhn, M., Larralde, M., Maistrenko, O. M., Malfertheiner, L., Milanese, A., Rodrigues, J. F. M., Sanchis-López, C., Schudoma, C., Szklarczyk, D., Sunagawa, S., Zeller, G., Huerta-Cepas, J., von Mering, C., … Mende, D. R. (2023). proGenomes3: Approaching one million accurately and consistently annotated high-quality prokaryotic genomes. Nucleic Acids Research, 51(D1), D760–D766. https://doi.org/10.1093/nar/gkac1078

Hyatt, D., Chen, G.-L., LoCascio, P. F., Land, M. L., Larimer, F. W., & Hauser, L. J. (2010). Prodigal: Prokaryotic gene recognition and translation initiation site identification. BMC Bioinformatics, 11(1), 119. https://doi.org/10.1186/1471-2105-11-119

Schwengers, O., Jelonek, L., Dieckmann, M. A., Beyvers, S., Blom, J., & Goesmann, A. (2021). Bakta: Rapid and standardized annotation of bacterial genomes via alignment-free sequence identification: Find out more about Bakta, the motivation, challenges and applications, here. Microbial Genomics, 7(11). https://doi.org/10.1099/mgen.0.000685