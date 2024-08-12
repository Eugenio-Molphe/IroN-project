#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 15.05.2024 ####
#### Create the training file for Prodigal ####

input=$1
output=$2 # Extension .trn

prodigal -i $1 -t $2