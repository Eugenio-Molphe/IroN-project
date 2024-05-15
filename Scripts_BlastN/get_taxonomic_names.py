#### Eugenio Perez Molphe Montoya ####
#### 14.05.2024 ####
#### Get a list of taxopnomic names for our bacteria ####

### Libraries ###
import sys

### Arguments ###
wholeTax = sys.argv[1] # The file with the taxonomy of all our Enterobacteriaceae genomes
iroNTax = sys.argv[2] # The file with taxonomic numbers of the genomes with iroN
out = sys.argv[3] # The output file (write it without extension!!!)

# Now let's open the taxonomy of the genomes and make it a dictionary.
# The keys will be taxonomic numbers and the values will be the species/strains names.
with open(wholeTax, 'r') as f:
    lines = f.readlines()

dictTax = {}
for line in lines:
    key, item = line.strip().split('\t')
    dictTax[key] = item

for key in dictTax:
    taxonomicLevels = dictTax[key].split(';')
    dictTax[key] = taxonomicLevels[-1]

# Now let's open the file with the taxonomic numbers of the genomes with iroN
with open(iroNTax, 'r') as f:
    taxaIroN = f.read().split('\n')

# Now let's write the species/strains names of the genomes with iroN to the output file
outputList = []
for taxaCode in taxaIroN:
    if taxaCode in dictTax:
        outputList.append(dictTax[taxaCode])

outputList.sort()

outputSet = set(outputList)
outputSet = list(outputSet)
outputSet.sort()

with open(out + '.txt', 'w') as f: # The file with all the species/strains
    for item in outputList:
        f.write("%s\n" % item)

with open(out + '.unique.txt', 'w') as f: # The file with all the species/strains
    for item in outputSet:
        f.write("%s\n" % item)