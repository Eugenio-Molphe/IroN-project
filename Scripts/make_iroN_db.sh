#!/bin/bash

#### Eugenio Perez Molphe Montoya ####
#### 8.05.2024 ####
#### Create our iroN database ####

in=$1
db=$2

echo 'starting makeblastdb'

makeblastdb \
    -in $in \
    -dbtype nucl \
    -out $db

echo 'done, now checking if everything went fine'

blastdbcmd -info -db $db