#!/bin/bash

#### Nicolas Naepflin and Eugenio Perez Molphe Montoya ####
#### 26.04.2024 and 8.05.2024 ####
#### Extract the annotated sequences by blasting against our IroN db ####

blastin=$1
seqin=$2
flankingbp=$3
out=$4

# sort file and obtain seq with lowest  e-value

tophit=$(sort -n -k10 $blastin | head -n1)

# get sequence

while IFS=$'\t' read -r qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore sstrand; do
	if [[ "$sstrand" == "plus" ]]; then
		startpos=$((sstart-flankingbp))
		endpos=$((send+flankingbp))	
		echo $startpos
		echo $endpos
		# get sequence
		seqkit seq -w0 $seqin | grep -A1 "${sseqid}$" | seqkit subseq -r "$startpos":"$endpos" | seqkit seq -w0 >> ${out}
	elif [[ "$sstrand" == "minus" ]]; then
		startpos=$((send-flankingbp))
		endpos=$((sstart+flankingbp))
		
		# get reverse complement
		seqkit seq -w0 $seqin | grep -A1 "${sseqid}$" | seqkit subseq -r "$startpos":"$endpos" | seqkit seq -w0 --quiet -r -p -t dna >> ${out}
	else
		echo "Failed, unknown value for sstrand: ${sstrand}"
	fi
done <<< "$tophit"