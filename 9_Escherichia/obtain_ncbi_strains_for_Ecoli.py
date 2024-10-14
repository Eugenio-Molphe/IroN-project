###########################################
#### Eugenio Perez Molphe Montoya ####
#### 14.10.2024 ####
#### Create a table with the identities of the genomes of Escherichia coli ####
###########################################

### Importing libraries
from Bio import Entrez
from Bio import SeqIO
import pandas as pd
import sys

### Get the arguments
# The input file (csv file with the accession numbers)
inputFile = sys.argv[1]
# The output file (csv file with the accession numbers and the strain)
outputFile = sys.argv[2]

### The functions
# Function to fetch taxon and strain
def get_assembly_id(accession):
    # Fetch the assembly ID
    handle = Entrez.esearch(db="assembly", term=accession)
    result = Entrez.read(handle)
    assembly_id = result['IdList'][0]
    return assembly_id


def fetch_taxon_and_strain(accession):
    # Get the internal assembly ID
    assemblyId = get_assembly_id(accession)

    # Fetch the assembly information
    handle = Entrez.esummary(db="assembly", id=assemblyId, retmode="xml")
    record = Entrez.read(handle, validate=False)
    handle.close()
    
    # Extracting Taxon and Strain
    assembly_info = record['DocumentSummarySet']['DocumentSummary'][0]
    taxon = assembly_info['Organism']
    try:
        if assembly_info['Biosource']['InfraspeciesList'][1]['Sub_type'] == 'strain':
            strain = assembly_info['Biosource']['InfraspeciesList'][1]['Sub_value']
    except:
        if assembly_info['Biosource']['InfraspeciesList'][0]['Sub_type'] == 'strain':
            strain = assembly_info['Biosource']['InfraspeciesList'][0]['Sub_value']
        else:
            strain = 'serotype ' + assembly_info['Biosource']['InfraspeciesList'][0]['Sub_value']

    return taxon, strain

### Main code ###

# Read the input file and get a list of accession numbers
accessionDf = pd.read_csv(inputFile)
accessionList = accessionDf["accession"].tolist()

# Fetch the Taxon and Strain for each accession
# Set your email (required by NCBI)
Entrez.email = "eugenio.perez@mls.uzh.ch"

# Lists to store the results
taxonList = []
strainList = []

# Fetch and print Taxon and Strain for each accession
for accession in accessionList:
    taxon, strain = fetch_taxon_and_strain(accession)
    taxonList.append(taxon)
    strainList.append(strain)
    print("Accession:", accession, 'strain:', strain)
print('All our Escherichia strains have their strains')

# Create a dataframe with the results
accessionDf["Taxon"] = taxonList
accessionDf["Strain"] = strainList

# Save the updated dataframe to the output file
accessionDf.to_csv(outputFile, index=False)
print("The dataframe has been saved to", outputFile)